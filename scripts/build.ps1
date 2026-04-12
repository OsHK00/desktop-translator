param(
    [switch]$OneFile = $true
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot

$venvPython = Join-Path $projectRoot "venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

Write-Host "Using Python: $python"

& $python -m pip show pyinstaller *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PyInstaller..."
    & $python -m pip install pyinstaller
}

$appName = "TranslateApp"
$entrypoint = "src\translateapp\main.py"
$distDir = Join-Path $projectRoot "dist"
$buildDir = Join-Path $projectRoot "build"
$specFile = Join-Path $projectRoot "$appName.spec"
$iconPath = Join-Path $projectRoot "assets\translate-icon.ico"

if (Test-Path $buildDir) { Remove-Item -LiteralPath $buildDir -Recurse -Force }
if (Test-Path (Join-Path $distDir $appName)) { Remove-Item -LiteralPath (Join-Path $distDir $appName) -Recurse -Force }
if (Test-Path $specFile) { Remove-Item -LiteralPath $specFile -Force }

$modeArg = if ($OneFile) { "--onefile" } else { "--onedir" }

$args = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",
    $modeArg,
    "--name", $appName,
    "--paths", "src",
    "--add-data", "assets;assets",
    "--add-data", "config;config",
    $entrypoint
)

if (Test-Path $iconPath) {
    $args += @("--icon", $iconPath)
}

Write-Host "Building $appName ($modeArg)..."
& $python @args

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed with exit code $LASTEXITCODE"
}

Write-Host "Build completed."
if ($OneFile) {
    Write-Host ("Output: " + (Join-Path $distDir "$appName.exe"))
} else {
    Write-Host ("Output: " + (Join-Path $distDir $appName))
}