$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$launcher=Join-Path $root 'START-STUDIO.pyw'
$pythonw=(Get-Command pythonw.exe -ErrorAction Stop).Source
$icon=Join-Path $root 'studio.ico'
if(!(Test-Path $launcher)){throw 'Browser launcher missing'}
if(!(Test-Path $icon)){throw 'Icon missing'}
$desktop=[Environment]::GetFolderPath('DesktopDirectory')
if(!(Test-Path $desktop)){throw 'Desktop unavailable'}
$shell=New-Object -ComObject WScript.Shell
$path=Join-Path $desktop 'AI Content Production Engine.lnk'
$link=$shell.CreateShortcut($path)
$link.TargetPath=$pythonw
$link.Arguments='-B "'+$launcher+'"'
$link.WorkingDirectory=$root
$link.IconLocation="$icon,0"
$link.Description='AI Content Production Engine - open browser dashboard only'
$link.Save()
$check=$shell.CreateShortcut($path)
if($check.TargetPath -ne $pythonw -or $check.Arguments -ne $link.Arguments){throw 'Shortcut verification failed'}
Write-Output "Desktop shortcut verified: $path"
Write-Output "Target: $($check.TargetPath)"
Write-Output "Arguments: $($check.Arguments)"
Write-Output "Icon: $($check.IconLocation)"
$bridge=Join-Path $root 'START-NOTEBOOK-BRIDGE.cmd'
if(Test-Path $bridge){
 $bp=Join-Path $desktop 'Notebook Media Bridge.lnk'
 $bl=$shell.CreateShortcut($bp)
 $bl.TargetPath=$bridge
 $bl.WorkingDirectory=$root
 $bl.IconLocation="$icon,0"
 $bl.Description='Notebook Media Bridge - local preview and analytics'
 $bl.Save()
 if($shell.CreateShortcut($bp).TargetPath -ne $bridge){throw 'Notebook shortcut verification failed'}
}
