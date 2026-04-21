$ErrorActionPreference = "Stop"

Write-Host "Virtual Health Assistant - sanity check" -ForegroundColor Cyan
Write-Host ""

function Check-File($path) {
  if (Test-Path $path) {
    $item = Get-Item $path
    $size = $item.Length

    # Avoid fancy inline expressions; keep Windows PowerShell compatible.
    $suffix = ""
    if ($size -lt 1024) {
      $suffix = " (small file: " + $size + " bytes)"
    } else {
      $suffix = " (" + $size + " bytes)"
    }

    Write-Host ("OK: " + $path + $suffix) -ForegroundColor Green
    return $true
  }
  Write-Host ("MISSING: " + $path) -ForegroundColor Red
  return $false
}

function Check-Command($name) {
  $cmd = Get-Command $name -ErrorAction SilentlyContinue
  if ($null -eq $cmd) {
    Write-Host ("MISSING COMMAND: " + $name) -ForegroundColor Yellow
    return $false
  }
  Write-Host ("OK: command " + $name + " (" + $cmd.Source + ")") -ForegroundColor Green
  return $true
}

Write-Host "## 1) Tools"
$hasGit = Check-Command git

if ($hasGit) {
  try {
    $lfsVersion = (& git lfs version) 2>$null
    if ($LASTEXITCODE -eq 0) {
      Write-Host ("OK: git lfs (" + $lfsVersion + ")") -ForegroundColor Green
    } else {
      Write-Host "MISSING: git lfs (install Git LFS / Git for Windows)" -ForegroundColor Yellow
    }
  } catch {
    Write-Host "MISSING: git lfs (install Git LFS / Git for Windows)" -ForegroundColor Yellow
  }
}

Check-Command python | Out-Null
Check-Command node | Out-Null
Check-Command npm | Out-Null

Write-Host ""
Write-Host "## 2) Git LFS-tracked files present (after clone: run 'git lfs pull')"

$paths = @(
  "data/raw/drugbank_clean.csv",
  "ml_models/models/symptom_vectorizer.pkl",
  "ml_models/models/disease_encoder.pkl",
  "ml_models/models/X_train.pkl",
  "ml_models/models/y_train.pkl"
)

$allOk = $true
foreach ($p in $paths) {
  $ok = Check-File $p
  if (-not $ok) { $allOk = $false }
}

Write-Host ""
Write-Host "## 3) Backend venv quick check"
if (Test-Path "backend/venv/Scripts/python.exe") {
  Write-Host "OK: backend venv exists (backend/venv)" -ForegroundColor Green
} else {
  Write-Host "NOTE: backend venv not found yet. Create it:" -ForegroundColor Yellow
  Write-Host "  cd backend; python -m venv venv; .\\venv\\Scripts\\Activate.ps1; pip install -r requirements.txt" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "## 4) ML inference model file (optional)"
if (Test-Path "ml_models/models/lightgbm_model.pkl") {
  Write-Host "OK: ml_models/models/lightgbm_model.pkl present" -ForegroundColor Green
} else {
  Write-Host "NOTE: ml_models/models/lightgbm_model.pkl is missing." -ForegroundColor Yellow
  Write-Host "  - For demo: set DEMO_ML_FALLBACK=1 in backend/.env" -ForegroundColor Yellow
  Write-Host "  - For real model: run feature_engineering.py then train_lightgbm.py" -ForegroundColor Yellow
}

Write-Host ""
if ($allOk) {
  Write-Host "Sanity check complete: looks good." -ForegroundColor Cyan
} else {
  Write-Host "Sanity check complete: some required files are missing." -ForegroundColor Yellow
  Write-Host "If you cloned from GitHub, run: git lfs install; git lfs pull" -ForegroundColor Yellow
}

