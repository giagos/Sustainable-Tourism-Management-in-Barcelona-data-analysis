param(
    [string]$WorkspaceRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Get-ExtensionFromContentType {
    param(
        [string]$ContentType
    )

    if (-not $ContentType) {
        return '.bin'
    }

    switch -Regex ($ContentType.ToLowerInvariant()) {
        'text/csv' { return '.csv' }
        'application/csv' { return '.csv' }
        'application/zip' { return '.zip' }
        'application/gzip' { return '.gz' }
        'application/x-gzip' { return '.gz' }
        'application/json' { return '.json' }
        'application/geo\+json' { return '.geojson' }
        'application/vnd\.geo\+json' { return '.geojson' }
        default { return '.bin' }
    }
}

function Get-SafeName {
    param(
        [string]$Value
    )

    if (-not $Value) {
        return 'unnamed'
    }

    return (($Value -replace '[\\/:*?"<>|]', '_') -replace '\s+', '_')
}

function Get-RelativePath {
    param(
        [string]$Root,
        [string]$Path
    )

    $rootPath = (Resolve-Path $Root).ProviderPath.TrimEnd('\\')
    $fullPath = (Resolve-Path $Path).ProviderPath

    if ($fullPath.StartsWith($rootPath, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $fullPath.Substring($rootPath.Length).TrimStart('\\')
    }

    $rootUri = New-Object System.Uri($rootPath + '\\')
    $pathUri = New-Object System.Uri($fullPath)
    return [System.Uri]::UnescapeDataString($rootUri.MakeRelativeUri($pathUri).ToString()).Replace('/', '\\')
}

function Get-DestinationInfo {
    param(
        [uri]$Uri
    )

    $segments = $Uri.AbsolutePath.Trim('/') -split '/'

    if ($Uri.Host -like '*insideairbnb.com') {
        $city = $segments[2]
        $snapshot = $segments[3]
        $section = $segments[4]
        $fileName = [System.IO.Path]::GetFileName($Uri.AbsolutePath)

        return [PSCustomObject]@{
            SourceGroup = 'inside_airbnb'
            DatasetId = "$city-$snapshot"
            ResourceId = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
            RelativeDirectory = Join-Path 'Data\\raw\\inside_airbnb' (Join-Path "$city-$snapshot" $section)
            FileName = $fileName
            Label = "inside_airbnb_${city}_${snapshot}_$([System.IO.Path]::GetFileNameWithoutExtension($fileName))"
            NeedsResolvedName = $false
        }
    }

    if ($Uri.Host -like '*opendata.portdebarcelona.cat') {
        $fileName = [System.IO.Path]::GetFileName($Uri.AbsolutePath)

        return [PSCustomObject]@{
            SourceGroup = 'port_barcelona'
            DatasetId = 'passenger_traffic'
            ResourceId = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
            RelativeDirectory = 'Data\\raw\\port_barcelona\\passenger_traffic'
            FileName = $fileName
            Label = "port_barcelona_$([System.IO.Path]::GetFileNameWithoutExtension($fileName))"
            NeedsResolvedName = $false
        }
    }

    if ($Uri.Host -like '*opendata-ajuntament.barcelona.cat') {
        $datasetIndex = [Array]::IndexOf($segments, 'dataset')
        $resourceIndex = [Array]::IndexOf($segments, 'resource')
        $datasetId = if ($datasetIndex -ge 0 -and $datasetIndex + 1 -lt $segments.Length) { $segments[$datasetIndex + 1] } else { 'unknown_dataset' }
        $resourceId = if ($resourceIndex -ge 0 -and $resourceIndex + 1 -lt $segments.Length) { $segments[$resourceIndex + 1] } else { 'unknown_resource' }

        return [PSCustomObject]@{
            SourceGroup = 'barcelona_open_data'
            DatasetId = $datasetId
            ResourceId = $resourceId
            RelativeDirectory = Join-Path 'Data\\raw\\barcelona_open_data' $datasetId
            FileName = $null
            Label = "barcelona_open_data_${datasetId}_${resourceId}"
            NeedsResolvedName = $true
        }
    }

    throw "Unsupported URL host: $($Uri.Host)"
}

$WorkspaceRoot = (Resolve-Path $WorkspaceRoot).ProviderPath

$linksPath = Join-Path $WorkspaceRoot 'links.tex'
if (-not (Test-Path $linksPath)) {
    throw "Links file not found: $linksPath"
}

$catalogDir = Join-Path $WorkspaceRoot 'Data\\catalog'
$rawDir = Join-Path $WorkspaceRoot 'Data\\raw'
$tmpDir = Join-Path $WorkspaceRoot 'Data\\_tmp_downloads'

foreach ($dir in @($catalogDir, $rawDir, $tmpDir)) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

$urls = Get-Content $linksPath |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and ($_ -match '^https?://') }

$manifest = New-Object System.Collections.Generic.List[object]

foreach ($url in $urls) {
    $uri = [uri]$url
    $destination = Get-DestinationInfo -Uri $uri
    $targetDirectory = Join-Path $WorkspaceRoot $destination.RelativeDirectory

    if (-not (Test-Path $targetDirectory)) {
        New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null
    }

    if (-not $destination.NeedsResolvedName) {
        $targetPath = Join-Path $targetDirectory $destination.FileName
        Invoke-WebRequest -Uri $url -OutFile $targetPath -MaximumRedirection 5
        $finalUrl = $url
        $contentType = $null
        $sizeBytes = (Get-Item $targetPath).Length
    }
    else {
        $tempPath = Join-Path $tmpDir ("$($destination.ResourceId).download")
        if (Test-Path $tempPath) {
            Remove-Item $tempPath -Force
        }

        $response = Invoke-WebRequest -Uri $url -OutFile $tempPath -PassThru -MaximumRedirection 5
        $finalUrl = $response.BaseResponse.ResponseUri.AbsoluteUri
        $contentType = $response.Headers['Content-Type']
        $resolvedLeaf = [System.IO.Path]::GetFileName(([uri]$finalUrl).AbsolutePath)

        if ((-not $resolvedLeaf) -or ($resolvedLeaf -ieq 'download')) {
            $resolvedLeaf = "$($destination.ResourceId)$(Get-ExtensionFromContentType -ContentType $contentType)"
        }

        $fileName = "resource_$($destination.ResourceId)__$(Get-SafeName $resolvedLeaf)"
        $targetPath = Join-Path $targetDirectory $fileName

        Get-ChildItem -Path $targetDirectory -Filter "resource_$($destination.ResourceId)__*" -ErrorAction SilentlyContinue |
            Remove-Item -Force

        if (Test-Path $targetPath) {
            Remove-Item $targetPath -Force
        }

        Move-Item -Path $tempPath -Destination $targetPath
        $sizeBytes = (Get-Item $targetPath).Length
    }

    $manifest.Add([PSCustomObject]@{
        source_group = $destination.SourceGroup
        dataset_id = $destination.DatasetId
        resource_id = $destination.ResourceId
        label = $destination.Label
        relative_path = Get-RelativePath -Root $WorkspaceRoot -Path $targetPath
        original_url = $url
        final_url = $finalUrl
        content_type = $contentType
        size_bytes = $sizeBytes
    })
}

$manifestPath = Join-Path $catalogDir 'dataset_manifest.csv'
$manifest | Sort-Object source_group, dataset_id, relative_path | Export-Csv -Path $manifestPath -NoTypeInformation -Encoding UTF8

if (Test-Path $tmpDir) {
    Remove-Item $tmpDir -Recurse -Force
}

Write-Host "Downloaded $($manifest.Count) files."
Write-Host "Manifest: $manifestPath"