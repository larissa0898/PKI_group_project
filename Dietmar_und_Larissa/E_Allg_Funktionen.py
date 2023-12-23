# Hier Code zur Abbildung der allgemeinen Funktionen #
from tkinter import filedialog
import customtkinter

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

def reset_canvas(canvas_list, anzeigen_Bildbreite, anzeigen_Bildhöhe, anzeigen_Dateipfad):
    for canvas in canvas_list:
        canvas.config(bg="black")  # Hintergrundfarbe auf Schwarz setzen
        canvas.delete("all")

    # Labels zurücksetzen
    anzeigen_Bildbreite.configure(text="Bildbreite: ")
    anzeigen_Bildhöhe.configure(text="Bildhöhe: ")
    anzeigen_Dateipfad.configure(text="Dateipfad: ")

def print_to_pdf():
    pass
