# Import allgemeiner Bibliotheken
import tkinter as tk
import cv2
import numpy as np
import customtkinter

from PIL import Image, ImageTk
from tkinter import filedialog, ttk, DISABLED, NORMAL
from CTkColorPicker import *

# Import Standardfunktionen-Modul
import standardfunktionen

# Import erweiterte Funktionen-Modul
import erweiterte_Funktionen

# Import Funktionen Menupunkt Bearbeiten
import allg_Funktionen

#Import Funktionen Menupunkt Einstellungen
import einstellungen

# Import Funktionen Menupunkt Info
import info

# Import OCR-Funktionen
import ocr

# Import Objekt-/Gesichtserkennungsfunktionen
import objekterkennung
import gesichtswiedererkennung
import selfie

# Variablen für Bildeigenschaften global definieren
label_Bildbreite = None
label_Bildhoehe = None
label_Dateipfad = None
anzeigen_Bildbreite = None
anzeigen_Bildhoehe = None
anzeigen_Dateipfad = None

#Globale Variablen und Konstanten
original_image = None # original image object opencv
original_image_path = None #path of original image
original_image_copy = None #copy of original image to enable a reset
resized_image = None # image resized (just for GUI view)
rgb_image = None #image in RGB converted
tk_image = None # tkinter visual object
file_types = [('JPEG Files', '*.jpg'), ('PNG Files', '*.png'), ('BMP Files', '*.bmp')]

# Variables
MAX_IMAGE_WIDTH = 495
MAX_IMAGE_HEIGHT = 580
canvas = None

#Funktion, um das Programm zu schließen
def close_program():
    root.destroy()

#Positioniert das Hauptfenster mittig vom Bildschirm
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Funktion, um den Dateidialog zu öffnen und ein Bild zu laden
def show_file_dialog():
    global original_image_path
    img = None
    try:
        # Filedialog zum Bildöffnen starten
        original_image_path = filedialog.askopenfilename(filetypes=file_types)

        # Bild mittels openCV einlesen
        img = cv2.imread(str(original_image_path))
        print("Datei:", str(original_image_path), "geladen.")
        disable_buttons(new_img = True)

        # Bild-Anzeige initiieren
        show_image(img)
    except Exception as exc:
        print("Keine Datei geladen: ",exc)
    return(img)

def resize_image(image, max_width, max_height):
    '''Funktion skaliert das Bild auf eine max.Breite oder Höhe, ohne das Format zu ändern
    1:1 aus ChatGPT 3.5'''
    # Extrahiere Breite und Höhe
    height, width = image.shape[:2]

    # Seitenverhältnis berechnen
    aspect_ratio = width / height

    # Neue Bilddimensionen gemäß Seitenverhältnis berechnen
    new_width = min(width, max_width)
    new_height = int(new_width / aspect_ratio)

    # Wenn neue Bilddimensionen größer sind als max. Canvas-Größe --> Neu berechnen
    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    # Größenanpassung des Bildes
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image

