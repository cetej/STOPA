<#
.SYNOPSIS
  Sync master secrets.env into Windows User-scope environment variables.

.DESCRIPTION
  Reads ~/.claude/keys/secrets.env (KEY=VALUE per line), pushes each non-empty
  key into `[Environment]::SetEnvironmentVariable($k, $v, 'User')`. After sync,
  all new processes (CC, scheduled tasks, shells) inherit the values.

  Existing processes (already-running shells) will NOT see changes — restart them.

.PARAMETER DryRun
  Show what would be set, do not touch env vars.

.PARAMETER Clear
  Remove all keys that would have been synced (useful when rotating/revoking).

.EXAMPLE
  pwsh scripts/keys-sync.ps1
  pwsh scripts/keys-sync.ps1 -DryRun
  pwsh scripts/keys-sync.ps1 -Clear

.NOTES
  Safe: only writes keys listed in secrets.env. Never touches unrelated env vars.
  secrets.env is gitignored — never committed.
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Clear
)

$ErrorActionPreference = 'Stop'
$SecretsPath = Join-Path $HOME '.claude\keys\secrets.env'

if (-not (Test-Path $SecretsPath)) {
    Write-Host "ERROR: $SecretsPath not found." -ForegroundColor Red
    Write-Host "Copy secrets.env.template to secrets.env and fill in values first."
    exit 1
}

$synced = 0
$skipped = 0
$cleared = 0

Get-Content $SecretsPath | ForEach-Object {
    $line = $_.Trim()
    if ($line -eq '' -or $line.StartsWith('#')) { return }

    $idx = $line.IndexOf('=')
    if ($idx -lt 1) { return }

    $key = $line.Substring(0, $idx).Trim()
    $value = $line.Substring($idx + 1).Trim()

    if ($Clear) {
        if ($DryRun) {
            Write-Host "[DRY] would clear $key"
        } else {
            [Environment]::SetEnvironmentVariable($key, $null, 'User')
            Write-Host "CLEARED $key"
        }
        $script:cleared++
        return
    }

    if ($value -eq '') {
        Write-Host "SKIP $key (empty value)" -ForegroundColor DarkGray
        $script:skipped++
        return
    }

    if ($DryRun) {
        $preview = if ($value.Length -gt 8) { $value.Substring(0, 4) + '...' + $value.Substring($value.Length - 4) } else { '***' }
        Write-Host "[DRY] would set $key = $preview"
    } else {
        [Environment]::SetEnvironmentVariable($key, $value, 'User')
        Write-Host "SET $key" -ForegroundColor Green
    }
    $script:synced++
}

Write-Host ""
if ($Clear) {
    Write-Host "Cleared: $cleared keys"
} else {
    Write-Host "Synced: $synced   Skipped (empty): $skipped"
    if (-not $DryRun) {
        Write-Host ""
        Write-Host "IMPORTANT: restart open shells and Claude Code sessions to pick up changes." -ForegroundColor Yellow
    }
}
