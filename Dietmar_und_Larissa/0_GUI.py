# Import allgemeiner Bilbliotheken
import tkinter as tk
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
import customtkinter

from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import StringVar, ttk
from tkinter import DISABLED, NORMAL
from CTkColorPicker import *

# Import Standardfunktionen-Modul
import A_Standardfunktionen

# Import erweiterte Funktionen-Modul
from B_Erweiterte_Funktionen import *

# Import Funktionen Menupunkt Bearbeiten
from E_Allg_Funktionen import *

#Import Funktionen Menupunkt Einstellungen
from G_Einstellungen import *

# Import Funktionen Menupunkt Info
from H_Info import *

from D_OCR import *
from C_Objekterkennung import *
from C_Gesichtswiedererkennung import *
from C_Selfie import *


# Variablen für Bildeigenschaften global definieren
label_Bildbreite = None
label_Bildhöhe = None
label_Dateipfad = None

#Globale Variablen und Konstanten
original_image = None # original image object opencv
original_image_path = None #path of original image
original_image_copy = None #copy of original image to enable a reset
resized_image = None # image resized (just for GUI view)
rgb_image = None #image in RGB converted
tk_image = None # tkinter visual object
file_types = [('JPEG Files', '*.jpg'), ('PNG Files', '*.png'), ('BMP Files', '*.bmp')]
#filename = None

#Variables for basic effects
rotation_angle = 90
scale_factor = 0.5
cut_x_pos = 30
cut_y_pos = 140
cut_width = 150
cut_height = 150
frame_thickness = 20
frame_color = (0, 200, 0)
MAX_IMAGE_WIDTH = 800
MAX_IMAGE_HEIGHT = 600

def print_me():
    print(f"Datei: {original_image.get()}")
    print(f"Datei: ")

#Funktion, um das Programm zu schließen
def close_program():
    root.destroy()

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
    try:
        original_image_path = filedialog.askopenfilename(filetypes=file_types)
        img = cv2.imread(str(original_image_path))
        print("Datei:", str(original_image_path), "geladen.")
        show_image(img)
    except Exception as exc:
        print("Keine Datei geladen: ",exc)

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

    # Größenanpassung des Bildes
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


