$ErrorActionPreference = 'Stop';
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"

$packageArgs = @{
  packageName   = $env:ChocolateyPackageName
  destination   = "$toolsDir"
  file64        = "$toolsDir\ngspice-41_64.7z"  
}

Get-ChocolateyUnzip @packageArgs

# Install start menu shortcuts
$programs = [environment]::GetFolderPath([environment+specialfolder]::Programs)
$shortcutFilePath = Join-Path $programs "Ngspice.lnk"
$targetPath = Join-Path $toolsDir "Spice64\bin\ngspice.exe"
Install-ChocolateyShortcut -shortcutFilePath $shortcutFilePath -targetPath $targetPath

$shortcutFilePath = Join-Path $programs "Ngspice Console.lnk"
$targetPath = Join-Path $toolsDir "Spice64\bin\ngspice_con.exe"
Install-ChocolateyShortcut -shortcutFilePath $shortcutFilePath -targetPath $targetPath
