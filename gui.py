import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

CONFIG_FILE = "config1.json"

def loadConfig():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def saveConfig(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

config = loadConfig()
MY_NAME = config.get("myName", None)
FOLDER_PATH = config.get("folderPath", None)
LANGUAGE = config.get("language", "English")

TEXTS = {
    "English": {
        "folder_label": "Folder with JSON files:",
        "select_folder": "Select Folder",
        "your_name": "Your name:",
        "update_name": "Apply",
        "updated_name": "Settings updated",
        "settings_title": "Settings",
        "language_label": "Language:",
        "name_col": "Name",
        "sent_col": "Sent",
        "received_col": "Received",
        "export_button": "Export",
        "help_button": "Help"
    },
    "Polski": {
        "folder_label": "Folder z plikami JSON:",
        "select_folder": "Wybierz folder",
        "your_name": "Twoje imię:",
        "update_name": "Zastosuj",
        "updated_name": "Ustawienia zapisane",
        "settings_title": "Ustawienia",
        "language_label": "Język:",
        "name_col": "Imię",
        "sent_col": "Wysłane",
        "received_col": "Otrzymane",
        "export_button": "Eksportuj",
        "help_button": "Pomoc"
    }
}

def countMessagesInFolder(folderPath, myName):
    messagesCount = {}
    for fileName in os.listdir(folderPath):
        if fileName.endswith(".json"):
            with open(os.path.join(folderPath, fileName), "r", encoding="utf-8") as f:
                data = json.load(f)
                participants = [p for p in data.get("participants", []) if p != myName]
                messages = data.get("messages", [])
                for msg in messages:
                    sender = msg.get("senderName", "Unknown")
                    if sender == myName:
                        for recipient in participants:
                            if recipient not in messagesCount:
                                messagesCount[recipient] = {'sent':0,'received':0}
                            messagesCount[recipient]['sent'] += 1
                    else:
                        if sender not in messagesCount:
                            messagesCount[sender] = {'sent':0,'received':0}
                        messagesCount[sender]['received'] += 1
    return messagesCount

def refreshTable():
    if not FOLDER_PATH or not MY_NAME:
        return
    messagesCount = countMessagesInFolder(FOLDER_PATH, MY_NAME)
    for row in tree.get_children():
        tree.delete(row)
    for person, counts in messagesCount.items():
        tree.insert("", "end", values=(person, counts['sent'], counts['received']))

def openSettings():
    global MY_NAME, FOLDER_PATH, LANGUAGE, config
    settingsWindow = tk.Toplevel(root)
    settingsWindow.title(TEXTS[LANGUAGE]["settings_title"])
    settingsWindow.geometry("350x320")
    settingsWindow.resizable(False, False)
    settingsWindow.configure(bg="black")
    frame_settings = tk.Frame(settingsWindow, bg="white", bd=2, relief="solid")
    frame_settings.place(x=10, y=10, width=330, height=300)
    tk.Label(frame_settings, text=TEXTS[LANGUAGE]["folder_label"], bg="white", fg="black").pack(pady=5)
    folderLabel = tk.Label(frame_settings, text=FOLDER_PATH if FOLDER_PATH else "No folder selected", wraplength=300, bg="white", fg="black")
    folderLabel.pack(pady=5)
    def chooseFolder():
        global FOLDER_PATH
        folder = filedialog.askdirectory()
        if folder:
            FOLDER_PATH = folder
            folderLabel.config(text=FOLDER_PATH)
    tk.Button(frame_settings, text=TEXTS[LANGUAGE]["select_folder"], command=chooseFolder).pack(pady=5)
    tk.Label(frame_settings, text=TEXTS[LANGUAGE]["your_name"] + (" (exactly as in Messenger)" if LANGUAGE=="English" else " (dokładnie tak jak w Messengerze)"), bg="white", fg="black").pack(pady=10)
    nameEntry = tk.Entry(frame_settings)
    nameEntry.pack(pady=5)
    if MY_NAME:
        nameEntry.insert(0, MY_NAME)
    tk.Label(frame_settings, text=TEXTS[LANGUAGE]["language_label"], bg="white", fg="black").pack(pady=5)
    languageCombo = ttk.Combobox(frame_settings, values=["English","Polski"], state="readonly")
    languageCombo.pack(pady=5)
    languageCombo.set(LANGUAGE)
    def applySettings():
        global MY_NAME, LANGUAGE, config
        MY_NAME = nameEntry.get()
        LANGUAGE = languageCombo.get()
        config["myName"] = MY_NAME
        config["language"] = LANGUAGE
        config["folderPath"] = FOLDER_PATH
        saveConfig(config)
        tree.heading("Name", text=TEXTS[LANGUAGE]["name_col"])
        tree.heading("Sent", text=TEXTS[LANGUAGE]["sent_col"])
        tree.heading("Received", text=TEXTS[LANGUAGE]["received_col"])
        exportButton.config(text=TEXTS[LANGUAGE]["export_button"])
        helpButton.config(text=TEXTS[LANGUAGE]["help_button"])
        messagebox.showinfo("Info", TEXTS[LANGUAGE]["updated_name"])
        refreshTable()
    tk.Button(frame_settings, text=TEXTS[LANGUAGE]["update_name"], command=applySettings).pack(pady=15)

def exportData():
    if not FOLDER_PATH or not MY_NAME:
        messagebox.showwarning("Warning","Folder or name not set")
        return
    messagesCount = countMessagesInFolder(FOLDER_PATH, MY_NAME)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
    if file_path:
        with open(file_path,"w",encoding="utf-8") as f:
            f.write(f"{TEXTS[LANGUAGE]['name_col']}\t{TEXTS[LANGUAGE]['sent_col']}\t{TEXTS[LANGUAGE]['received_col']}\n")
            for person, counts in messagesCount.items():
                f.write(f"{person}\t{counts['sent']}\t{counts['received']}\n")
        messagebox.showinfo("Info", f"Data exported to {file_path}")

def openHelp():
    webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=MCFMhelp@gmail.com")

def run():
    global root, tree, exportButton, helpButton
    root = tk.Tk()
    root.title("MCFM")
    root.geometry("500x800+10+10")
    root.resizable(False, False)
    root.configure(bg="white")
    try:
        root.iconbitmap("MCFM.ico")
    except:
        pass
    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
    style.configure("Treeview.Heading", font=('Arial',12,'bold'), background="white", foreground='black')
    style.layout("Treeview",[('Treeview.treearea',{'sticky':'nswe'})])
    frame_table = tk.Frame(root, bg="black", bd=2)
    frame_table.place(x=20, y=60, width=460, height=700)
    tree = ttk.Treeview(frame_table, columns=("Name","Sent","Received"), show="headings")
    tree.heading("Name", text=TEXTS[LANGUAGE]["name_col"])
    tree.heading("Sent", text=TEXTS[LANGUAGE]["sent_col"])
    tree.heading("Received", text=TEXTS[LANGUAGE]["received_col"])
    tree.column("Name", width=200, anchor="w")
    tree.column("Sent", width=80, anchor="center")
    tree.column("Received", width=80, anchor="center")
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    gearButton = tk.Button(root, text="⚙️", command=openSettings)
    gearButton.place(x=10, y=10, width=40, height=40)
    exportButton = tk.Button(root, text=TEXTS[LANGUAGE]["export_button"], command=exportData)
    exportButton.place(x=60, y=10, width=80, height=40)
    helpButton = tk.Button(root, text=TEXTS[LANGUAGE]["help_button"], command=openHelp)
    helpButton.place(x=150, y=10, width=60, height=40)
    refreshTable()
    root.mainloop()
