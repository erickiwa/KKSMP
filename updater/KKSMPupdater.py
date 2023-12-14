import tkinter as tk
from tkinter import ttk
import requests
import zipfile
import os
import shutil
from PIL import Image, ImageTk
import sys

# Sim, eu gerei o código com auxilio do ChatGPT porque eu tenho nenhum conhecimento de Python.
# O código faz o seguinte, ele lê um link que coloquei num txt raw e esse link baixa o modpack
# Ao baixar ele descompacta, deleta as pastas e substitui pelas do arquivo compactado
# Se você tem sugestões abra um ticket e me fala, tudo que eu queria era arrumar esse código.

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def baixar_e_descompactar():
    url_raw = "https://raw.githubusercontent.com/ItsOnlyMe360/KKSMP/main/redirect.txt"

    response = requests.get(url_raw)
    raw_text = response.text

    url_file = raw_text.strip()

    response_file = requests.get(url_file)
    zip_filename = "mods.zip"

    with open(zip_filename, "wb") as zip_file:
        zip_file.write(response_file.content)

    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        total_files = len(zip_ref.namelist())
        extracted_files = 0

        for file in zip_ref.namelist():
            zip_ref.extract(file, "temp")
            extracted_files += 1

    minecraft_path = os.path.join(os.getcwd(), ".minecraft")

    if os.path.exists(minecraft_path):
        for folder in ["mods", "resourcepacks", "shaderpacks", "config", "MenuLayout"]:
            folder_path = os.path.join(minecraft_path, folder)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

        merge_folders("temp", minecraft_path)
    else:
        os.rename("temp", minecraft_path)

    os.remove(zip_filename)

    label_status.config(text="Atualização concluída!", foreground="white", background="#1F1F1F")

def merge_folders(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=True)
        else:
            shutil.copy(s, d)

root = tk.Tk()
root.title("KKSMP Updater")
root.resizable(False, False)
root.geometry("854x480")

bg_image = Image.open(resource_path("bg.png"))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

style = ttk.Style()
style.configure('TButton', padding=6, relief="flat", font=('Helvetica', 12))
style.configure('TLabel', font=('Helvetica', 12))

button_baixar = ttk.Button(root, text="Atualizar", command=baixar_e_descompactar, style='TButton')
button_baixar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

label_status = ttk.Label(root, text="", foreground="black", style='TLabel')
label_status.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

root.mainloop()
