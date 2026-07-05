# PowerShell helper to register a Windows Scheduled Task that runs the downloader schedule
param(
    [string]$Ticker = "^NSEI",
    [int]$Minutes = 60,
    [string]$WorkingDir = "C:\Users\anupa\OneDrive\Documents\Ai Trading Algo\trading"
)

$python = "python"
try {
    $python = (Get-Command python -ErrorAction Stop).Source
} catch {
    Write-Warning "`nPython executable not found in PATH. Ensure Python is installed or update the script to point to the correct python.exe.`n"
}

$psCommand = "cd '$WorkingDir'; & '$python' -m python.main schedule $Ticker --minutes $Minutes"
$action = New-ScheduledTaskAction -Execute "pwsh" -Argument "-NoProfile -WindowStyle Hidden -Command \"$psCommand\""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes $Minutes) -RepetitionDuration ([TimeSpan]::MaxValue)
Register-ScheduledTask -TaskName "AI-NIFTY-Downloader-$Ticker" -Action $action -Trigger $trigger -RunLevel Highest -Force
Write-Host "Registered scheduled task for $Ticker every $Minutes minutes. Use Task Scheduler to review or edit the task." 
