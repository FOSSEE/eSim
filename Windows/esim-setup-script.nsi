;NSIS Modern User Interface
;Start Menu Folder Selection Example Script
;Modified by Fahim Khan, Saurabh Bansode, Rahul Paknikar - 20_08_2019
;Made by eSim Team, FOSSEE, IIT Bombay

;--------------------------------
;Include Modern UI

 !include "MUI2.nsh"
 !include "ZipDLL.nsh"
 !include "EnvVarUpdate.nsh"
 !include "x64.nsh"
;--------------------------------

;General

!define PRODUCT_NAME "eSim" 
!define PRODUCT_VERSION "1.1.2.0"
!define VERSION "1.1.2.0"
!define PRODUCT_PUBLISHER "FOSSEE"
!define PRODUCT_WEB_SITE "http://fossee.in"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

VIAddVersionKey  "ProductName" "eSim"
VIProductVersion "${PRODUCT_VERSION}"
VIFileVersion "${VERSION}"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey  "CompanyName" "FOSSEE @ IIT-B"
VIAddVersionKey "LegalCopyright" "Copyright (C) 2007 Free Software Foundation,  Inc."
VIAddVersionKey "FileDescription" "eSim Installer"



;Default installation folder
  InstallDir "C:\"
  
;Get installation folder from registry if available
  InstallDirRegKey HKLM "Software\eSim" ""

;Request application privileges for Windows Vista
  RequestExecutionLevel user
  
;--------------------------------
;Variables
  Var StartMenuFolder
 
;--------------------------------
;Interface Settings
  !define MUI_ABORTWARNING
  !define Python_HOME "C:\Python27"
;--------------------------------

;Pages
  
  !insertmacro MUI_PAGE_LICENSE "LICENSE.rtf"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  
  ;Start Menu Folder Page Configuration

  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKLM" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\eSim" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
 
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "eSim-Installer.exe"


;Installer Sections
Section "Ngspice circuit simulator" SecDummy

  SetOutPath "$INSTDIR"
;ADD YOUR OWN FILES HERE...
ZipDLL::extractall "$EXEDIR\spice.zip" "C:\"
ZipDLL::extractall "$EXEDIR\eSim.zip" "$INSTDIR\"

;Copying Folder to install directory
SetOutPath "$INSTDIR\eSim"
;File /nonfatal /a /r "eSim\"



;Store installation folder
  WriteRegStr HKLM "Software\eSim" "" $INSTDIR
  
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
;Create shortcuts
  ;create desktop shortcut
  CreateShortCut "$DESKTOP\eSim.lnk" "$INSTDIR\eSim\esim.bat" "" "$EXEDIR\logo.ico" "" SW_SHOWMINIMIZED
  
  !insertmacro MUI_STARTMENU_WRITE_END
 
CreateDirectory "$PROFILE\AppData\Roaming\kicad"
; will replace the kicad folder. If there is not one, it will create
CopyFiles "$PROFILE\AppData\Roaming\kicad\fp-lib-table" "$PROFILE\AppData\Roaming\kicad\fp-lib-table-backup"
CopyFiles "$PROFILE\AppData\Roaming\kicad\fp-lib-table-online" "$PROFILE\AppData\Roaming\kicad\fp-lib-table-online-backup"
CopyFiles "$EXEDIR\dependencies\OfflineFiles\fp-lib-table" "$PROFILE\AppData\Roaming\kicad\"
CopyFiles "$EXEDIR\dependencies\OfflineFiles\fp-lib-table-online" "$PROFILE\AppData\Roaming\kicad\"
SectionEnd

