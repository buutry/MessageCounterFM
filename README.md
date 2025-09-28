# MCFM – Message Counter For Messenger

MCFM is a Python script with a GUI that counts messages you have sent and received by analyzing `.json` files exported from Facebook Messenger.  
You need to download your conversation files from Facebook in `.json` format to use this tool.

---

## Features / Funkcje
- Counts total messages in a conversation / Liczy wszystkie wiadomości w rozmowie
- Shows messages sent by you and received from others / Pokazuje wiadomości wysłane przez Ciebie i otrzymane od innych
- Multi-language support: English and Polish / Obsługa języka angielskiego i polskiego
- Export your data to a `.txt` file / Eksport danych do pliku `.txt`
- Settings for folder selection, user name, and language / Ustawienia folderu, imienia i języka
- Built-in help button to contact support / Wbudowany przycisk pomocy do kontaktu z supportem

---

## Getting Started / Jak zacząć

### Prerequisites / Wymagania
- Python 3.10+ installed on your system / Python 3.10+ zainstalowany w systemie
- Required libraries: `tkinter`, `json` / Wymagane biblioteki `tkinter`, `json`

### Running the script / Uruchamianie skryptu
1. Download or clone this repository / Pobierz lub sklonuj repozytorium.
2. Make sure `gui.py` and `main.py` are in the same folder / Upewnij się, że `gui.py` i `main.py` są w tym samym folderze.
3. Open terminal/command prompt in the folder and run / Otwórz terminal w folderze i uruchom:

```bash
python gui.py
```
4. You can also just double click `main.py` / Możesz też podwójnie kliknąć `main.py`

### Using the EXE / Uruchamianie wersji EXE
- Make sure every file is in the same folder / Upewnij się że każdy plik jest w jednym folderze
- Install `PyInstaller` / Pobierz `PyInstaller`
  ```
  pip install pyinstaller
  ```

- Create MCFM.exe / Stwórz MCFM.exe
  ```
  cd "Directory of the folder"
  ```
  Then

  ```
  pyinstaller --onefile --windowed --name MCFM --icon=MCFM.ico main.py
  ```
  
  ### ANY TIPS OR QUESTIONS? CONTACT MCFMhelp@gmail.com
  
