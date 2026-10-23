$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $repoRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Missing .venv. Follow README.md to install dependencies first.'
}
$labs = @('lab01-xu-ly-van-ban', 'lab02-xay-dung-chi-muc-nguoc', 'lab03-xu-ly-cau-truy-van')
foreach ($lab in $labs) {
    Push-Location (Join-Path $repoRoot $lab)
    try {
        Write-Host "Checking $lab"
        & $pythonPath -m compileall -q .
        if ($LASTEXITCODE -ne 0) { throw "Compile failed: $lab" }
        & $pythonPath -m unittest discover -s tests -p 'test_*.py' -v
        if ($LASTEXITCODE -ne 0) { throw "Tests failed: $lab" }
    } finally {
        Pop-Location
    }
}
