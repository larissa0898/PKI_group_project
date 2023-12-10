import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk
from tkinter import messagebox

# Integration Funktionen Phil Balczukat
#import Phil.basic_features_lib

# Globale Variable für properties_label
properties_label = None

def show_help_dialog():
    help_dialog = tk.Toplevel(root)
    help_dialog.title("Hilfe")

    help_text = """
    Hier sind die Funktionen des Programms:

    1. Standardfunktionen:
       - Rotieren: Dreht das Bild um 90 Grad im Uhrzeigersinn.
       - Skalieren: Ändert die Größe des Bildes.
       - Spiegel horizontal: Spiegelt das Bild horizontal.
       - Spiegel vertikal: Spiegelt das Bild vertikal.
       - Ausschneiden: Schneidet einen Bereich aus dem Bild aus.
       - Rahmen hinzufügen: Fügt einen Rahmen um das Bild hinzu.

    2. Erweiterte Funktionen:
       - Funktion 1: Kurze Beschreibung der Funktion.
       - Funktion 2: Kurze Beschreibung der Funktion.
       - ...

    3. Bilderkennung und -transformation:
       - Funktion 1: Kurze Beschreibung der Funktion.
       - Funktion 2: Kurze Beschreibung der Funktion.
       - ...

    4. Video Features:
       - Funktion 1: Kurze Beschreibung der Funktion.
       - Funktion 2: Kurze Beschreibung der Funktion.
       - ...

    5. OCR Erkennung:
       - Funktion 1: Kurze Beschreibung der Funktion.
       - Funktion 2: Kurze Beschreibung der Funktion.
       - ...
    """
    help_label = tk.Label(help_dialog, text=help_text, justify='left')
    help_label.pack(padx=20, pady=20)

    close_button = tk.Button(help_dialog, text="Schließen", command=help_dialog.destroy)
    close_button.pack(pady=10)

def print_me():
    print(f"Datei: {file_path.get()}")

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def close_program():
    print("Programm wird geschlossen.")
    root.destroy()

def show_info_dialog():
    info_dialog = tk.Toplevel(root)
    info_dialog.title("BILDBEARBEITUNG UND BILDANALYSE")
    info_dialog.geometry("600x600")

    tk.Label(info_dialog, text="BILDBEARBEITUNG UND BILDANALYSE").pack()
    tk.Frame(info_dialog, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=5)
    tk.Label(info_dialog, text="Entwicklerteam Gruppe a1-1:").pack(pady=5)

    developers = ["Al-Atrash, Anas Abdelsaman Ramadan", "Balczukat, Phil", "Ferme, Larissa", "Koch, Claus-Peter",
                  "Ysop, Dietmar"]
    for developer in developers:
        tk.Label(info_dialog, text=developer).pack(pady=1)

    tk.Frame(info_dialog, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=5)

    center_window(info_dialog)

def show_version_dialog():
    version_dialog = tk.Toplevel(root)
    version_dialog.title("BILDBEARBEITUNG UND BILDANALYSE")
    version_dialog.geometry("280x160")
    tk.Label(version_dialog, text="BILDBEARBEITUNG UND BILDANALYSE").pack()
    tk.Frame(version_dialog, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=5)
    tk.Label(version_dialog, text="Programmversion 3.0").pack(pady=1)
    tk.Label(version_dialog, text="(c) 2024").pack(pady=3)

def save_file_callback():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        print(f"Datei speichern: {file_path}")

def save_file_as_callback():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        print(f"Datei speichern unter: {file_path}")
        # Hier könntest du die Logik für das Speichern des aktuellen Bildes an einem anderen Ort implementieren

#Funktion, um den Dateidialog zu öffnen und ein Bild zu laden
def show_file_dialog():
    file_types = [('JPEG Files', '*.jpg'), ('PNG Files', '*.png'), ('BMP Files', '*.bmp')]
    filename = filedialog.askopenfilename(filetypes=file_types)
    show_image(filename)

