import tkinter as tk
from version import APP_NAME, APP_VERSION

def main():
    root = tk.Tk()
    root.title(APP_NAME)

    label = tk.Label(root, text=f"{APP_NAME}\nVersão: {APP_VERSION}", font=("Arial", 14))
    label.pack(padx=20, pady=20)

    btn = tk.Button(root, text="Fechar", command=root.destroy)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
