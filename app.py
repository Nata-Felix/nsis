import requests
import os
import sys
import tempfile
import tkinter as tk
from tkinter import messagebox
import ctypes

# Definições de Versão (movidas de version.py)
APP_NAME = "MeuAppTeste"
APP_VERSION = "3.5.0" 
APP_AUTHOR = "Natã Silva"

# Configurações do GitHub para Atualização
GITHUB_REPO = "Nata-Felix/nsis"
ASSET_NAME_PREFIX = "Setup_"

# Variável para a janela principal (root)
root = None 


def is_newer_version(new_version, current_version):
    """
    Compara duas strings de versão (ex: "2.2.0") e retorna True se a nova for maior.
    """
    try:
        # Converte "2.2.0" em uma tupla de inteiros (2, 2, 0) para comparação
        new_parts = tuple(map(int, new_version.split('.')))
        current_parts = tuple(map(int, current_version.split('.')))
        
        # Compara as tuplas.
        return new_parts > current_parts
    except ValueError:
        # Em caso de erro de formato, faz comparação de string
        return new_version > current_version


def check_for_update():
    """
    Verifica a versão mais recente no GitHub e baixa/executa
    o instalador SE uma versão MAIS NOVA for encontrada.
    """
    global root
    
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        release = r.json()

        latest_version = release["tag_name"].lstrip("v")

        # Verifica se a versão do GitHub é superior à local
        if is_newer_version(latest_version, APP_VERSION):
            asset = next(
                (a for a in release["assets"] if a["name"].startswith(ASSET_NAME_PREFIX)),
                None
            )
            if not asset:
                messagebox.showinfo("Atualização", "Nova versão encontrada, mas instalador não disponível.")
                return

            download_url = asset["browser_download_url"]
            tmp_installer = os.path.join(tempfile.gettempdir(), asset["name"])

            # 1. Baixa o instalador NSIS
            messagebox.showinfo("Download", f"Baixando instalador da versão {latest_version}...")
            with requests.get(download_url, stream=True) as resp:
                resp.raise_for_status()
                with open(tmp_installer, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)

            # *** MENSAGEM SUPRIMIDA E SUBSTITUÍDA POR PRINT NO CONSOLE ***
            print(f"[INFO] Nova versão {latest_version} encontrada! Iniciando instalação silenciosa...")

            # 2. Executa o instalador com privilégios de administrador (UAC) e modo silencioso (/S)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", tmp_installer, "/S", None, 1
            )

            # 3. Encerra o app atual imediatamente
            if root:
                root.destroy()
            sys.exit(0)

        else:
            # Esta mensagem permanece para feedback de que nada foi feito
            messagebox.showinfo("Atualização", "Você já está na versão mais recente.")

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao verificar atualização:\n{e}")


def setup_gui():
    """
    Configura a interface gráfica com os botões.
    """
    global root
    
    # Cria a janela principal do Tkinter
    root = tk.Tk()
    root.title(f"{APP_NAME} - Versão {APP_VERSION}")
    
    # Rótulo de informações
    label = tk.Label(root, text=f"Aplicativo: {APP_NAME}\nVersão Atual: {APP_VERSION}\n\nClique para verificar atualizações.", padx=30, pady=20)
    label.pack(pady=10)

    # Botão para Procurar Atualização
    btn_update = tk.Button(root, text="Procurar Atualização", command=check_for_update)
    btn_update.pack(pady=5, ipadx=10, fill='x', padx=30)

    # Botão para Fechar
    btn_close = tk.Button(root, text="Fechar", command=root.destroy)
    btn_close.pack(pady=(5, 10), ipadx=10, fill='x', padx=30)
    
    # Inicia o ciclo de eventos do Tkinter
    root.mainloop()


# --- Início da Execução do Script ---
if __name__ == "__main__":
    setup_gui()