# Hier Code zur Abbildung der allgemeinen Funktionen #
from tkinter import filedialog
import customtkinter

def reset_canvas(canvas_list, anzeigen_Bildbreite, anzeigen_Bildhoehe, anzeigen_Dateipfad):
    for canvas in canvas_list:
        canvas.config(bg="black")  # Hintergrundfarbe auf Schwarz setzen
        canvas.delete("all")

    # Labels zurücksetzen
    print(type(anzeigen_Bildbreite))
    anzeigen_Bildbreite.configure(text="")
    anzeigen_Bildhoehe.configure(text="")
    anzeigen_Dateipfad.configure(text="")

