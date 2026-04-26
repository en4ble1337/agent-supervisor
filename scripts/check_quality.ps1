# Quality Check Script

Write-Host "Running Backend Quality Checks..." -ForegroundColor Cyan
.\.venv\Scripts\ruff check .
if ($LASTEXITCODE -ne 0) { Write-Host "Backend Lint Failed" -ForegroundColor Red; exit 1 }

.\.venv\Scripts\mypy backend
if ($LASTEXITCODE -ne 0) { Write-Host "Backend Type Check Failed" -ForegroundColor Red; exit 1 }

Write-Host "Running Backend Tests..." -ForegroundColor Cyan
.\.venv\Scripts\python -m pytest tests/ -v
if ($LASTEXITCODE -ne 0) { Write-Host "Backend Tests Failed" -ForegroundColor Red; exit 1 }

Write-Host "Running Frontend Quality Checks..." -ForegroundColor Cyan
cd frontend
npm run lint
if ($LASTEXITCODE -ne 0) { Write-Host "Frontend Lint Failed" -ForegroundColor Red; cd ..; exit 1 }

npx tsc --noEmit
if ($LASTEXITCODE -ne 0) { Write-Host "Frontend Type Check Failed" -ForegroundColor Red; cd ..; exit 1 }

Write-Host "Running Frontend Tests..." -ForegroundColor Cyan
npm run test
if ($LASTEXITCODE -ne 0) { Write-Host "Frontend Tests Failed" -ForegroundColor Red; cd ..; exit 1 }

cd ..
Write-Host "All Quality Checks Passed!" -ForegroundColor Green
exit 0
