import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk
from tkinter import messagebox
from Claus_und_Larissa.Claus.Gesichtswiederkennung.Gesichtswiedererkennung import Gesichtswiedererkennung
from Claus_und_Larissa.Claus.Gesichtswiederkennung.Gesichtswiedererkennung import Gesichtswiedererkennung_Trainieren
from Claus_und_Larissa.Claus.Gesichtswiederkennung.Gesichtswiedererkennung import Lade_TrainiertesModell
import json
from pathlib import Path

# Integration Funktionen Phil Balczukat
#import Phil.basic_features_lib

# Variablen für Bildeigenschaften global definieren
label_Bildbreite = None
label_Bildhöhe = None
label_Dateipfad = None

#Erzeugt eine Messagebox, um eine kurze Übersicht zu den Funktionen anzuzeigen
def show_help_dialog():
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

    5. OCR Funktionen:
       - Funktion 1: Kurze Beschreibung der Funktion.
       - Funktion 2: Kurze Beschreibung der Funktion.
       - ...
    """
    messagebox.showinfo("Hilfe", help_text)

#Erzeugt eine Messagebox, um Auskunft über das Entwicklerteam zu geben
def show_info_dialog():
    message = "Entwicklerteam Gruppe a1-1:\n\n" + "\n".join([
        "Al-Atrash, Anas Abdelsaman Ramadan",
        "Balczukat, Phil",
        "Ferme, Larissa",
        "Koch, Claus-Peter",
        "Ysop, Dietmar"
    ])
    messagebox.showinfo("BILDBEARBEITUNG UND BILDANALYSE", message)

#Erzeugt eine Messagebox, um Auskunft über die Programmversion zu geben
def show_version_dialog():
    version_text = """
    BILDBEARBEITUNG UND BILDANALYSE

    Programmversion 3.0
    (c) 2024
    """
    messagebox.showinfo("Version", version_text)

def resize_image(image, max_width, max_height):
    '''Funktion skaliert das Bild auf eine max.Breite oder Höhe, ohne das Format zu ändern
    1:1 aus ChatGPT 3.5'''
    # Get the original image dimensions
    height, width = image.shape[:2]

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Calculate new dimensions while maintaining aspect ratio
    new_width = min(width, max_width)
    new_height = int(new_width / aspect_ratio)

    # If the calculated height exceeds the maximum height, recalculate dimensions
    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image

def FaceRecognitionTraining():
    '''Funktion zur Wiedererkennung von Personen im Bild, basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''
    try:
        # Laden der trainierten Label Daten aus einer JSON Datei
        file_path_training = filedialog.askdirectory(title="Speicherordner Trainingsdaten")
        print("Ordner Trainingsdaten:", file_path_training)

        # Dateipfad für die Speicherung des Modells wählen
        file_path_save = filedialog.askdirectory(title="Speicherort für trainiertes Datenmodell")
        print("Speicherordner:", file_path_save)

        Gesichtswiedererkennung_Trainieren(file_path_training,file_path_save)

        print("Training durchgeführt")

    except Exception as err_face_recognition_training:
        print("Error Face Recognition Training: ", err_face_recognition_training)

def FaceRecognition():
    '''Funktion zur Wiedererkennung von Personen im Bild, basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''
    try:
        # Laden der trainierten Label und Modell Daten aus einer JSON und XML Datei
        file_path = filedialog.askdirectory(title="Pfad der vortrainierten Daten (Verzeichnis) wählen")
        print("Selected Folder:", file_path)
        trained_recognizer, label_map_load = Lade_TrainiertesModell(file_path)

        # Test mit bekannten Bildern auf Basis der bekannten Gesichtsdatenbank
         test_image_path = filedialog.askopenfilename(title="Bild mit Gesichtern auswählen")
        #file_path+r"/search/ElonMusk_Gruppe.jpg"
        img = Gesichtswiedererkennung(trained_recognizer, test_image_path, label_map_load)
        show_image_live(img)

    except Exception as err_face_recognition:
        print("Error Face Recognition: ", err_face_recognition)


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

#Funktion, um den Dateidialog zu öffnen und ein Bild zu laden
def show_file_dialog():
    file_types = [('JPEG Files', '*.jpg'), ('PNG Files', '*.png'), ('BMP Files', '*.bmp')]
    filename = filedialog.askopenfilename(filetypes=file_types)
    show_image(filename)

#Funktion zum Anzeigen des live verarbeiten Bildes, ohne speichern
def show_image_live(image):
    #original_image = cv2.imread(image_path)
    #resized_image = cv2.resize(image, (495, 600))
    resized_image = resize_image(image, 595, 800)
    # Konvertiere das Bild von BGR zu RGB (für die Anzeige in Tkinter)
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    tk_image = ImageTk.PhotoImage(Image.fromarray(rgb_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
    canvas.place(x=35, y=65)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Halte das Tkinter-Fenster offen
    root.mainloop()

#Funktion um das ausgewählte Bild zu laden und die Dateieigenschaften zuzuweisen
def show_image(image_path):
    original_image = cv2.imread(image_path)
    resized_image = cv2.resize(original_image, (495, 600))

    # Konvertiere das Bild von BGR zu RGB (für die Anzeige in Tkinter)
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    tk_image = ImageTk.PhotoImage(Image.fromarray(rgb_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
    canvas.place(x=35, y=65)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Zeige Bildeigenschaften in den globalen Label-Variablen an
    label_Bildbreite = original_image.shape[1]
    label_Bildhöhe = original_image.shape[0]
    label_Dateipfad = image_path

    # Zeige Bildeigenschaften in den globalen Label-Variablen an
    anzeigen_Bildbreite.config(text=f"Bildbreite: {label_Bildbreite:,} Pixel")
    anzeigen_Bildhöhe.config(text=f"Bildhöhe: {label_Bildhöhe:,} Pixel")
    anzeigen_Dateipfad.config(text=f"Dateipfad: {label_Dateipfad.replace(',', '.')}")

    # Halte das Tkinter-Fenster offen
    root.mainloop()

#Funktion, um speichern aufzurufen
def save_file_callback():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        print(f"Datei speichern: {file_path}")

#Funktion, um speichern unter aufzurufen
def save_file_as_callback():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        print(f"Datei speichern unter: {file_path}")

#Funktion, um das Programm zu schließen
def close_program():
    print("Programm wird geschlossen.")
    root.destroy()

def reset_canvas():
    # Lösche alle Elemente im Canvas
    canvas.delete("all")

def print_to_pdf():
    pass

# Tkinter-App erstellen
root = tk.Tk()
root.title("BILDBEARBEITUNG UND BILDANALYSE")

# Hauptfenster in der Bildschirmmitte positionieren
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1280
window_height = 800
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Erstelle ein Canvas und platziere es auf dem Fenster
canvas = tk.Canvas(root, width=600, height=650, bd=2, relief="solid")
canvas.place(x=30, y=60)

# Menüleiste erstellen
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Datei öffnen", command=show_file_dialog)
file_menu.add_command(label="Datei speichern", command=save_file_callback)
file_menu.add_command(label="Datei speichern unter", command=save_file_as_callback)
file_menu.add_separator()
file_menu.add_command(label="PDF Drucken", command=print_to_pdf())
file_menu.add_separator()
file_menu.add_command(label="Ende", command=close_program)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Default Werte", command=print_me)

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

# Dateieigenschaften anzeigen
anzeigen_Bildbreite = tk.Label(root, text=label_Bildbreite, bg="#e4eee9")
anzeigen_Bildbreite.place(x=150, y=33)

anzeigen_Bildhöhe = tk.Label(root, text=label_Bildbreite, bg="#e4eee9")
anzeigen_Bildhöhe.place(x=300, y=33)

anzeigen_Dateipfad = tk.Label(root, text=label_Dateipfad, bg="#e4eee9")
anzeigen_Dateipfad.place(x=30, y=725)

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
tk.Button(buttons_frame, text="Markup", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Weich-\n zeichner", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Licht\n Schatten", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Texteffekte", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Farbeffekte", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Filter", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

# Bereich für Bilderkennung und -transformation
bilderkennung_frame = tk.Frame(bedienung_frame, width=120, height=30, bd=1, relief="sunken", bg="#eeeee4")
bilderkennung_frame.pack(pady=40)
tk.Label(bilderkennung_frame, text="Bilderkennung und -transformation", bg="#eeeee4").pack()

# Bereitstellung der Buttons (Erweitert) und nebeneinander anordnen
buttons_frame = tk.Frame(bilderkennung_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Gesichts-\nwiedererk.", command=FaceRecognition, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Gesichts-\nwiederk.\nTraining", command=FaceRecognitionTraining, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
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
tk.Label(OCR_frame, text="OCR Funktionen", bg="#eeeee4").pack()

# Bereitstellung der Buttons (Erweitert) und nebeneinander anordnen
buttons_frame = tk.Frame(OCR_frame)
buttons_frame.pack()
tk.Button(buttons_frame, text="Text-\n erkennung", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Text\n to speech", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Text\n to pdf", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Sprach-\n erkennung", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Dummy", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)
tk.Button(buttons_frame, text="Dummy", command=print_me, width=10, height=3, bg="#e4e4ee").pack(side="left", padx=5)

root.config(bg="#fdfdfc")
root.mainloop()