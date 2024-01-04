#Hier Code zur Abbildung der allgemeinen Funktionen#
#Import notwendiger Bibliotheken#
from tkinter import filedialog
import customtkinter


def reset_canvas(canvas_list, anzeigen_Bildbreite, anzeigen_Bildhoehe, anzeigen_Dateipfad):
    #Überprüfe, ob die Liste der Canvas-Objekte nicht leer ist
    if not canvas_list:
        print("Fehler: Kein Bild vorhanden.")
        return

    #Iteriere durch die Canvas-Objekte und setze ihre Eigenschaften zurück
    for canvas in canvas_list:
        canvas.config(bg="black")  # Hintergrundfarbe auf Schwarz setzen
        canvas.delete("all")

    #Label-Objekte zurücksetzen
    if anzeigen_Bildbreite:
        anzeigen_Bildbreite.configure(text="")

    if anzeigen_Bildhoehe:
        anzeigen_Bildhoehe.configure(text="")

    if anzeigen_Dateipfad:
        anzeigen_Dateipfad.configure(text="")

    print("Canvas und Labels zurückgesetzt.")
