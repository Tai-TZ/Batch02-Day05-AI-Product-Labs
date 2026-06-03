# Start FastAPI backend on port 8000
$BackendRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $BackendRoot

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example — add OPENROUTER_API_KEY or DEMO_MODE=true"
}

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
}

python run.py
