; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "OpenEIS"
#define MyAppVersion "2.5"
#define MyAppPublisher "Pacific Northwest National Laboratory"
#define MyAppURL "https://github.com/VOLTTRON/openeis/"

;--------------------------------------------------------------------
; CHANGE ME TO REAL DIR TO OPEN WITH INNO
; #define SrcRoot "c:\working_dir\data"
;--------------------------------------------------------------------
#define SrcRoot "~~WORKING_DIR~~"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{C1F3BDBD-D4C7-48BE-A0DA-8DA629AD9EDA}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=c:\{#MyAppName}-{#MyAppVersion}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#SrcRoot}\python\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs; Excludes: "*__pycache__*"
Source: "{#SrcRoot}\wheels\*"; DestDir: "{app}\wheels"; Flags: ignoreversion recursesubdirs; Excludes: "*__pycache__*"
; Source: "{#SrcRoot}\numpy\*"; DestDir: "{app}\python\Lib\site-packages"; Flags: ignoreversion recursesubdirs; Excludes: "*__pycache__*"
; Source: "{#SrcRoot}\openeis\*"; DestDir: "{app}\openeis"; Flags: ignoreversion recursesubdirs
Source: "{#SrcRoot}\misc\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs; Excludes: "*__pycache__*"

[Run]
Filename: "{app}\python\python.exe"; Parameters: "{app}\get-pip.py"
Filename: "{app}\python\Scripts\pip.exe"; Parameters: "install wheel"
Filename: "{app}\python\Scripts\pip.exe"; Parameters: "install --no-index --find-links={app}\wheels -r {app}\requirements.txt"
Filename: "{app}\python\Scripts\pip.exe"; Parameters: "install numpy --no-index --find-links={app}\wheels"
Filename: "{app}\python\Scripts\pip.exe"; Parameters: "install scipy --no-index --find-links={app}\wheels"
Filename: "{app}\python\Scripts\pip.exe"; Parameters: "install openeis-ui --no-index --find-links={app}\wheels --pre"
Filename: "{app}\python\Scripts\pip.exe"; Parameters: "install openeis --no-index --find-links={app}\wheels"

Filename: "{app}\start-openeis.bat"; Description: "Launch application"; Flags: postinstall nowait skipifsilent unchecked

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

