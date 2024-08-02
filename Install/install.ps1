$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isadmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isadmin) {
	$pyPath = Join-Path $ENV:TEMP "python-3.12.4.exe"
	Write-Host "Download python to " $pyPath " ..."
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
	Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.4/python-3.12.4.exe" -OutFile $pyPath
	Write-Host "installing python..."
	& $pyPath /passive InstallAllUsers=0 InstallLauncherAllUsers=1 AssociateFiles=1 PrependPath=1 Include_test=0   | Out-Null
	write-host "Install required modules..."
	$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") 
	pip install -r requirements.txt
	# create shortcut
	#python Make_shortcut.py
	
	
	
	write-host "Installation Done."
} else {
	Write-Host "Error: This script must be run as administrator."
}