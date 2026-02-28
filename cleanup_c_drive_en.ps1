#Requires -RunAsAdministrator
# Windows C Drive Cleanup Script v2.0
# Run as Administrator

$ErrorActionPreference = "SilentlyContinue"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Get-FolderSize {
    param([string]$Path)
    if (Test-Path $Path) {
        $size = (Get-ChildItem -Path $Path -Recurse -Force -ErrorAction SilentlyContinue | 
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        return [math]::Round($size / 1MB, 2)
    }
    return 0
}

function Remove-SafelyWithStats {
    param([string]$Path, [string]$Description, [int]$DaysOld = 0)
    
    if (Test-Path $Path) {
        $beforeSize = Get-FolderSize -Path $Path
        try {
            if ($DaysOld -gt 0) {
                $cutoffDate = (Get-Date).AddDays(-$DaysOld)
                Get-ChildItem -Path $Path -Recurse -Force -ErrorAction SilentlyContinue | 
                    Where-Object { $_.LastWriteTime -lt $cutoffDate } |
                    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            } else {
                Get-ChildItem -Path $Path -Recurse -Force -ErrorAction SilentlyContinue | 
                    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            }
            $afterSize = Get-FolderSize -Path $Path
            $freedSpace = $beforeSize - $afterSize
            if ($freedSpace -gt 0) {
                Write-ColorOutput "  [OK] $Description - Freed: $freedSpace MB" "Green"
                return $freedSpace
            } else {
                Write-ColorOutput "  [--] $Description - Already clean" "Gray"
            }
        } catch {
            Write-ColorOutput "  [!!] $Description - Some files in use" "Yellow"
        }
    } else {
        Write-ColorOutput "  [--] $Description - Path not found" "Gray"
    }
    return 0
}

Clear-Host
Write-ColorOutput "================================================================" "Cyan"
Write-ColorOutput "         Windows C Drive Deep Cleanup Tool v2.0                 " "Cyan"
Write-ColorOutput "         Please run as Administrator                            " "Cyan"
Write-ColorOutput "================================================================" "Cyan"
Write-Host ""

$diskBefore = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'" | 
              Select-Object @{N='FreeSpace';E={[math]::Round($_.FreeSpace/1GB, 2)}}
Write-ColorOutput "Before cleanup - C: Free Space: $($diskBefore.FreeSpace) GB" "Yellow"
Write-Host ""

$totalFreed = 0

# 1. User Temp Files
Write-ColorOutput "[1/8] Cleaning User Temp Files..." "Cyan"
$totalFreed += Remove-SafelyWithStats -Path "$env:TEMP" -Description "User Temp Folder"
$totalFreed += Remove-SafelyWithStats -Path "$env:LOCALAPPDATA\Temp" -Description "Local App Temp"
Write-Host ""

# 2. System Temp Files
Write-ColorOutput "[2/8] Cleaning System Temp Files..." "Cyan"
$totalFreed += Remove-SafelyWithStats -Path "C:\Windows\Temp" -Description "Windows Temp"
$totalFreed += Remove-SafelyWithStats -Path "C:\Windows\Prefetch" -Description "Prefetch Files" -DaysOld 30
Write-Host ""

# 3. Windows Update Cache
Write-ColorOutput "[3/8] Cleaning Windows Update Cache..." "Cyan"
Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
$totalFreed += Remove-SafelyWithStats -Path "C:\Windows\SoftwareDistribution\Download" -Description "Windows Update Cache"
Start-Service -Name wuauserv -ErrorAction SilentlyContinue
Write-Host ""

# 4. Browser Cache
Write-ColorOutput "[4/8] Cleaning Browser Cache..." "Cyan"
$chromePaths = @(
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache"
)
foreach ($path in $chromePaths) {
    $totalFreed += Remove-SafelyWithStats -Path $path -Description "Chrome Cache"
}

$edgePaths = @(
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache"
)
foreach ($path in $edgePaths) {
    $totalFreed += Remove-SafelyWithStats -Path $path -Description "Edge Cache"
}

$firefoxPath = "$env:LOCALAPPDATA\Mozilla\Firefox\Profiles"
if (Test-Path $firefoxPath) {
    Get-ChildItem -Path $firefoxPath -Directory | ForEach-Object {
        $totalFreed += Remove-SafelyWithStats -Path "$($_.FullName)\cache2" -Description "Firefox Cache"
    }
}
Write-Host ""

# 5. System Logs
Write-ColorOutput "[5/8] Cleaning System Logs..." "Cyan"
$totalFreed += Remove-SafelyWithStats -Path "C:\Windows\Logs\CBS" -Description "CBS Logs" -DaysOld 30
$totalFreed += Remove-SafelyWithStats -Path "C:\Windows\Logs\DISM" -Description "DISM Logs" -DaysOld 30
$totalFreed += Remove-SafelyWithStats -Path "C:\inetpub\logs" -Description "IIS Logs" -DaysOld 30

try {
    wevtutil cl Application 2>$null
    wevtutil cl System 2>$null
    Write-ColorOutput "  [OK] Windows Event Logs cleared" "Green"
} catch {
    Write-ColorOutput "  [!!] Event Logs cleanup failed" "Yellow"
}
Write-Host ""

# 6. Recycle Bin
Write-ColorOutput "[6/8] Cleaning Recycle Bin..." "Cyan"
try {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    Write-ColorOutput "  [OK] Recycle Bin emptied" "Green"
} catch {
    Write-ColorOutput "  [!!] Recycle Bin cleanup failed" "Yellow"
}
Write-Host ""

# 7. Other Caches
Write-ColorOutput "[7/8] Cleaning Other Caches..." "Cyan"
$totalFreed += Remove-SafelyWithStats -Path "C:\Windows\Installer\`$PatchCache`$" -Description "Installer Patch Cache"
$totalFreed += Remove-SafelyWithStats -Path "C:\ProgramData\Microsoft\Windows\WER" -Description "Error Reports" -DaysOld 7
$totalFreed += Remove-SafelyWithStats -Path "$env:LOCALAPPDATA\Microsoft\Windows\WER" -Description "User Error Reports" -DaysOld 7
$totalFreed += Remove-SafelyWithStats -Path "$env:LOCALAPPDATA\D3DSCache" -Description "DirectX Shader Cache"
$totalFreed += Remove-SafelyWithStats -Path "$env:LOCALAPPDATA\npm-cache" -Description "NPM Cache" -DaysOld 30
$totalFreed += Remove-SafelyWithStats -Path "$env:LOCALAPPDATA\pip\cache" -Description "pip Cache" -DaysOld 30
Write-Host ""

# 8. Disk Cleanup Tool
Write-ColorOutput "[8/8] Running Disk Cleanup Tool..." "Cyan"
$cleanupKey = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches"
$cleanupItems = @(
    "Active Setup Temp Folders",
    "Downloaded Program Files",
    "Internet Cache Files",
    "Old ChkDsk Files",
    "Recycle Bin",
    "Setup Log Files",
    "System error memory dump files",
    "System error minidump files",
    "Temporary Files",
    "Temporary Setup Files",
    "Thumbnail Cache",
    "Update Cleanup"
)

foreach ($item in $cleanupItems) {
    $path = "$cleanupKey\$item"
    if (Test-Path $path) {
        Set-ItemProperty -Path $path -Name StateFlags0001 -Value 2 -ErrorAction SilentlyContinue
    }
}

Start-Process -FilePath "cleanmgr.exe" -ArgumentList "/sagerun:1" -NoNewWindow -ErrorAction SilentlyContinue
Write-ColorOutput "  [OK] Disk Cleanup running in background" "Green"
Write-Host ""

# Summary
Start-Sleep -Seconds 2
$diskAfter = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'" | 
             Select-Object @{N='FreeSpace';E={[math]::Round($_.FreeSpace/1GB, 2)}}

Write-ColorOutput "================================================================" "Green"
Write-ColorOutput "                    CLEANUP COMPLETE                            " "Green"
Write-ColorOutput "================================================================" "Green"
Write-ColorOutput "  Before: $($diskBefore.FreeSpace) GB" "White"
Write-ColorOutput "  After:  $($diskAfter.FreeSpace) GB" "White"
$freedGB = [math]::Round($diskAfter.FreeSpace - $diskBefore.FreeSpace, 2)
if ($freedGB -gt 0) {
    Write-ColorOutput "  Freed:  $freedGB GB" "Yellow"
} else {
    Write-ColorOutput "  Freed:  Calculating (Disk Cleanup still running)" "Yellow"
}
Write-ColorOutput "================================================================" "Green"
Write-Host ""

Write-ColorOutput "[Additional Tips]" "Cyan"
Write-Host "  1. Run: Dism.exe /online /Cleanup-Image /StartComponentCleanup"
Write-Host "  2. Uninstall unused programs"
Write-Host "  3. Use WizTree to find large files"
Write-Host "  4. Disable hibernation: powercfg -h off"
Write-Host ""

Write-ColorOutput "Press any key to exit..." "Gray"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
