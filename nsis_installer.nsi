!define APP_NAME "MeuAppTeste"
!define EXE_NAME "app.exe"
!define APP_VERSION "3.5.0"
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"

Name "${APP_NAME} v${APP_VERSION}"
OutFile "Setup_${APP_NAME}_v${APP_VERSION}.exe"
InstallDir ${INSTALL_DIR}
; *** ALTERAÇÃO AQUI: Fecha a janela do instalador automaticamente ***
AutoCloseWindow true
ShowInstDetails show
ShowUninstDetails show
RequestExecutionLevel admin

Section "Instalar Aplicação"
    DetailPrint "Encerrando instância de ${EXE_NAME}..."
    nsExec::ExecToLog 'taskkill /IM ${EXE_NAME} /F /T'
    Sleep 3000

    DetailPrint "Limpando diretórios temporários _MEI..."
    RMDir /r "$TEMP\_MEI*"

    DetailPrint "Instalando arquivos..."
    SetOutPath $INSTDIR
    File "dist\${EXE_NAME}"

    DetailPrint "Criando atalhos..."
    CreateShortcut "$SMSTARTUP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "--tray"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"

    WriteUninstaller "$INSTDIR\Uninstall.exe"

    DetailPrint "Iniciando aplicação..."
    ; Executa o aplicativo instalado
    Exec "$INSTDIR\${EXE_NAME}" 

    DetailPrint "Instalação concluída." 
SectionEnd

Section "Uninstall"
    DetailPrint "Encerrando instância de ${EXE_NAME}..."
    nsExec::ExecToLog 'taskkill /IM ${EXE_NAME} /F /T'
    Sleep 2000

    DetailPrint "Removendo atalhos e arquivos..."
    Delete "$SMSTARTUP\${APP_NAME}.lnk"
    Delete "$INSTDIR\${EXE_NAME}"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$SMPROGRAMS\${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir $INSTDIR

    DetailPrint "Desinstalação concluída."
SectionEnd