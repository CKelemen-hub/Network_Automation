# Usage:
#   .\push-to-github.ps1 -RepoUrl "https://github.com/YOUR_USER/YOUR_REPO.git"
#
# For an existing repo that already has commits, this script pulls first (merge allowed).

param(
    [Parameter(Mandatory = $true)]
    [string]$RepoUrl,

    [string]$Branch = "main",
    [switch]$ForceFirstPush
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is not installed or not on PATH"
}

if (-not (Test-Path .git)) {
    git init
}

git add -A
$status = git status --porcelain
if ($status) {
    git commit -m @"
Add printer VLAN lab toolkit for EVE-NG validation.

Includes JSON deployment template, Python validate/generate scripts, and Ansible lab playbook.
"@
}

git branch -M $Branch

$remotes = git remote
if ($remotes -contains "origin") {
    git remote set-url origin $RepoUrl
} else {
    git remote add origin $RepoUrl
}

if ($ForceFirstPush) {
    git push -u origin $Branch --force
} else {
    git pull origin $Branch --allow-unrelated-histories 2>$null
    git push -u origin $Branch
}

Write-Host "Done. Remote: $RepoUrl branch: $Branch"
