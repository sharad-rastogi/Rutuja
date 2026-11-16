param(
    [string]$Browser,
    [switch]$Headed
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path "reports", "test-results" | Out-Null

if ($Browser) {
    $env:PLAYWRIGHT_BROWSER = $Browser
}
if ($Headed) {
    $env:PLAYWRIGHT_HEADED = "true"
}

python -m pytest @args
exit $LASTEXITCODE