def show_image(image_path):
    original_image = cv2.imread(image_path)
    resized_image = cv2.resize(original_image,(495,600))

    # Konvertiere das Bild von BGR zu RGB (für die Anzeige in Tkinter)
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    tk_image = ImageTk.PhotoImage(Image.fromarray(rgb_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
    canvas.place(x=35, y=65)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Zeige Bildeigenschaften in einem Textfeld an
    properties_text = f"Dateipfad: {image_path}\n" \
                      f"Bildbreite: {original_image.shape[1]}\n" \
                      f"Bildhöhe: {original_image.shape[0]}"
    properties_label.config(text=properties_text)

    # Textfeld für Bildeigenschaften erstellen
    properties_label = tk.Label(root, text="")
    properties_label.place(x=30, y=60)

    # Halte das Tkinter-Fenster offen
    root.mainloop()

def reset_canvas():
    # Erstelle ein leeres Bild (weißer Hintergrund)
    empty_image = Image.new("RGB", (500, 500), "white")
    tk_empty_image = ImageTk.PhotoImage(empty_image)

    # Aktualisiere das Canvas mit dem leeren Bild
    canvas.itemconfig(image_item, image=tk_empty_image)

def print_to_pdf():
    try:
        global image_tk
        if image_tk:
            pdf = FPDF()
            pdf.add_page()
            pdf.image(ImageTk.getimage(image_tk), x=10, y=10, w=190)
            pdf.output("output.pdf")
    except NameError:
        print("Bild nicht gefunden.")

# Tkinter-App erstellen
root = tk.Tk()
root.title("BILDBEARBEITUNG UND BILDANALYSE")

# Hauptfenster in der Bildschirmmitte positionieren
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1300
window_height = 800
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Erstelle ein Canvas und platziere es auf dem Fenster
canvas = tk.Canvas(root, width=600, height=685, bd=2, relief="solid")
canvas.place(x=30, y=60)

# Menüleiste erstellen
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Datei öffnen", command=show_file_dialog)
file_menu.add_command(label="Datei speichern", command=save_file_callback)
file_menu.add_command(label="Datei speichern unter", command=save_file_as_callback)
file_menu.add_separator()
file_menu.add_command(label="Datei schließen", command=print_me)
file_menu.add_separator()
file_menu.add_command(label="PDF Drucken", command=print_to_pdf())
file_menu.add_separator()
file_menu.add_command(label="Eigenschaften", command=print_me)
file_menu.add_separator()
file_menu.add_command(label="Ende", command=close_program)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Reset / Default", command=print_me)

settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Standardeinstellungen", command=print_me)
settings_menu.add_command(label="Erweiterte Einstellungen", command=print_me)
settings_menu.add_command(label="Bildtransformation", command=print_me)
settings_menu.add_command(label="OCR und Video", command=print_me)

info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="Hilfe", command=show_help_dialog)
info_menu.add_command(label="Entwicklerteam", command=show_info_dialog)
info_menu.add_command(label="Programmversion", command=show_version_dialog)

menu_bar.add_cascade(label="Datei", menu=file_menu)
menu_bar.add_cascade(label="Bearbeiten", menu=edit_menu)
menu_bar.add_cascade(label="Einstellungen", menu=settings_menu)
menu_bar.add_cascade(label="Info", menu=info_menu)

root.config(menu=menu_bar)

# Button zum Zurücksetzen des Canvas hinzufügen
reset_button = tk.Button(root, text="Reset Canvas", command=reset_canvas)
reset_button.place(x=30,y=30)

# Bereich für Bedienungselemente
bedienung_frame = tk.Frame(root, width=300, height=800, bd=2, relief="solid", bg="#e4eee9")
bedienung_frame.place(x=700, y=30)

# Rahmen für die Standardfunktionen
standard_frame = tk.Frame(bedienung_frame, width=120, height=30, bd=1, relief="sunken", bg="#eeeee4")
standard_frame.pack(pady=0)
tk.Label(standard_frame, text='Standardfunktionen', bg="#eeeee4").pack()

# Bereitstellung der Buttons (Standard) und nebeneinander anordnen
buttons_frame = tk.Frame(standard_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Rotieren", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Skalieren", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Spiegel\n horizontal", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Spiegeln\n vertikal", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Ausschneiden", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Rahmen\n hinzufügen", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

# Erweiterte Funktionen
erweitert_frame = tk.Frame(bedienung_frame, width=120, height=30, bd=1, relief="sunken", bg="#eeeee4")
erweitert_frame.pack(pady=40)
tk.Label(erweitert_frame, text="Erweiterte Funktionen", bg="#eeeee4").pack()

# Bereitstellung der Buttons (Erweitert) und nebeneinander anordnen
buttons_frame = tk.Frame(erweitert_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Funktion 1", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 2", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 3", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 4", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 5", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 6", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

# Bereich für Bilderkennung und -transformation
bilderkennung_frame = tk.Frame(bedienung_frame, width=120, height=30, bd=1, relief="sunken", bg="#eeeee4")
bilderkennung_frame.pack(pady=40)
tk.Label(bilderkennung_frame, text="Bilderkennung und -transformation", bg="#eeeee4").pack()

# Bereitstellung der Buttons (Erweitert) und nebeneinander anordnen
buttons_frame = tk.Frame(bilderkennung_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Funktion 1", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 2", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 3", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 4", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 5", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 6", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

# Bereich für Video Features
video_frame = tk.Frame(bedienung_frame, width=120, height=30, bd=1, relief="sunken", bg="#eeeee4")
video_frame.pack(pady=40)
tk.Label(video_frame, text="Video Features", bg="#eeeee4").pack()

# Bereitstellung der Buttons (Erweitert) und nebeneinander anordnen
buttons_frame = tk.Frame(video_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Funktion 1", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 2", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 3", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 4", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 5", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 6", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

# Bereich für OCR Erkennung
OCR_frame = tk.Frame(bedienung_frame, width=120, height=30, bd=1, relief="sunken", bg="#eeeee4")
OCR_frame.pack(pady=40)
tk.Label(OCR_frame, text="OCR Erkennung", bg="#eeeee4").pack()

# Bereitstellung der Buttons (Erweitert) und nebeneinander anordnen
buttons_frame = tk.Frame(OCR_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Funktion 1", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 2", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 3", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 4", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 5", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Funktion 6", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

root.config(bg="#fdfdfc")
root.mainloop()
