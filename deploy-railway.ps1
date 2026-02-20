# Railway Deployment Script
# Deploy Security Scanner to Railway

Write-Host "🚀 Deploying Security Scanner to Railway..." -ForegroundColor Green

# Check if Railway CLI is installed
$railway = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railway) {
    Write-Host "❌ Railway CLI not found. Installing..." -ForegroundColor Red
    npm install -g @railway/cli
}

# Navigate to project directory
$projectPath = "C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner"
Set-Location $projectPath
Write-Host "📁 Changed to: $projectPath" -ForegroundColor Cyan

# Check if already initialized
if (Test-Path ".railway") {
    Write-Host "✅ Railway project already initialized" -ForegroundColor Green
} else {
    Write-Host "🔧 Initializing Railway project..." -ForegroundColor Yellow
    railway init
}

# Check if PostgreSQL is added
$dbConfig = Get-Content "railway.json" -ErrorAction SilentlyContinue | ConvertFrom-Json
if ($dbConfig -and $dbConfig.services) {
    Write-Host "✅ Database already configured" -ForegroundColor Green
} else {
    Write-Host "🔧 Adding PostgreSQL database..." -ForegroundColor Yellow
    railway add postgresql
}

# Deploy
Write-Host "🚀 Deploying to Railway..." -ForegroundColor Yellow
railway up

# Get domain
Write-Host "🌐 Getting deployment URL..." -ForegroundColor Yellow
$domain = railway domain
Write-Host "✅ Deployed successfully!" -ForegroundColor Green
Write-Host "🌐 Your app is available at: $domain" -ForegroundColor Cyan
Write-Host "📚 API Documentation: $domain/docs" -ForegroundColor Cyan
Write-Host "❤️ Health Check: $domain/health" -ForegroundColor Cyan

# Test deployment
Write-Host ""
Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
try {
    $response = Invoke-WebRequest -Uri "$domain/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Health check passed!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Health check failed with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Deployment complete!" -ForegroundColor Green