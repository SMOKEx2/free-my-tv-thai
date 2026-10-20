$ErrorActionPreference = 'Stop'
try {
    Import-Module Microsoft.PowerShell.Utility -ErrorAction Stop
    if (-not [Environment]::Is64BitOperatingSystem -or $env:PROCESSOR_ARCHITECTURE -eq 'ARM64') {
        throw 'The included toolchain supports Windows x64. See INSTALL.md for other build hosts.'
    }
    $manifestPath = Join-Path $PSScriptRoot 'tools\bundles\windows-x64.json'
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $archivePath = Join-Path $PSScriptRoot ('tools\bundles\' + $manifest.archive)
    if ((Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash -ne $manifest.sha256) {
        throw 'Bundled tool archive checksum mismatch. Download a fresh copy of this repository.'
    }
    $toolsRoot = Join-Path $PSScriptRoot '.local\toolchain'
    if (-not (Test-Path -LiteralPath (Join-Path $toolsRoot 'python\python.exe'))) {
        Write-Host 'Extracting the included portable tools (no separate downloads)...'
        Expand-Archive -LiteralPath $archivePath -DestinationPath $toolsRoot -Force
    }
    foreach ($entry in $manifest.files.PSObject.Properties) {
        $filePath = Join-Path $toolsRoot $entry.Name
        if (-not (Test-Path -LiteralPath $filePath) -or
            (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash -ne $entry.Value) {
            throw ('Extracted tool verification failed: ' + $entry.Name + '. Extract tools/bundles/windows-x64.zip again into .local/toolchain.')
        }
    }
    $env:ADB_VENDOR_KEYS = Join-Path $PSScriptRoot '.local\adb-keys'
    $env:ANDROID_USER_HOME = Join-Path $PSScriptRoot '.local\android'
    $env:PYTHONUTF8 = '1'
    New-Item -ItemType Directory -Path $env:ADB_VENDOR_KEYS -Force | Out-Null
    & (Join-Path $toolsRoot 'python\python.exe') (Join-Path $PSScriptRoot 'tools\tv_setup.py') @args
    exit $LASTEXITCODE
} catch {
    Write-Error $_
    exit 1
}