#Funktion zum Anzeigen des live verarbeiten Bildes, ohne speichern
def show_image_live(image):
    global original_image
    global resized_image
    global rgb_image #OpenCV konvertiertes Bild - Speichern (Originalgröße)
    global tk_image #Ausgabebild

    # Aktualisiere rgb_image-Objekt
    rgb_image = image

    # Bild auf Canvas-Größe skalieren (nur für die Ansicht)
    resized_image = resize_image(rgb_image, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT)

    # Update Größe und Breite:
    global anzeigen_Bildhoehe
    global anzeigen_Bildbreite
    label_Bildbreite = rgb_image.shape[1]
    label_Bildhoehe = rgb_image.shape[0]
    if anzeigen_Bildbreite:
        anzeigen_Bildbreite.configure(text=f'Breite: {label_Bildbreite}')

    if anzeigen_Bildhoehe:
        anzeigen_Bildhoehe.configure(text=f'Höhe: {label_Bildhoehe}')

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    tk_image = ImageTk.PhotoImage(Image.fromarray(resized_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    global canvas
    canvas.config(width=tk_image.width(), height=tk_image.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas_list.append(canvas)

    # Halte das Tkinter-Fenster offen
    root.mainloop()

def show_image(image):
    global original_image
    global original_image_copy
    global resized_image
    global rgb_image
    global tk_image
    global anzeigen_Dateipfad
    global anzeigen_Bildbreite
    global anzeigen_Bildhoehe

    # Speichere Originalbild für Reset-Funktion
    original_image_copy = image
    original_image = original_image_copy

    # Konvertiere das Bild von BGR zu RGB (für die Anzeige in Tkinter)
    rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Skalierung des Bildes für die Anzeige in GUI
    resized_image = resize_image(rgb_image, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT)

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    tk_image = ImageTk.PhotoImage(Image.fromarray(resized_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    global canvas
    # Canvas erzeugen, wenn noch nicht existiert.
    if canvas is None:
        canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
        canvas.pack()
        canvas.place(x=35, y=65)
    # Wenn Canvas schon existiert, nur  Größe ändern
    else:
        canvas.config(width=tk_image.width(), height=tk_image.height())

    # Bild mit Canvas verknüpfen
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Füge das Canvas-Objekt zu einer Liste hinzu
    canvas_list.append(canvas)

    # Zeige Bildeigenschaften in den globalen Label-Variablen an
    label_Bildbreite = original_image.shape[1]
    label_Bildhoehe = original_image.shape[0]
    label_Dateipfad = original_image_path  # image_path

    # Finde den Index des letzten Slashes in der Variable Dateipfad
    last_slash_index = label_Dateipfad.rfind("/")

    # Überprüfe, ob der Text länger als 50 Zeichen ist
    if len(label_Dateipfad) > 50:
        # Suche nach einem Backslash ab dem 50. Zeichen
        index_of_backslash = label_Dateipfad.find("/", 50)

        # Überprüfe, ob ein Backslash gefunden wurde
        if index_of_backslash != -1:
            # Teile den Text in zwei Teile, basierend auf dem gefundenen Backslash
            erster_teil = label_Dateipfad[:index_of_backslash + 1]
            zweiter_teil = label_Dateipfad[index_of_backslash + 1:]

            # Kombiniere die Teile mit einem Zeilenumbruch
            neuer_text = f"{erster_teil}\n{zweiter_teil}"
        else:
            # Wenn kein Backslash gefunden wurde, bleibe beim ursprünglichen Text
            neuer_text = label_Dateipfad
    else:
        # Wenn der Text nicht länger als 50 Zeichen ist, bleibe beim ursprünglichen Text
        neuer_text = label_Dateipfad

    # Zeige Bildeigenschaften in den globalen Label-Variablen an
    # Dateieigenschaften anzeigen
    if anzeigen_Bildbreite:
        anzeigen_Bildbreite.destroy()
    anzeigen_Bildbreite = customtkinter.CTkLabel(root, text=f'Breite: {label_Bildbreite}', fg_color="transparent", text_color="yellow")
    anzeigen_Bildbreite.place(x=150, y=20)

    if anzeigen_Bildhoehe:
        anzeigen_Bildhoehe.destroy()
    anzeigen_Bildhoehe = customtkinter.CTkLabel(root, text=f'Höhe: {label_Bildhoehe}', fg_color="transparent", text_color="yellow")
    anzeigen_Bildhoehe.place(x=250, y=20)

    if anzeigen_Dateipfad:
        anzeigen_Dateipfad.destroy()

    anzeigen_Dateipfad = customtkinter.CTkLabel(root, text=f"Dateipfad: {neuer_text}", fg_color="transparent", text_color="yellow")
    anzeigen_Dateipfad.place(x=30, y=680)

    # Halte das Tkinter-Fenster offen
    root.mainloop()

#########################################################################
#Hilfsfunktionen für die Multi-Bilder Suche nach bestimmten Objekten

#Funktion zum Öffnen eines Auswahldialogs
def select_object():
    # Create a new tkinter window
    select_window = tk.Toplevel()
    select_window.title("Objekt auswählen")

    # Create a label
    label = tk.Label(select_window, text="Suche Objekt:")
    label.pack(padx=10, pady=10)

    # Create a combobox (dropdown) widget
    selected_object = tk.StringVar()
    object_list = objekterkennung.get_Suchoptionen()  # Lade die Liste verfügbarer Optionen
    combobox = ttk.Combobox(select_window, textvariable=selected_object, values=object_list)
    combobox.pack(padx=10, pady=10)

    result = None  # Variable für die Auswahlübernahme

    # Funktion für den OK Button
    def ok_button_click():
        nonlocal result
        result = selected_object.get()
        print("Gewählt: " + result)
        select_window.destroy()  # Schließe das Auswahlfenster

    # "OK" Button
    ok_button = tk.Button(select_window, text="OK", command=lambda: ok_button_click)
    ok_button.pack(padx=10, pady=10)

    # Warte bis Fenster geschlossen wurde und gib die gewählte Auswahl zurück
    select_window.wait_window()
    return result
    #########################################################################

######### Callback-Funktionen für Datei-Handling ###############
#-----------------------------------------------------------------
#Speichern
def save_file_callback():
    if original_image_path:
        # Farbkonvertierung von RGB in BGR
        export_img = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        # Speichere das Bild unter dem gegebenen Dateinamen
        cv2.imwrite(original_image_path, export_img)
        print(f"Datei gespeichert: {original_image_path}")

#Funktion, um speichern unter aufzurufen
def save_file_as_callback():
    # Filedialog öffnen --> Speichern des Ziel-Pfades
    file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=file_types)
    if file_path:
        # Farbkonvertierung von RGB in BGR
        export_img = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        # Speichere Bild in neuen Ziel-Pfad
        cv2.imwrite(file_path, export_img)
        print(f"Datei gespeichert unter: {file_path}")

#-----------------------------------------------------------------
######### Callback-Funktionen für A_Standardfunktionen ###############
#-----------------------------------------------------------------
# Callback-Funktion für Reset zum Ursprungsbild
def reset2original_callback():
    if original_image_copy is not None:
        # Farbkonvertierung von RGB in BGR
        reset_img = cv2.cvtColor(original_image_copy, cv2.COLOR_BGR2RGB)
        # Zeige Bild an
        show_image_live(reset_img)
        print("Reset durchgeführt.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Bild spiegeln H
def mirror_v_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.mirror_img_v(rgb_image))
        print("Bild horizontal gespiegelt.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Bild spiegeln V
def mirror_h_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.mirror_img_h(rgb_image))
        print("Bild vertikal gespiegelt.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Bild Rotieren
def rotate_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.rotate_img(rgb_image, standardfunktionen.rotation_angle))
        print("Bild rotiert.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Bild skalieren
def scale_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.scale_img(rgb_image, standardfunktionen.scale_factor))
        print("Bild skaliert.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Bild in Graustufen umwandeln
def img2greyscale_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.grayscale_img(rgb_image))
        print("Bild in Graustufen umgewandelt.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Bild Ausschneiden
def crop_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.crop_img(rgb_image, standardfunktionen.cut_x_pos, standardfunktionen.cut_y_pos, standardfunktionen.cut_width, standardfunktionen.cut_height))
        print("Bild ausgeschnitten.")
    else:
        print("Error: Kein Bild geladen.")

# Callback-Funktion zum Rahmen hinzufügen
def addFrame_callback():
    global rgb_image
    if rgb_image is not None:
        show_image_live(standardfunktionen.add_frame(rgb_image, standardfunktionen.frame_thickness, standardfunktionen.frame_color))
        print("Rahmen hinzugefügt.")
    else:
        print("Error: Kein Bild geladen.")
#-----------------------------------------------------------------

#-----------------------------------------------------------------
######### Callback-Funktionen für B_Erweiterte_Funktionen ###############
#-----------------------------------------------------------------

# Callback-Funktion Markup
def markup_image_function_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.markup_image_function(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Filter
def filter_effect_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.filter_effect(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Schwarzweiß 
def black_white_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.black_white(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Weichzeichner
def blur_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.blur(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Text auf Bild
def text_effect_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.text_effect(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Kontrast
def contrast_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.contrast(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Helligkeit
def brightness_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.brightness(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Dunkel
def darken_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.darken(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Verpixelung 
def pixelate_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.pixelate(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Weißabgleich
def white_balance_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.white_balance(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Licht
def add_light_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.add_light(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Schatten
def shadow_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.add_shadow(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Farbkanäle
def color_balance_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.color_balance(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

# Callback-Funktion Sepia
def sepia_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.sepia(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return

    else:
        return

# Callback-Funktion Sättigung
def saturation_callback():
    if rgb_image is not None:
        return_image = erweiterte_Funktionen.saturation(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

#-----------------------------------------------------------------

# Funktion, um Text 2 Speech zu starten und andere Buttons zu aktivieren
def on_text_to_speech_click():
    ocr.text_to_speech()
    pause_button.configure(state="normal")
    resume_button.configure(state="normal")
    stop_button.configure(state="normal")

# Funktion, um Sprache anzeigen zu lassen
def on_sprache_button_click():
    detected_language = ocr.detect_language(use_conditions=True)
    language_label.configure(text=f"Erkannte Sprache: {detected_language}")

# CustomTkinter root window erzeugen und Einstellungen vornehmen
root = customtkinter.CTk()
root.title("BILDBEARBEITUNG UND BILDANALYSE")

customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_appearance_mode("dark")

# Hauptfenster in der Bildschirmmitte positionieren
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1280
window_height = 800
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Menüleiste inkl. Menupunkte erstellen
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Datei öffnen", command=show_file_dialog)
file_menu.add_command(label="Datei speichern", command=save_file_callback)
file_menu.add_command(label="Datei speichern unter", command=save_file_as_callback)
file_menu.add_separator()
file_menu.add_command(label="OCR-Text als PDF speichern", command=lambda: ocr.text_to_pdf(original_image_path))
file_menu.entryconfigure("OCR-Text als PDF speichern", state=DISABLED)  # Deaktiviere den Menüpunkt

# ... andere Menüpunkte usw.
file_menu.add_separator()
file_menu.add_command(label="Ende", command=lambda: close_program())

settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Standardeinstellungen", command=lambda:einstellungen.standard_einstellungen(root))
settings_menu.add_command(label="Objektsuche in Bildern", command=lambda:Suche_Bilder_mit_Objekten(root))

info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="Hilfe", command=info.show_help_dialog)
info_menu.add_command(label="Entwicklerteam", command=info.show_info_dialog)
info_menu.add_command(label="Programmversion", command=info.show_version_dialog)

menu_bar.add_cascade(label="Datei", menu=file_menu)
menu_bar.add_cascade(label="Einstellungen", menu=settings_menu)
menu_bar.add_cascade(label="Info", menu=info_menu)

root.config(menu=menu_bar)

# Button zum "reseten" des Canvas hinzufügen
reset_button = customtkinter.CTkButton(root, width=30, text="Reset", command=lambda: allg_Funktionen.reset_canvas(canvas_list, anzeigen_Bildbreite, anzeigen_Bildhoehe, anzeigen_Dateipfad))
reset_button.place(x=30, y=20)

# Button zum Zurücksetzen auf das Originalbild hinzufügen
reset_button = customtkinter.CTkButton(root, width=30, text="Original", command=reset2original_callback)
reset_button.place(x=80, y=20)

# Liste für die Canvas-Objekte erstellen
canvas_list = []

# Rahmen für die einzelnen Funktionen der Anwendung
standard_frame = customtkinter.CTkFrame(root, width=550, height=700, fg_color="#30302e")
standard_frame.place(x=700, y=25)

# Label für die Standardfunktionen erzeugen und positionieren
label_standard = customtkinter.CTkLabel(standard_frame, text="---------- STANDARDFUNKTIONEN ----------", fg_color="transparent")
label_standard.place(x=15, y=15)

# Bereitstellung der Buttons (Standard) inkl. Anordnung im standard_frame und Bild laden
rotieren_path = r".\Icons\icon_rotieren.png"  # Lade das Bild
rotieren_original = Image.open(rotieren_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
rotieren_image = rotieren_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(rotieren_image)
rotieren_button = customtkinter.CTkButton(standard_frame, text="Rotieren", image=tk_image, command=rotate_callback)
rotieren_button.place(x=15, y=50)

skalieren_path = r".\Icons\icon_skalieren.png"  # Lade das Bild
skalieren_original = Image.open(skalieren_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
skalieren_image = skalieren_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(skalieren_image)
skalieren_button = customtkinter.CTkButton(standard_frame, text="Skalieren", image=tk_image, command=scale_callback)
skalieren_button.place(x=200, y=50)

spiegelhor_path = r".\Icons\icon_spiegeln_horizontal.png"  # Lade das Bild
spiegelhor_original = Image.open(spiegelhor_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
spiegelhor_image = spiegelhor_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(spiegelhor_image)
spiegelhor_button = customtkinter.CTkButton(standard_frame, text="Spiegeln\n horizontal", image=tk_image, command=mirror_h_callback)
spiegelhor_button.place(x=385, y=50)

vertikal_path = r".\Icons\icon_spiegeln_vertikal.png"  # Lade das Bild
vertikal_original = Image.open(vertikal_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
vertikal_image = vertikal_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(vertikal_image)
spiegelver_button = customtkinter.CTkButton(standard_frame, text="Spiegeln\n vertikal", image=tk_image, command=mirror_v_callback)
spiegelver_button.place(x=15, y=100)

ausschneiden_path = r".\Icons\icon_ausschneiden.png"  # Lade das Bild
ausschneiden_original = Image.open(ausschneiden_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
ausschneiden_image = ausschneiden_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(ausschneiden_image)
ausschneiden_button = customtkinter.CTkButton(standard_frame, text="Ausschneiden", image=tk_image, command=crop_callback)
ausschneiden_button.place(x=200, y=100)

rahmen_path = r".\Icons\icon_Rahmen_hinzufügen.png"  # Lade das Bild
rahmen_original = Image.open(rahmen_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
rahmen_image = rahmen_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(rahmen_image)
rahmen_button = customtkinter.CTkButton(standard_frame, text="Rahmen\n hinzufügen", image=tk_image, command=addFrame_callback)
rahmen_button.place(x=385, y=100)

# Label für die Erweiterten Funktionen erzeugen und positionieren
label_erweitert = customtkinter.CTkLabel(standard_frame, text="---------- ERWEITERTE FUNKTIONEN ----------", fg_color="transparent")
label_erweitert.place(x=15, y=160)#180

markup_path = r".\Icons\icon_markup.png"  # Lade das Bild
markup_original = Image.open(markup_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
markup_image = markup_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(markup_image)
markup_button = customtkinter.CTkButton(standard_frame, text="Markup", image=tk_image, command= lambda : markup_image_function_callback())
markup_button.place(x=15, y=195)#215

filter_path = r".\Icons\icon_filter.png"  # Lade das Bild
filter_original = Image.open(filter_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
filter_image = filter_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(filter_image)
filter_button = customtkinter.CTkButton(standard_frame, text="Filter", image=tk_image, command= lambda : filter_effect_callback())
filter_button.place(x=200, y=195)#215

blackwhite_path = r".\Icons\icon_blackwhite.png"  # Lade das Bild
blackwhite_original = Image.open(blackwhite_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
blackwhite_image = blackwhite_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(blackwhite_image)
blackwhite_button = customtkinter.CTkButton(standard_frame, text="Schwarz\n Weiß", image=tk_image, command= lambda : black_white_callback())
blackwhite_button.place(x=385, y=195)#215

blur_path = r".\Icons\icon_blur.png"  # Lade das Bild
blur_original = Image.open(blur_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
blur_image = blur_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(blur_image)
blur_button = customtkinter.CTkButton(standard_frame, text="Blur Effekt", image=tk_image, command= lambda : blur_callback())
blur_button.place(x=15, y=245)#265

text_path = r".\Icons\icon_text.png"  # Lade das Bild
text_original = Image.open(text_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
text_image = text_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(text_image)
text_button = customtkinter.CTkButton(standard_frame, text="Text", image=tk_image, command= lambda : text_effect_callback())
text_button.place(x=200, y=245)#265

kontrast_path = r".\Icons\icon_kontrast.png"  # Lade das Bild
kontrast_original = Image.open(kontrast_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
kontrast_image = kontrast_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(kontrast_image)
kontrast_button = customtkinter.CTkButton(standard_frame, text="Kontrast", image=tk_image, command= lambda : contrast_callback())
kontrast_button.place(x=385, y=245)#265

helligkeit_path = r".\Icons\icon_Helligkeit.png"  # Lade das Bild
helligkeit_original = Image.open(helligkeit_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
helligkeit_image = helligkeit_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(helligkeit_image)
helligkeit_button = customtkinter.CTkButton(standard_frame, text="Helligkeit", image=tk_image, command= lambda : brightness_callback())
helligkeit_button.place(x=15, y=295)#315

dunkel_path = r".\Icons\icon_dunkel.png"  # Lade das Bild
dunkel_original = Image.open(dunkel_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
dunkel_image = dunkel_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(dunkel_image)
dunkel_button = customtkinter.CTkButton(standard_frame, text="Dunkel", image=tk_image, command= lambda : darken_callback())
dunkel_button.place(x=200, y=295)#315

pixel_path = r".\Icons\icon_pixel.png"  # Lade das Bild
pixel_original = Image.open(pixel_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
pixel_image = pixel_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(pixel_image)
pixel_button = customtkinter.CTkButton(standard_frame, text="Pixel", image=tk_image, command= lambda : pixelate_callback())
pixel_button.place(x=385, y=295) #315

konvertieren_path = r".\Icons\icon_konvertieren.png"  # Lade das Bild
konvertieren_original = Image.open(konvertieren_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
konvertieren_image = konvertieren_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(konvertieren_image)
konvertieren_button = customtkinter.CTkButton(standard_frame, text="Weißabgleich", image=tk_image, command= lambda : white_balance_callback())
konvertieren_button.place(x=15, y=345)#365

licht_path = r".\Icons\icon_Licht.png"  # Lade das Bild
licht_original = Image.open(licht_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
licht_image = licht_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(licht_image)
licht_button = customtkinter.CTkButton(standard_frame, text="Licht", image=tk_image, command= lambda : add_light_callback())
licht_button.place(x=200, y=345)#365

schatten_path = r".\Icons\icon_schatten.png"  # Lade das Bild
schatten_original = Image.open(schatten_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
schatten_image = schatten_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(schatten_image)
schatten_button = customtkinter.CTkButton(standard_frame, text="Schatten", image=tk_image, command= lambda : shadow_callback())
schatten_button.place(x=385, y=345) #365

rgb_path = r".\Icons\icon_rgb.png"  # Lade das Bild
rgb_original = Image.open(rgb_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
rgb_image_pic = rgb_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(rgb_image_pic)
rgb_button = customtkinter.CTkButton(standard_frame, text="Farbkanäle", image=tk_image, command= lambda : color_balance_callback())
rgb_button.place(x=15, y=395)#415

sepia_path = r".\Icons\icon_sepia.png"  # Lade das Bild
sepia_original = Image.open(sepia_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
sepia_image = sepia_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(sepia_image)
sepia_button = customtkinter.CTkButton(standard_frame, text="Sepia", image=tk_image, command= lambda : sepia_callback())
sepia_button.place(x=200, y=395)

sättigung_path = r".\Icons\icon_sättigung.png"  # Lade das Bild
sättigung_original = Image.open(sättigung_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
sättigung_image = sättigung_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(sättigung_image)
sättigung_button = customtkinter.CTkButton(standard_frame, text="Sättigung", image=tk_image, command= lambda : saturation_callback())
sättigung_button.place(x=385, y=395)#415

# Label für die Bilderkennung erzeugen und positionieren
label_erweitert = customtkinter.CTkLabel(standard_frame, text="---------- BILDERKENNUNG UND OBJEKTSUCHE ----------", fg_color="transparent")
label_erweitert.place(x=15, y=455)

gesicht_path = r".\Icons\icon_gesicht.png"  # Lade das Bild
gesicht_original = Image.open(gesicht_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
gesicht_image = gesicht_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(gesicht_image)
gesicht_button = customtkinter.CTkButton(standard_frame, text="Wieder-\n erkennung", image=tk_image, command=lambda:FaceRecognition(original_image_path))
gesicht_button.place(x=15, y=490)#530

gesicht_path = r".\Icons\icon_gesicht.png"  # Lade das Bild
gesicht_original = Image.open(gesicht_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
gesicht_image = gesicht_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(gesicht_image)
gesicht_button = customtkinter.CTkButton(standard_frame, text="Datenbank-\n training", image=tk_image,command=lambda:FaceRecognitionTraining())
gesicht_button.place(x=15, y=535)#530

objekte_path = r".\Icons\icon_objekterkennung.png"  # Lade das Bild
objekte_original = Image.open(objekte_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
objekte_image = objekte_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(objekte_image)
objekte_button = customtkinter.CTkButton(standard_frame, text="Objekte \n erkennen", image=tk_image, command= lambda:handle_yolo_1Bild(rgb_image))
objekte_button.place(x=200, y=490) #530

objekte_path = r".\Icons\icon_objekterkennung.png"  # Lade das Bild
objekte_original = Image.open(objekte_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
objekte_image = objekte_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(objekte_image)
objekte_button = customtkinter.CTkButton(standard_frame, text="Objektsuche", image=tk_image, command= lambda:Suche_Bilder_mit_Objekten(root))
objekte_button.place(x=200, y=535) #530

selfie_path = r".\Icons\icon_selfie.png"  # Lade das Bild
selfie_original = Image.open(selfie_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
selfie_image = selfie_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(selfie_image)
selfie_button = customtkinter.CTkButton(standard_frame, text="Selfie", image=tk_image, command=lambda: Hintergrund_Ausblendung_Fkt(root,rgb_image))
selfie_button.place(x=385, y=490) #530

# Label für die Bilderkennung erzeugen und positionieren
label_erweitert = customtkinter.CTkLabel(standard_frame, text="---------- OCR ERKENNUNG UND AUSGABE ----------", fg_color="transparent")
label_erweitert.place(x=15, y=590)   #610

ocrstart_path = r".\Icons\icon_ocrstart.png"  # Lade das Bild
ocrstart_original = Image.open(ocrstart_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
ocrstart_image = ocrstart_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(ocrstart_image)
ocrstart_button = customtkinter.CTkButton(standard_frame, text="OCR Start", image=tk_image, command= lambda: handle_ocr_start(rgb_image))
ocrstart_button.place(x=15, y=620)  #645

text2speech_path = r".\Icons\icon_text2speech.png"  # Lade das Bild
text2speech_original = Image.open(text2speech_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
text2speech_image = text2speech_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(text2speech_image)
text2speech_button = customtkinter.CTkButton(standard_frame, text="Text 2 Speech", image=tk_image, command=on_text_to_speech_click, state="disabled")
text2speech_button.place(x=200, y=620)  #645

text_pause_path = r".\Icons\icon_pause.png"  # Lade das Bild
text_pause_original = Image.open(text_pause_path)
#Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
text_pause_image = text_pause_original.resize(size=[20, 20])
tk_image = ImageTk.PhotoImage(text_pause_image)
pause_button = customtkinter.CTkButton(standard_frame, text="", image=tk_image, command=ocr.on_pause_click, width=20, height=25, state="disabled")
pause_button.place(x=202, y=660)

text_weiter_path = r".\Icons\icon_weiter.png"  # Lade das Bild
text_weiter_original = Image.open(text_weiter_path)
#Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
text_weiter_image = text_weiter_original.resize(size=[20, 20])
tk_image = ImageTk.PhotoImage(text_weiter_image)
resume_button = customtkinter.CTkButton(standard_frame, text="", image=tk_image, command=ocr.on_resume_click, width=20, height=25, state="disabled")
resume_button.place(x=254, y=660)

text_stop_path = r".\Icons\icon_stop.png"  # Lade das Bild
text_stop_original = Image.open(text_stop_path)
#Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
text_stop_image = text_stop_original.resize(size=[20, 20])
tk_image = ImageTk.PhotoImage(text_stop_image)
stop_button = customtkinter.CTkButton(standard_frame, text="", image=tk_image, command=ocr.on_stop_click, width=20, height=25, state="disabled")
stop_button.place(x=306, y=660)

sprache_path = r".\Icons\icon_sprache.png"  # Lade das Bild
sprache_original = Image.open(sprache_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
sprache_image = sprache_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(sprache_image)
sprache_button = customtkinter.CTkButton(standard_frame, text="Sprache\n anzeigen", image=tk_image, command=on_sprache_button_click, state="disabled")
sprache_button.place(x=385, y=620)   #645

language_label = customtkinter.CTkLabel(standard_frame, text=f'', font=("Arial", 10))
language_label.place(x=385, y=660)

def FaceRecognitionTraining():
    '''Funktion zur Wiedererkennung von Personen im Bild, basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''
    einstellungen.show_popup(root,
                             "Wähle im 1. Schritt das übergeordnete Verzeichnis in dem sich\nin mit Personennamen bezeichnet die Bilder der Personen befinden.\n\n\nWähle im 2. Schritt das Verzeichnis in dem die Trainingsdatenbank gespeichert werden soll.")
    try:
        # Laden der trainierten Label Daten aus einer JSON Datei
        file_path_training = filedialog.askdirectory(title="Verzeichnis der Trainingsdaten in Ordnern")
        print("Ordner Trainingsdaten:", file_path_training)

        # Dateipfad für die Speicherung des Modells wählen
        file_path_save = filedialog.askdirectory(title="Speicherort für trainiertes Datenmodell")
        print("Speicherordner:", file_path_save)

        gesichtswiedererkennung.Gesichtswiedererkennung_Trainieren(file_path_training,file_path_save)
        einstellungen.show_popup(root,
                                 "Training erfolgreich durchgeführt.\n\nTeste den trainierten Datensatz und passe ggf.\ndie Bildauswahl an um ein besseres Ergebnis zu erhalten.")
        print("Training durchgeführt")

    except Exception as err_face_recognition_training:
        print("Error Face Recognition Training: ", err_face_recognition_training)
        einstellungen.show_popup(root,
                                 "Training konnte nicht durchgeführt werden!!! Bitte prüfe den gewählten Ordner und die enthaltenen Daten.")

#Funktion zum Wiedererkennen von bekannten Gesichtern im geladenen Bild
def FaceRecognition(image):
    '''Funktion zur Wiedererkennung von Personen im Bild, basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''
    try:
        #Anweisung zur Bedienung einblenden
        einstellungen.show_popup(root,"Die Erkennung wird auf dem angezeigten Bild im Hauptfenster durchgeführt.\n\nWähle im folgenden die vortrainierte Datenbank, die verwendet werden soll.")
        # Laden der trainierten Label und Modell Daten aus einer JSON und XML Datei
        file_path = filedialog.askdirectory(title="Pfad der vortrainierten Daten (Verzeichnis) wählen")
        trained_recognizer, label_map_load = gesichtswiedererkennung.Lade_TrainiertesModell(file_path)

        img = None
        #Gesichtswiedererkennung mit Rückgabe der wesentlichen Eigenschaften
        try:
            img, img_path, name, confidence = gesichtswiedererkennung.Gesichtswiedererkennung(trained_recognizer, image, label_map_load)
        except:
            einstellungen.show_popup(root,
                                     "Ggf. befindet sich kein bekanntes Gesicht im Bild.\n\nEin Unstimmigkeit ist aufgetreten. Bitte prüfe die ausgewählte Bilddatenbank.")
            print("Err oder nur unbekannte Gesichter- Gesichtswiedererkennung GUI")
        #Ausgabe des Bildes mit markierten bekannten Personen
        if img is not None:
            show_image_live(img)

    except Exception as err_face_recognition:
        einstellungen.show_popup(root, "Ggf. befindet sich kein bekanntes Gesicht im Bild.\n\nEin Unstimmigkeit ist aufgetreten. Bitte prüfe die ausgewählte Bilddatenbank.")
        print("Error Face Recognition: ", err_face_recognition)

#Funktion zum durchsuchen von Ordnern mit Bildern nach bekannten Gesichtern
def FaceRecognitionOrdner():
    '''Funktion zur Wiedererkennung von Personen in Bildern eines Verzeichnisses,
    basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''

    # Create a new tkinter window
    select_window = tk.Toplevel()
    select_window.title("Ausgabe Bilder Gesichtswiedererkennung")
    try:
        # Laden der trainierten Label und Modell Daten aus einer JSON und XML Datei
        suchordner = filedialog.askdirectory(title="Verzeichnis der Trainingsdaten:")
        trained_recognizer, label_map_load = gesichtswiedererkennung.Lade_TrainiertesModell(suchordner)

        if trained_recognizer is not None:
            print("Geladenes Modell: "+trained_recognizer)

        # Test mit bekannten Bildern auf Basis der bekannten Gesichtsdatenbank
        folder_path = filedialog.askdirectory(title="Zu durchsuchendes Verzeichnis mit Bildern")
        print("Dateipfad: "+folder_path)
        # Gesichtswiedererkennung mit Rückgabe der wesentlichen Eigenschaften
        counter, gefundene_gesichter = gesichtswiedererkennung.Suche_Bildinhalt_Bekannte_Gesichter(trained_recognizer,label_map_load,folder_path)
        # Ausgabe eines Bildes mit markierten bekannten Personen
        display_images(gefundene_gesichter)

    except Exception as err_face_recognition:
        print("Error Face Recognition: ", err_face_recognition)

def display_images(image_data, root):
    '''Funktion zur Ausgabe der gefundenen Bilder'''
    custom_window = customtkinter.CTkToplevel(root)
    custom_window.title("ERGEBNIS DER OBJEKT IN BILDSUCHE")
    custom_window.attributes('-topmost', 1)  # Fenster in den Vordergrund holen

    # Hauptfenster in der Bildschirmmitte positionieren
    screen_width = custom_window.winfo_screenwidth()
    screen_height = custom_window.winfo_screenheight()
    window_width = 680 # Breite des Fensters erhöht
    window_height = 280
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # INFO für die Auswahl vom YOLO Modell
    info_frame = customtkinter.CTkFrame(custom_window, width=450, height=23)
    info_frame.place(x=200, y=0)
    #Wenn Objekte gefunden wurden
    if len(image_data) > 0:
        objekt_label = customtkinter.CTkLabel(info_frame,
                                          text="Zum Vergrößern auf das Thumbnail klicken.")
        objekt_label.place(x=100, y=0)
    #Wenn keine Objekte gefunden wurden:
    else:
        objekt_label = customtkinter.CTkLabel(info_frame,
                                              text="Kein passendes Bild gefunden.")
        objekt_label.place(x=100, y=0)

    image_cache = []
    labelbuttons= []
    sortiert = dict(sorted(image_data.items(), key=lambda item: item[1][1], reverse=True))

    for i, entrys in enumerate(sortiert.values(), start=1):
        image_path = entrys[0]
        confi = entrys[1]
        #print(f"Eintrag Nr. {i}: Bildpfad: {image_path}, Übereinstimmung: {confi}")
        image_path = image_path.replace('\\', '/')

        img = Image.open(image_path)
        img.thumbnail((100, 100))  # Bild auf ansprechende Vorschaugröße reduzieren
        img = ImageTk.PhotoImage(img)

        # Foto der Liste hinzufügen
        image_cache.append(img)

        #Label zur Bildanzeige, dass auch als Button verwendet wird:
        label = customtkinter.CTkLabel(custom_window, image=img, text="")
        label.image = img
        #Event bei Linksklick auf Label anlegen
        label.bind("<Button-1>", lambda event,path=image_path: l_button_clicked(path))
        labelbuttons.append(label)
        label.grid(row=i, column=0, padx=10, pady=10)

        confidence_label = customtkinter.CTkLabel(custom_window, text=f"Übereinstimmung: {confi:.2f}\nPfad: {image_path}")
        confidence_label.grid(row=i, column=1, padx=10, pady=10)

#Event_ Button links gedrückt
#Hier in Verwendung für die Label/Bilder zur vergrößerten Vorschau Anzeige
def l_button_clicked(path):
    print(f"Bild Pfad: {path}")
    screen_width, screen_height = window_width, window_height
    datei = cv2.imread(path)
    #Bild in der Größe anpassen, so dass es auf dem Bildschirm voll ausgegeben werden kann
    datei = cv2.resize(datei, (screen_width,screen_height))
    cv2.imshow("Ausgewähltes Bild", datei)

def Suche_Bilder_mit_Objekten(root):
    '''Funktion zur Suche nach Objekten in Bildern eines auszuwählenden Verzeichnisses'''
    suchobjekt, modelwahl = einstellungen.objekte_einstellungen(root)
    if suchobjekt:
        print(f"Ausgewähltes Objekt: {suchobjekt}")
    model = None
    if modelwahl is None:
        model = objekterkennung.YOLO(".\model\yolov8m-seg.pt")  # ggf. bereits bei Programmstart initialisieren, da woanders auch verwendet
    else:
        try:
            suchordner = filedialog.askdirectory(title="Suchverzeichnis der Bilder auswählen:")
            model = objekterkennung.YOLO(".\model\\" + modelwahl + "-seg.pt")
            ergebnis = objekterkennung.Suche_Bildinhalt(model, suchobjekt, suchordner, root)
            # Ausgabe des Ergebnisses der gefundenen Bilder
            display_images(ergebnis, root)
        except:
            print("Modell konnte nicht geladen werden")
            einstellungen.show_popup(root,"Modell nicht gefunden.\nBitte Modell herunterladen und im Verzeichnis\nmodel einfügen.")


# Funktion, um YOLO Objekterkennung mit Segmentierung zu starten
def handle_yolo_1Bild(original_image):
    #Lade die Default Yolo Segmentierung
    model = objekterkennung.YOLO(".\model\yolov8m-seg.pt")
    if original_image is None:
        original_image = show_file_dialog()
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    #Führe die Erkennung und Segmentierung aus
    image = objekterkennung.Yolo_run(original_image, model)
    #Zeige das Bild im Vorschaufenster
    show_image_live(image)

#Funktion zum Abrufen der Webcam mit/ohne Hintergrund
def Hintergrund_Ausblendung_Fkt(root, rgb_image):
    global original_image_path
    image = None
    try:
        if original_image_path is not None:
            image = selfie.Hintergrund_Ausblendung(0, rgb_image)
        else:
            image = selfie.Hintergrund_Ausblendung()
        #Falls kein Bild zurückgegeben werden kann, z.B. weil keine Webcam vorhanden ist:
        if image is not None:
            show_image_live(image)
        else:
            einstellungen.show_popup(root, "Keine Videoquelle gefunden. Bitte Webcam prüfen.")
    except:
        einstellungen.show_popup(root,"Keine Videoquelle gefunden.")

ocr_started = False 

def disable_buttons(new_img=False):
    if new_img == True:
        text2speech_button.configure(state="disabled")
        sprache_button.configure(state="disabled")
        file_menu.entryconfigure("OCR-Text als PDF speichern", state=DISABLED)
        pause_button.configure(state="disabled")
        resume_button.configure(state="disabled")
        stop_button.configure(state="disabled")
        language_label.configure(text="")

# Funktion, um OCR zu starten und andere Buttons zu aktivieren
def handle_ocr_start(original_image):
    global ocr_started, text2speech_button, sprache_button
    try:
        status, result = ocr.start_ocr(original_image)
        if status == 'Erfolg' and isinstance(result, np.ndarray):
            ocr_started = True
            text2speech_button.configure(state="normal")
            sprache_button.configure(state="normal")
            file_menu.entryconfigure("OCR-Text als PDF speichern", state=NORMAL)
            show_image_live(result)
        else:
            print('Fehler bei der Texterkennung.')
    except:
        print('Fehler bei der Texterkennung.')

root.mainloop()