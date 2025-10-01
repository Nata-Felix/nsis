; nsis_installer_silent.nsi - instala em modo invisível, fecha e inicia app

!define APP_NAME "MeuAppTeste"
!define EXE_NAME "app.exe"
!define APP_VERSION "1.1.0"
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"

OutFile "Setup_${APP_NAME}_${APP_VERSION}.exe"
InstallDir ${INSTALL_DIR}
SilentInstall silent
SilentUnInstall silent
AutoCloseWindow true
ShowInstDetails nevershow
ShowUninstDetails nevershow

Section "Instalar"
  nsExec::ExecToLog 'taskkill /F /IM ${EXE_NAME} /T'

  SetOutPath $INSTDIR
  File "dist\${EXE_NAME}"

  ; cria atalhos
  CreateShortcut "$SMPROGRAMS\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"

  ; escreve o desinstalador
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; inicia app e fecha instalador
  Exec "$INSTDIR\${EXE_NAME}"
  Quit
SectionEnd

Section "Uninstall"
  nsExec::ExecToLog 'taskkill /F /IM ${EXE_NAME} /T'
  Delete "$INSTDIR\${EXE_NAME}"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$SMPROGRAMS\${APP_NAME}.lnk"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  RMDir $INSTDIR
  Quit
SectionEnd
