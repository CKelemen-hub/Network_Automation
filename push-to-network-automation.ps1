# Push this lab folder into:
#   https://github.com/CKelemen-hub/Network_Automation
# as subfolder: printer-vlan-lab/
#
# Usage (PowerShell):
#   cd C:\Users\csanad.kelemen\printer-vlan-lab
#   .\push-to-network-automation.ps1

$ErrorActionPreference = "Stop"

function Resolve-Git {
    $candidates = @(
        (Get-Command git -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source),
        "C:\Program Files\Git\cmd\git.exe",
        "C:\Program Files\Git\bin\git.exe"
    ) | Where-Object { $_ -and (Test-Path $_) }
    if (-not $candidates) {
        throw "git not found. Install Git for Windows: https://git-scm.com/download/win"
    }
    $script:GitExe = $candidates[0]
}

Resolve-Git

$RepoUrl = "https://github.com/CKelemen-hub/Network_Automation.git"
$SubfolderName = "printer-vlan-lab"
$LabSource = $PSScriptRoot
$CloneDir = Join-Path $env:TEMP "Network_Automation-push-$(Get-Random)"
$LabDest = Join-Path $CloneDir $SubfolderName

$ExcludeDirs = @(".git", ".venv", "__pycache__", "output")
$ExcludeFiles = @("_push.log", "push-to-github.ps1", "push-to-network-automation.ps1")

Write-Host "Using git: $GitExe"
Write-Host "Cloning $RepoUrl ..."
& $GitExe clone $RepoUrl $CloneDir

Write-Host "Copying lab into $SubfolderName/ ..."
if (Test-Path $LabDest) {
    Remove-Item $LabDest -Recurse -Force
}
New-Item -ItemType Directory -Path $LabDest -Force | Out-Null

Get-ChildItem $LabSource -Force | Where-Object {
    $_.Name -notin $ExcludeDirs -and $_.Name -notin $ExcludeFiles
} | ForEach-Object {
    Copy-Item $_.FullName -Destination $LabDest -Recurse -Force
}

Set-Location $CloneDir
& $GitExe add $SubfolderName
& $GitExe status

if (-not (& $GitExe diff --cached --quiet)) {
    & $GitExe commit -m @"
Add printer VLAN lab toolkit under $SubfolderName.

Python validation and IOS config generation for EVE-NG; Ansible lab playbook included.
"@
    & $GitExe push origin HEAD
    Write-Host "Pushed to $RepoUrl ($SubfolderName/)"
} else {
    Write-Host "No changes to commit (already up to date)."
}

Set-Location $LabSource
Write-Host "Clone workspace (optional cleanup): $CloneDir"
