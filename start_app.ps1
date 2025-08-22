# SecureBank Pro Launcher
Write-Host "🏦 Starting SecureBank Pro..." -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "📁 Current directory: $scriptDir" -ForegroundColor Yellow
Write-Host ""

# Python executable path
$pythonPath = "C:/Users/chinu/OneDrive/Documents/Workspace/.venv/Scripts/python.exe"

Write-Host "🐍 Checking Python environment..." -ForegroundColor Green
if (Test-Path $pythonPath) {
    Write-Host "✅ Python environment found!" -ForegroundColor Green
} else {
    Write-Host "❌ Python environment not found at: $pythonPath" -ForegroundColor Red
    Write-Host "Please ensure the virtual environment is set up correctly." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Launching Streamlit application..." -ForegroundColor Magenta
Write-Host "🌐 The app will open in your default browser" -ForegroundColor Cyan
Write-Host "📱 Access URL: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  Press Ctrl+C to stop the application" -ForegroundColor Red
Write-Host ""

# Start the Streamlit app
& $pythonPath -m streamlit run bank_management_app.py

Write-Host ""
Write-Host "👋 Thanks for using SecureBank Pro!" -ForegroundColor Green
Read-Host "Press Enter to exit"