#Funktion zum Anzeigen des live verarbeiten Bildes, ohne speichern
def show_image_live(image, width=MAX_IMAGE_WIDTH, height=MAX_IMAGE_HEIGHT):
    global original_image
    global resized_image
    global rgb_image #OpenCV konvertiertes Bild - Speichern (Originalgröße)
    global tk_image #Ausgabebild

    rgb_image = image
    resized_image = resize_image(rgb_image, width, height)

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    tk_image = ImageTk.PhotoImage(Image.fromarray(resized_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
    canvas.place(x=35, y=65)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Halte das Tkinter-Fenster offen
    root.mainloop()


# Funktion um das ausgewählte Bild zu laden und die Dateieigenschaften zuzuweisen
def show_image(image):
    global original_image
    global original_image_copy
    global resized_image
    global rgb_image
    global tk_image

    # Speichere Originalbild für Reset-Funktion
    original_image = original_image_copy = image

    # Konvertiere das Bild von BGR zu RGB (für die Anzeige in Tkinter)
    rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Skalierung des Bildes für die Anzeige in GUI
    #resized_image = cv2.resize(rgb_image, (495, 600))
    resized_image = resize_image(rgb_image, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT)

    # Erstelle ein PhotoImage-Objekt aus dem Numpy-Array
    #tk_image = ImageTk.PhotoImage(Image.fromarray(rgb_image))
    tk_image = ImageTk.PhotoImage(Image.fromarray(resized_image))

    # Erstelle ein Canvas und zeige das Bild darin an
    canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
    canvas.place(x=35, y=65)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Füge das Canvas-Objekt zu einer Liste hinzu
    canvas_list.append(canvas)

    # Zeige Bildeigenschaften in den globalen Label-Variablen an
    label_Bildbreite = original_image.shape[1]
    label_Bildhöhe = original_image.shape[0]
    label_Dateipfad = image_path

    # Zeige Bildeigenschaften in den globalen Label-Variablen an
    anzeigen_Bildbreite.configure(text=f"Bildbreite: {label_Bildbreite:,} Pixel")
    anzeigen_Bildhöhe.configure(text=f"Bildhöhe: {label_Bildhöhe:,} Pixel")
    anzeigen_Dateipfad.configure(text=f"Dateipfad: {label_Dateipfad.replace(',', '.')}")

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
    object_list = get_Suchoptionen()  # Lade die Liste verfügbarer Optionen
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
        export_img = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(original_image_path, export_img)
        print(f"Datei gespeichert: {original_image_path}")

#Funktion, um speichern unter aufzurufen
def save_file_as_callback():
    file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=file_types)
    if file_path:
        export_img = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(file_path, export_img)
        print(f"Datei gespeichert unter: {file_path}")

#-----------------------------------------------------------------
######### Callback-Funktionen für A_Standardfunktionen ###############
#-----------------------------------------------------------------
# Callback-Funktion für Reset zum Ursprungsbild
def reset2original_callback():
    print("Reset aufgerufen.")
    if original_image_copy is not None:
        reset_img = cv2.cvtColor(original_image_copy, cv2.COLOR_BGR2RGB)
        show_image_live(reset_img)

# Callback-Funktion zum Bild spiegeln H
def mirror_h_callback():
    print("Funktion Spiegeln H aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.mirror_img_h(rgb_image))

# Callback-Funktion zum Bild spiegeln V
def mirror_v_callback():
    print("Funktion Spiegeln V aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.mirror_img_v(rgb_image))

# Callback-Funktion zum Bild rotieren
def rotate_callback():
    print("Funktion Rotieren aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.rotate_img(rgb_image, rotation_angle))

# Callback-Funktion zum Bild skalieren
def scale_callback():
    print("Funktion Skalieren aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.scale_img(rgb_image, scale_factor))

# Callback-Funktion zum Bild in Graustufen umwandeln
def img2greyscale_callback():
    print("Funktion Graustufen aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.grayscale_img(rgb_image))

# Callback-Funktion zum Bild Ausschneiden
def crop_callback():
    print("Funktion Ausschneiden aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.crop_img(rgb_image, cut_x_pos, cut_y_pos, cut_width, cut_height))

# Callback-Funktion zum Rahmen hinzufügen
def addFrame_callback():
    print("Funktion Rahmen Hinzufügen aufgerufen.")
    global rgb_image
    if rgb_image is not None:
        show_image_live(A_Standardfunktionen.add_frame(rgb_image, frame_thickness, frame_color))

#-----------------------------------------------------------------

#-----------------------------------------------------------------
######### Callback-Funktionen für B_Erweiterte_Funktionen ###############
#-----------------------------------------------------------------


# Callback-Funktion Markup
def markup_image_function_callback():
    if rgb_image is not None:
        return_image = markup_image_function(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Filter
def filter_effect_callback():
    if rgb_image is not None:
        return_image = filter_effect(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Schwarzweiß 
def black_white_callback():
    if rgb_image is not None:
        return_image = black_white(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Weichzeichner
def blur_callback():
    if rgb_image is not None:
        return_image = blur(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Text auf Bild
def text_effect_callback():
    if rgb_image is not None:
        return_image = text_effect(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Kontrast
def contrast_callback():
    if rgb_image is not None:
        return_image = contrast(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Helligkeit
def brightness_callback():
    if rgb_image is not None:
        return_image = brightness(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Dunkel
def darken_callback():
    if rgb_image is not None:
        return_image = darken(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Verpixelung 
def pixelate_callback():
    if rgb_image is not None:
        return_image = pixelate(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Weißabgleich
def white_balance_callback():
    if rgb_image is not None:
        return_image = white_balance(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Licht
def add_light_callback():
    if rgb_image is not None:
        return_image = add_light(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Schatten
def shadow_callback():
    if rgb_image is not None:
        return_image = add_shadow(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Farbkanäle
def color_balance_callback():
    if rgb_image is not None:
        return_image = color_balance(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return


# Callback-Funktion Sepia
def sepia_callback():
    if rgb_image is not None:
        return_image = sepia(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return

    else:
        return


# Callback-Funktion Sättigung
def saturation_callback():
    if rgb_image is not None:
        return_image = saturation(rgb_image)
        if return_image is not None:
            show_image_live(return_image)
        else:
            return
    else:
        return

#-----------------------------------------------------------------

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
file_menu.add_command(label="OCR-Text als PDF speichern", command=lambda: text_to_pdf(original_image_path))
file_menu.entryconfigure("OCR-Text als PDF speichern", state=DISABLED)  # Deaktiviere den Menüpunkt

# ... andere Menüpunkte usw.
file_menu.add_separator()
file_menu.add_command(label="Ende", command=lambda: close_program())

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Default Werte", command=print_me)

settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Standardeinstellungen", command=lambda:standard_einstellungen(root))
settings_menu.add_command(label="Erweiterte Einstellungen", command=print_me)
settings_menu.add_command(label="Bilderkennung /\n Objektsuche", command=objekte_einstellungen)
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
reset_button = customtkinter.CTkButton(root, width=30, text="Ansicht leeren", command=lambda: reset_canvas(canvas_list, anzeigen_Bildbreite, anzeigen_Bildhöhe, anzeigen_Dateipfad))
reset_button.place(x=30, y=30)

# Button zum Zurücksetzen des Canvas hinzufügen
reset_button = customtkinter.CTkButton(root, width=30, text="Reset zum Original", command=reset2original_callback)
reset_button.place(x=130, y=30)

# Liste für die Canvas-Objekte erstellen
canvas_list = []

# Dateieigenschaften anzeigen
anzeigen_Bildbreite = customtkinter.CTkLabel(root, text=label_Bildbreite, fg_color="transparent", text_color="yellow")
anzeigen_Bildbreite.place(x=150, y=33)

anzeigen_Bildhöhe = customtkinter.CTkLabel(root, text=label_Bildhöhe, fg_color="transparent", text_color="yellow")
anzeigen_Bildhöhe.place(x=300, y=33)

anzeigen_Dateipfad = customtkinter.CTkLabel(root, text=label_Dateipfad, fg_color="transparent", text_color="yellow")
anzeigen_Dateipfad.place(x=30, y=690)

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
rgb_image = rgb_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(rgb_image)
rgb_button = customtkinter.CTkButton(standard_frame, text="Farbkanäle", image=tk_image, command= lambda : color_balance_callback())
rgb_button.place(x=15, y=395)#415

sepia_path = r".\Icons\icon_sepia.png"  # Lade das Bild
sepia_original = Image.open(sepia_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
sepia_image = sepia_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(sepia_image)
sepia_button = customtkinter.CTkButton(standard_frame, text="Sepia", image=tk_image, command= lambda : sepia_callback())
sepia_button.place(x=200, y=395)#415

sättigung_path = r".\Icons\icon_sättigung.png"  # Lade das Bild
sättigung_original = Image.open(sättigung_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
sättigung_image = sättigung_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(sättigung_image)
sättigung_button = customtkinter.CTkButton(standard_frame, text="Sättigung", image=tk_image, command= lambda : saturation_callback())
sättigung_button.place(x=385, y=395)#415

# Label für die Bilderkennung erzeugen und positionieren
label_erweitert = customtkinter.CTkLabel(standard_frame, text="---------- BILDERKENNUNG UND OBJEKTSUCHE ----------",
                                         fg_color="transparent")
label_erweitert.place(x=15, y=445) #495

gesicht_path = r".\Icons\icon_gesicht.png"  # Lade das Bild
gesicht_original = Image.open(gesicht_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
gesicht_image = gesicht_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(gesicht_image)
gesicht_button = customtkinter.CTkButton(standard_frame, text="Gesichts-\n erkennung", image=tk_image, command=lambda:FaceRecognition(original_image_path))
gesicht_button.place(x=15, y=470)#530

def FaceRecognitionTraining():
    '''Funktion zur Wiedererkennung von Personen im Bild, basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''
    try:
        # Laden der trainierten Label Daten aus einer JSON Datei
        file_path_training = filedialog.askdirectory(title="Verzeichnis der Trainingsdaten in Ordnern")
        print("Ordner Trainingsdaten:", file_path_training)

        # Dateipfad für die Speicherung des Modells wählen
        file_path_save = filedialog.askdirectory(title="Speicherort für trainiertes Datenmodell")
        print("Speicherordner:", file_path_save)

        Gesichtswiedererkennung_Trainieren(file_path_training,file_path_save)

        print("Training durchgeführt")

    except Exception as err_face_recognition_training:
        print("Error Face Recognition Training: ", err_face_recognition_training)

#Funktion zum Wiedererkennen von bekannten Gesichtern im geladenen Bild
def FaceRecognition(image):
    '''Funktion zur Wiedererkennung von Personen im Bild, basierend auf den gespeicherten Trainingsdaten, die ausgewählt werden können'''
    print("Dateipfad: "+image)
    try:
        # Laden der trainierten Label und Modell Daten aus einer JSON und XML Datei
        file_path = filedialog.askdirectory(title="Pfad der vortrainierten Daten (Verzeichnis) wählen")
        print("Selected Folder:", file_path)
        trained_recognizer, label_map_load = Lade_TrainiertesModell(file_path)

        # Test mit bekannten Bildern auf Basis der bekannten Gesichtsdatenbank
        #test_image_path = filedialog.askopenfilename(title="Bild mit Gesichtern auswählen")

        #Gesichtswiedererkennung mit Rückgabe der wesentlichen Eigenschaften
        #img,img_path,name,confidence = Gesichtswiedererkennung(trained_recognizer, test_image_path, label_map_load)
        img, img_path, name, confidence = Gesichtswiedererkennung(trained_recognizer, image, label_map_load)

        #Ausgabe des Bildes mit markierten bekannten Personen
        show_image_live(img)

    except Exception as err_face_recognition:
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
        trained_recognizer, label_map_load = Lade_TrainiertesModell(suchordner)
        #print("Geladenes Modell: "+trained_recognizer)
        if trained_recognizer is not None:
            print("OK 1")

        # Test mit bekannten Bildern auf Basis der bekannten Gesichtsdatenbank
        folder_path = filedialog.askdirectory(title="Zu durchsuchendes Verzeichnis mit Bildern")
        print("Dateipfad: "+folder_path)
        # Gesichtswiedererkennung mit Rückgabe der wesentlichen Eigenschaften
        counter, gefundene_gesichter = Suche_Bildinhalt_Bekannte_Gesichter(trained_recognizer,label_map_load,folder_path)
        # Ausgabe eines Bildes mit markierten bekannten Personen
        display_images(gefundene_gesichter)

    except Exception as err_face_recognition:
        print("Error Face Recognition: ", err_face_recognition)

gesicht_path = r".\Icons\icon_gesicht.png"  # Lade das Bild
gesicht_original = Image.open(gesicht_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
gesicht_image = gesicht_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(gesicht_image)
gesicht_button = customtkinter.CTkButton(standard_frame, text="Gesichts-\n erkennung- \n training", image=tk_image)
gesicht_button.place(x=15, y=515)#530

objekte_path = r".\Icons\icon_objekterkennung.png"  # Lade das Bild
objekte_original = Image.open(objekte_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
objekte_image = objekte_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(objekte_image)
objekte_button = customtkinter.CTkButton(standard_frame, text="Objekt-\n erkennung", image=tk_image, command= lambda:handle_yolo_1Bild(original_image))
objekte_button.place(x=200, y=470) #530

def display_images(image_data):
    root2 = tk.Toplevel()
    root2.title("Image Preview")
    root2.geometry('600x600')
    image_cache = []
    for i,(image_path, confidence) in image_data.items():
        image_path = image_path.replace('\\', '/')
        print(f"SubFunc: Eintrag Nr.: {i}: Bild: = {image_path}, Übereinstimmung: = {confidence}")
        img = Image.open(image_path)
        img.thumbnail((100, 100))  # Resize the image to a small preview size
        img = ImageTk.PhotoImage(img)

        # Append the PhotoImage object to the cache list
        image_cache.append(img)

        label = tk.Label(root2, image=img)
        label.image = img
        label.grid(row=i, column=0, padx=10, pady=10)

        confidence_label = tk.Label(root2, text=f"Übereinstimmung: {confidence:.2f}\nPfad: {image_path}")
        confidence_label.grid(row=i, column=1, padx=10, pady=10)

    root2.mainloop()


def Suche_Bilder_mit_Objekten():
    model = YOLO("yolov8m-seg.pt")  # ggf. bereits bei Programmstart initialisieren, da woanders auch verwendet
    suchordner = filedialog.askdirectory(title="Suchverzeichnis der Bilder auswählen:")
    selected_value = select_object()
    if selected_value:
        print(f"Ausgewähltes Objekt: {selected_value}")
    ergenis = Suche_Bilinhalt(model,selected_value,suchordner)
    display_images(ergenis)

objekte_path = r".\Icons\icon_objekterkennung.png"  # Lade das Bild
objekte_original = Image.open(objekte_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
objekte_image = objekte_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(objekte_image)
objekte_button = customtkinter.CTkButton(standard_frame, text="Bilder\n Objekt-\n suche", image=tk_image, command= lambda:Suche_Bilder_mit_Objekten())
objekte_button.place(x=200, y=515) #530

# Funktion, um YOLO Objekterkennung mit Segmentierung zu starten
def handle_yolo_1Bild(original_image):
    #Lade die Default Yolo Segmentierung
    model = YOLO("yolov8m-seg.pt")
    #Führe die Erkennung und Segmentierung aus
    image = Yolo_run(original_image,model)
    #Zeige das Bild im Vorschaufenster
    show_image_live(image)

#Funktion zum Abrufen der Webcam mit/ohne Hintergrund
def Hintergrund_Ausblendung_Fkt():
    global original_image_path
    image = None
    if original_image_path is not None:
        image = Hintergrund_Ausblendung(0,original_image_path)
    else:
        image = Hintergrund_Ausblendung()
    show_image_live(image)


selfie_path = r".\Icons\icon_selfie.png"  # Lade das Bild
selfie_original = Image.open(selfie_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
selfie_image = selfie_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(selfie_image)
selfie_button = customtkinter.CTkButton(standard_frame, text="Selfie", image=tk_image, command=lambda: Hintergrund_Ausblendung_Fkt())
selfie_button.place(x=385, y=470) #530

# Label für die Bilderkennung erzeugen und positionieren
label_erweitert = customtkinter.CTkLabel(standard_frame, text="---------- OCR ERKENNUNG UND AUSGABE ----------",
                                         fg_color="transparent")
label_erweitert.place(x=15, y=570)   #610

ocr_started = False 

# Funktion, um OCR zu starten und andere Buttons zu aktivieren
def handle_ocr_start(original_image):
    global ocr_started, text2speech_button, sprache_button
    status, result = start_ocr(original_image)
    if status == 'Erfolg' and isinstance(result, np.ndarray):
        ocr_started = True
        text2speech_button.configure(state="normal")
        sprache_button.configure(state="normal")
        file_menu.entryconfigure("OCR-Text als PDF speichern", state=NORMAL)
        show_image_live(result)
    else:
        print('Fehler bei der Texterkennung.')


# Funktion, um Text 2 Speech zu starten und andere Buttons zu aktivieren
def on_text_to_speech_click():
    text_to_speech()
    pause_button.configure(state="normal")
    resume_button.configure(state="normal")
    stop_button.configure(state="normal")

# Funktion, um Sprache anzeigen zu lassen
def on_sprache_button_click():
    detected_language = detect_language(use_conditions=True)
    language_label.configure(text=f"Erkannte Sprache: {detected_language}")

ocrstart_path = r".\Icons\icon_ocrstart.png"  # Lade das Bild
ocrstart_original = Image.open(ocrstart_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
ocrstart_image = ocrstart_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(ocrstart_image)
ocrstart_button = customtkinter.CTkButton(standard_frame, text="OCR Start", image=tk_image, command= lambda: handle_ocr_start(rgb_image))
ocrstart_button.place(x=15, y=605)  #645

text2speech_path = r".\Icons\icon_text2speech.png"  # Lade das Bild
text2speech_original = Image.open(text2speech_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
text2speech_image = text2speech_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(text2speech_image)
text2speech_button = customtkinter.CTkButton(standard_frame, text="Text 2 Speech", image=tk_image, command=on_text_to_speech_click, state="disabled")
text2speech_button.place(x=200, y=605)  #645

pause_button = customtkinter.CTkButton(standard_frame, text="Pause", command=on_pause_click, width=20, height=25, state="disabled")
pause_button.place(x=198, y=645)

resume_button = customtkinter.CTkButton(standard_frame, text="Weiter", command=on_resume_click, width=20, height=25, state="disabled")
resume_button.place(x=250, y=645)

stop_button = customtkinter.CTkButton(standard_frame, text="Stop", command=on_stop_click, width=20, height=25, state="disabled")
stop_button.place(x=302, y=645)


sprache_path = r".\Icons\icon_sprache.png"  # Lade das Bild
sprache_original = Image.open(sprache_path)
# Skaliere das Bild auf eine kleinere Größe (z.B. 50x50)
sprache_image = sprache_original.resize(size=[30, 30])
tk_image = ImageTk.PhotoImage(sprache_image)
sprache_button = customtkinter.CTkButton(standard_frame, text="Sprache\n anzeigen", image=tk_image, command=on_sprache_button_click, state="disabled")
sprache_button.place(x=385, y=605)   #645

language_label = customtkinter.CTkLabel(standard_frame, text=f'', font=("Arial", 10))
language_label.place(x=385, y=645)

root.mainloop()