Section -Prerequisites
  ;SetOutPath $INSTDIR\Prerequisites
  
  MessageBox MB_OK "Installing Python" 
      ExecWait '"msiexec" /i "$EXEDIR\dependencies\python-2.7.10.msi"'
	  
  ;Setting Environment Variable for Python
  ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "C:\Python27"
  
  
  MessageBox MB_OK "Installing PyQT4" 
      ExecWait "$EXEDIR\dependencies\PyQt4-4.10.4-gpl-Py2.7-Qt4.8.6-x32"
  
  MessageBox MB_OK "Installing Numpy"
	  ExecWait "$EXEDIR\dependencies\numpy-1.9.0-win32-superpack-python2.7.exe"
	  
  MessageBox MB_OK "Installing Matplotlib" 
      ExecWait "$EXEDIR\dependencies\matplotlib-1.4.0.win32-py2.7.exe"
	  
  MessageBox MB_OK "Installing dateutil for matplotlib"
	  ExecWait "$EXEDIR\dependencies\python-dateutil-2.2.win32-py2.7.exe"
	  
 MessageBox MB_OK "Installing six for matplotlib"
	  ExecWait "$EXEDIR\dependencies\six-1.8.0.win32-py2.7.exe" 

 MessageBox MB_OK "Installing pyparsing for matplotlib"
	  ExecWait "$EXEDIR\dependencies\pyparsing-2.0.2.win32-py2.7.exe"
	 
 
 
  MessageBox MB_OK "Installing KiCad"
    ExecWait "$EXEDIR\dependencies\kicad-4.0.7-i686.exe"


  Goto endActiveSync
  endActiveSync:
 

  ${If} ${RunningX64}
    
		${EnvVarUpdate} $0 "PATH" "A" "HKLM" "C:\Program Files (x86)\KiCad\bin"
		CopyFiles "$EXEDIR\dependencies\library\*.lib" "C:\Program Files (x86)\KiCad\share\library"
		CopyFiles "$EXEDIR\dependencies\library\*.dcm" "C:\Program Files (x86)\KiCad\share\library"
		CopyFiles "$EXEDIR\dependencies\template\kicad.pro" "C:\Program Files (x86)\KiCad\share\template"

		CopyFiles "$EXEDIR\dependencies\library\*.lib" "C:\Program Files (x86)\KiCad\share\kicad\library"
		CopyFiles "$EXEDIR\dependencies\library\*.dcm" "C:\Program Files (x86)\KiCad\share\kicad\library"
		CopyFiles "$EXEDIR\dependencies\template\kicad.pro" "C:\Program Files (x86)\KiCad\share\kicad\template"

		CopyFiles "$EXEDIR\dependencies\OfflineFiles\TerminalBlock_Altech_AK300-2_P5.00mm.kicad_mod" "C:\Program Files (x86)\KiCad\share\kicad\modules\Connectors_Terminal_Blocks.pretty\"
		CopyFiles "$EXEDIR\dependencies\OfflineFiles\TO-220-3_Vertical.kicad_mod" "C:\Program Files (x86)\KiCad\share\kicad\modules\TO_SOT_Packages_THT.pretty\"


    MessageBox MB_OK "Setting Permissions..."
      ExecWait "$EXEDIR\dependencies\permission (x86).bat"

  ${Else}
    
		${EnvVarUpdate} $0 "PATH" "A" "HKLM" "C:\Program Files\KiCad\bin"
		CopyFiles "$EXEDIR\dependencies\library\*.lib" "C:\Program Files\KiCad\share\library"
		CopyFiles "$EXEDIR\dependencies\library\*.dcm" "C:\Program Files\KiCad\share\library"
		CopyFiles "$EXEDIR\dependencies\template\kicad.pro" "C:\Program Files\KiCad\share\template"
		
		CopyFiles "$EXEDIR\dependencies\library\*.lib" "C:\Program Files\KiCad\share\kicad\library"
		CopyFiles "$EXEDIR\dependencies\library\*.dcm" "C:\Program Files\KiCad\share\kicad\library"
		CopyFiles "$EXEDIR\dependencies\template\kicad.pro" "C:\Program Files\KiCad\share\kicad\template"

		CopyFiles "$EXEDIR\dependencies\OfflineFiles\TerminalBlock_Altech_AK300-2_P5.00mm.kicad_mod" "C:\Program Files\KiCad\share\kicad\modules\Connectors_Terminal_Blocks.pretty\"
		CopyFiles "$EXEDIR\dependencies\OfflineFiles\TO-220-3_Vertical.kicad_mod" "C:\Program Files\KiCad\share\kicad\modules\TO_SOT_Packages_THT.pretty\"


    MessageBox MB_OK "Setting Permissions..."
      ExecWait "$EXEDIR\dependencies\permission.bat"

 ${EndIf}    
		
 ;Setting Env Variable for ngspice 
 ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "C:\spice\bin"
 
 
 
 SectionEnd

 Section -AdditionalIcons
  SetOutPath $INSTDIR
  CreateDirectory "$SMPROGRAMS\eSim"
  CreateShortCut "$SMPROGRAMS\eSim\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall



  

  Delete "$INSTDIR\uninst.exe"
  ;Delete "$INSTDIR\eSim"
  

  Delete "$SMPROGRAMS\eSim\Uninstall.lnk"
  
  ${If} ${RunningX64}
    ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "C:\Program Files (x86)\KiCad\bin"
    
 ${Else}
    ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "C:\Program Files\KiCad\bin"
    
 ${EndIf}    
 
 ;Setting Env Variable for ngspice 
 ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "C:\spice\bin"

  RMDir "$SMPROGRAMS\eSim"
  ;RMDir "$INSTDIR\eSim"
  ;RMDir /r "$INSTDIR\"
  RMDir /r "$INSTDIR\eSim"
  Delete "$DESKTOP\eSim.lnk" 

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
 
 ;Descriptions

  ;Language strings
  ;LangString DESC_SecDummy ${LANG_ENGLISH} "Ngspice is a mixed-level/mixed-signal circuit simulator. Its code is based on three open source software packages: Spice3f5, Cider1b1 and Xspice. Ngspice is part of gEDA project, a full GPL'd suite of Electronic Design Automation tools."

  ;Assign language strings to sections
  ;!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
   ; !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
 ; !insertmacro MUI_FUNCTION_DESCRIPTION_END
 
;--------------------------------