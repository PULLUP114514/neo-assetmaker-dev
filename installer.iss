; ArknightsPassMaker Installer

#define MyAppName "ArknightsPassMaker"
#define MyAppNameCN "明日方舟通行证素材工具箱"
#ifndef MyAppVersion
  #define MyAppVersion "2.1.0"
#endif
#define MyAppPublisher "Rafael-ban"
#define MyAppURL "https://github.com/rhodesepass/neo-assetmaker"
#define MyAppExeName "ArknightsPassMaker.exe"
#define MyAppIcon "resources\icons\favicon.ico"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppNameCN}
AppVersion={#MyAppVersion}
AppVerName={#MyAppNameCN} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\{#MyAppName}
DefaultGroupName={#MyAppNameCN}
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename={#MyAppName}_v{#MyAppVersion}_Setup
SetupIconFile={#MyAppIcon}
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
AppMutex=ArknightsPassMakerMutex
MinVersion=10.0
CloseApplications=yes
CloseApplicationsFilter=*.exe
WizardStyle=modern
WizardImageFile=resources\installer\wizard.bmp
WizardSmallImageFile=resources\installer\wizard_small.bmp
LicenseFile=resources\installer\LICENSE.txt
ShowLanguageDialog=no
Uninstallable=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppNameCN}

[Languages]
Name: "chinese"; MessagesFile: "resources\installer\ChineseSimplified.isl"

[Messages]
WelcomeLabel1=欢迎使用 明日方舟通行证素材工具箱
WelcomeLabel2=本程序将安装 [name/ver] 到您的计算机。%n%n点击"下一步"继续安装。
FinishedHeadingLabel=安装完成
FinishedLabel=明日方舟通行证素材工具箱 已成功安装到您的计算机。%n%n感谢您的使用！

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
; === 升级时清理旧版本应用文件 ===
; 在安装新文件之前执行 (Inno Setup: processed as the first step of installation)
; 用户数据目录 (config/, logs/, .recovery/) 不在此列表中，自动保留
;
; -- 应用子目录（整体删除后由新版本重新安装）--
Type: filesandordirs; Name: "{app}\lib"
Type: filesandordirs; Name: "{app}\resources"
Type: filesandordirs; Name: "{app}\simulator"
Type: filesandordirs; Name: "{app}\epass_flasher"
Type: filesandordirs; Name: "{app}\class_icons"
; -- 根目录下的二进制文件 --
Type: files; Name: "{app}\*.dll"
Type: files; Name: "{app}\*.exe"
Type: files; Name: "{app}\*.pyd"
; -- cx_Freeze 元数据 --
Type: files; Name: "{app}\frozen_modules.json"
; -- 旧的运行时日志（每次启动以 'w' 模式重新创建，见 main.py:22-33）--
Type: files; Name: "{app}\stdout.log"
Type: files; Name: "{app}\stderr.log"
Type: files; Name: "{app}\crash.log"

[Files]
Source: "ArknightsPassMaker\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppNameCN}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppNameCN}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppNameCN}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppNameCN, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
