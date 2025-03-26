# Remove start menu shortcuts
$programs = [environment]::GetFolderPath([environment+specialfolder]::Programs)
$shortcutFilePath = Join-Path $programs "Ngspice.lnk"
if (Test-Path $shortcutFilePath) { Remove-Item $shortcutFilePath }

$shortcutFilePath = Join-Path $programs "Ngspice Console.lnk"
if (Test-Path $shortcutFilePath) { Remove-Item $shortcutFilePath }