# 🧹 Clean and Reset Solar System Setup

Write-Host ""
Write-Host "🧹 Solar System 3D - Clean Install" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  This will DELETE the virtual environment and reinstall everything."
Write-Host ""

$response = Read-Host "Continue? (yes/no)"
if ($response -ne "yes") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "🗑️  Removing virtual environment..."
if (Test-Path ".\venv") {
    Remove-Item -Recurse -Force ".\venv"
    Write-Host "✅ Removed venv" -ForegroundColor Green
} else {
    Write-Host "ℹ️  venv not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🗑️  Removing cache and temporary files..."
if (Test-Path ".\__pycache__") {
    Remove-Item -Recurse -Force ".\__pycache__" -ErrorAction SilentlyContinue
}
if (Test-Path ".\.pytest_cache") {
    Remove-Item -Recurse -Force ".\.pytest_cache" -ErrorAction SilentlyContinue
}
if (Test-Path ".\*.pyc") {
    Remove-Item ".\*.pyc" -ErrorAction SilentlyContinue
}
Write-Host "✅ Cache cleared" -ForegroundColor Green

Write-Host ""
Write-Host "📦 Creating new virtual environment..."
python -m venv venv
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create venv" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📥 Installing dependencies..."
Write-Host "   (This may take a few minutes...)" -ForegroundColor Yellow
Write-Host ""

# Upgrade pip and setuptools first (but don't fail if it errors)
Write-Host "Upgrading pip..." -ForegroundColor Gray
.\venv\Scripts\python -m pip install --upgrade pip setuptools wheel --no-warn-script-location --disable-pip-version-check
if ($LASTEXITCODE -ne 0) {
    Write-Host "ℹ️  pip upgrade skipped (continuing with old pip)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Installing packages..." -ForegroundColor Gray

# Install packages
.\venv\Scripts\pip install --prefer-binary -r requirements.txt --no-warn-script-location --disable-pip-version-check
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠️  Trying alternative installation method..." -ForegroundColor Yellow
    .\venv\Scripts\pip install --no-build-isolation -r requirements.txt --disable-pip-version-check
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Installation failed" -ForegroundColor Red
        Write-Host ""
        Write-Host "Try these steps:" -ForegroundColor Yellow
        Write-Host "1. Close all Python windows"
        Write-Host "2. Run PowerShell as Administrator"  
        Write-Host "3. Delete: Remove-Item -Recurse venv"
        Write-Host "4. Try again"
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next step:"
Write-Host "  .\run.bat"
Write-Host ""

Read-Host "Press Enter to close"
