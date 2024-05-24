\
; base.nsi

XPStyle on

Page license
Page directory
;Page components
Page instfiles

RequestExecutionLevel admin

LoadLanguageFile "${NSISDIR}\Contrib\Language files\English.nlf"
LoadLanguageFile "${NSISDIR}\Contrib\Language files\Spanish.nlf"

# set license page
LicenseText ""
LicenseData "license.txt"
LicenseForceSelection checkbox

; use the default string for the directory page.
DirText ""

Name "Hey, we are venom version 1.0.0.0"
OutFile "venom-1.0.0.0.exe"
;SetCompress off ; disable compression (testing)
SetCompressor /SOLID lzma
;InstallDir venom
InstallDir $PROGRAMFILES\venom

InstallDirRegKey HKLM "Software\venom" "Install_Dir"

VIProductVersion "1.0.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "venom"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Hey, we are venom version 1.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "https://github.com/Hanslettthedev"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "1.0.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "Copy whatever you want"
;VIAddVersionKey /LANG=${LANG_ENGLISH} "InternalName" "FileSetup.exe"

Section venom
    SectionIn RO
    SetOutPath $INSTDIR
    File /r dist\*.*
    IfFileExists $INSTDIR\\conf\\rece.ini 0 +3
        IfFileExists $INSTDIR\\rece.ini +2 0
        CopyFiles $INSTDIR\\conf\\rece.ini $INSTDIR\\rece.ini
    IfFileExists $INSTDIR\\conf\\reingart.crt 0 +3
        IfFileExists $INSTDIR\\reingart.crt +2 0
        CopyFiles $INSTDIR\\conf\\reingart.crt $INSTDIR\\reingart.crt
    IfFileExists $INSTDIR\\conf\\reingart.key 0 +3
        IfFileExists $INSTDIR\\reingart.key +2 0
        CopyFiles $INSTDIR\\conf\\reingart.key $INSTDIR\\reingart.key
    WriteRegStr HKLM SOFTWARE\venom "Install_Dir" "$INSTDIR"
    ; Write the uninstall keys for Windows
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\venom" "DisplayName" "Hey, we are venom version 1.0.0.0 (solo eliminar)"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\venom" "UninstallString" "$INSTDIR\Uninst.exe"
    WriteUninstaller "Uninst.exe"
    ;create start-menu items
    IfFileExists $INSTDIR\\pyrece.exe 0 +4
        CreateDirectory "$SMPROGRAMS\venom"
        CreateShortCut "$SMPROGRAMS\venom\PyRece.lnk" "$INSTDIR\pyrece.exe" "" "$INSTDIR\pyrece.exe" 0
        CreateShortCut "$SMPROGRAMS\venom\Designer.lnk" "$INSTDIR\designer.exe" "" "$INSTDIR\designer.exe" 0
        ;CreateShortCut "$SMPROGRAMS\venom\Uninstall.lnk" "$INSTDIR\Uninst.exe" "" "$INSTDIR\Uninst.exe" 0
    IfFileExists $INSTDIR\\factura.exe 0 +3
        CreateDirectory "$SMPROGRAMS\venom"
        CreateShortCut "$SMPROGRAMS\venom\PyFactura.lnk" "$INSTDIR\factura.exe" "" "$INSTDIR\factura.exe" 0
  
SectionEnd

Section "Uninstall"
    ;Delete Files

    ;Delete Uninstaller And Unistall Registry Entries
    Delete "$INSTDIR\Uninst.exe"
    DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\venom"
    DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\venom"

SectionEnd

;--------------------------------

Function .onInit

    IfSilent nolangdialog

    ;Language selection dialog

    Push ""
    Push ${LANG_ENGLISH}
    Push English
    Push ${LANG_SPANISH}
    Push Spanish
    Push A ; A means auto count languages
           ; for the auto count to work the first empty push (Push "") must remain
    LangDLL::LangDialog "Installer Language" "Please select the language of the installer"

    Pop $LANGUAGE
    StrCmp $LANGUAGE "cancel" 0 +2
        Abort
        
nolangdialog:
        
FunctionEnd

