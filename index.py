import os


nsi_base_script = r"""\
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

Name "%(description)s"
OutFile "%(out_file)s"
;SetCompress off ; disable compression (testing)
SetCompressor /SOLID lzma
;InstallDir %(install_dir)s
InstallDir $PROGRAMFILES\%(install_dir)s

InstallDirRegKey HKLM "Software\%(reg_key)s" "Install_Dir"

VIProductVersion "%(product_version)s"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "%(name)s"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "%(description)s"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "%(company_name)s"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "%(product_version)s"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "%(copyright)s"
;VIAddVersionKey /LANG=${LANG_ENGLISH} "InternalName" "FileSetup.exe"

Section %(name)s
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
    WriteRegStr HKLM SOFTWARE\%(reg_key)s "Install_Dir" "$INSTDIR"
    ; Write the uninstall keys for Windows
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(reg_key)s" "DisplayName" "%(description)s (solo eliminar)"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(reg_key)s" "UninstallString" "$INSTDIR\Uninst.exe"
    WriteUninstaller "Uninst.exe"
    ;create start-menu items
    IfFileExists $INSTDIR\\pyrece.exe 0 +4
        CreateDirectory "$SMPROGRAMS\%(name)s"
        CreateShortCut "$SMPROGRAMS\%(name)s\PyRece.lnk" "$INSTDIR\pyrece.exe" "" "$INSTDIR\pyrece.exe" 0
        CreateShortCut "$SMPROGRAMS\%(name)s\Designer.lnk" "$INSTDIR\designer.exe" "" "$INSTDIR\designer.exe" 0
        ;CreateShortCut "$SMPROGRAMS\%(name)s\Uninstall.lnk" "$INSTDIR\Uninst.exe" "" "$INSTDIR\Uninst.exe" 0
    IfFileExists $INSTDIR\\factura.exe 0 +3
        CreateDirectory "$SMPROGRAMS\%(name)s"
        CreateShortCut "$SMPROGRAMS\%(name)s\PyFactura.lnk" "$INSTDIR\factura.exe" "" "$INSTDIR\factura.exe" 0
  
SectionEnd

Section "Uninstall"
    ;Delete Files

    ;Delete Uninstaller And Unistall Registry Entries
    Delete "$INSTDIR\Uninst.exe"
    DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\%(reg_key)s"
    DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%(reg_key)s"

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

"""


metadata:dict = {
    "name": "venom",
    "description": "Hey, we are venom",
    "version": "1.0.0.0",
    "copyright": "Copy whatever you want",
    "url": "https://github.com/Hanslettthedev"
}


class NSISScript(object):
    def __init__(self, metadata, dist_dir):
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = metadata.get("name")
        self.description = metadata.get("description")
        self.version = metadata.get("version")
        self.copyright = metadata.get("copyright")
        self.url = metadata.get("url")

    def create(self, pathname="base.nsi"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        ver = self.version
        if "-" in ver:
            ver = ver[: ver.index("-")]
        rev = self.version.endswith("-full") and ".1" or ".0"
        ver = [c in "0123456789." and c or ".%s" % (ord(c) - 96) for c in ver] + [rev]
        ofi.write(
            nsi_base_script
            % {
                "name": self.name,
                "description": "%s version %s" % (self.description, self.version),
                "product_version": "".join(ver),
                "company_name": self.url,
                "copyright": self.copyright,
                "install_dir": self.name,
                "reg_key": self.name,
                "out_file": "%s-%s.exe"
                % (
                    self.name,
                    self.version
                    if len(self.version) < 128
                    else (self.version[:14] + self.version[-5:]),
                ),
            }
        )

    def compile(self, pathname="base.nsi"):
        os.startfile(pathname, "compile")



# create the Installer, using the files py2exe has created.
script = NSISScript(metadata, "./dist")
print("*** creating the nsis script***")
script.create()
print("*** compiling the nsis script***")
script.compile()
