# Zip eSim for copying into Ubuntu VM
# Run from anywhere; script finds eSim repo relative to itself
param(
    [string]$RepoPath = (Join-Path $PSScriptRoot ".."),
    [string]$OutZip = (Join-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) "eSim-for-VM.zip")
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $RepoPath)) {
    Write-Host "Repo not found: $RepoPath" -ForegroundColor Red
    exit 1
}
Write-Host "Zipping: $RepoPath" -ForegroundColor Cyan
Write-Host "Output:  $OutZip" -ForegroundColor Cyan
Compress-Archive -Path $RepoPath -DestinationPath $OutZip -Force
Write-Host "Done. Copy $OutZip into your Ubuntu VM, then:" -ForegroundColor Green
Write-Host "  mkdir -p ~/work && cd ~/work"
Write-Host "  unzip /path/to/eSim-for-VM.zip"
Write-Host "  cd eSim && git checkout Chatbot_Enhancements"
Write-Host "  chmod +x scripts/setup_copilot_ubuntu.sh && ./scripts/setup_copilot_ubuntu.sh"
