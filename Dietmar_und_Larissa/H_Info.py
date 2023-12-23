# Hier Code zur Abbildung der allgemeinen Funktionen #
from tkinter import messagebox

#Erzeugt eine Messagebox, um eine kurze Übersicht zu den Funktionen anzuzeigen
def show_help_dialog():
    help_text = """
    Hier sind die Funktionen des Programms:

    1. Standardfunktionen:
       - Rotieren: Dreht das Bild im Uhrzeigersinn.
       - Skalieren: Ändert die Größe des Bildes.
       - Spiegel horizontal: Spiegelt das Bild horizontal.
       - Spiegel vertikal: Spiegelt das Bild vertikal.
       - Ausschneiden: Bereich aus Bild schneiden.
       - Rahmen hinzufügen: Rahmen erstellen.

    2. Erweiterte Funktionen:
       - Markup: Hervorhebung bestimmter Bereiche im Bild.
       - Filter: Anwendung von Filtern auf das Bild.
       - Schwarz Weiß: Konvertiert das Bild in Schwarz-Weiß.
       - Blur Effekt: Fügt einen Weichzeichnungseffekt hinzu.
       - Text: Einfügen von Text in das Bild.
       - Kontrast: Ändert den Kontrast des Bildes.
       - Helligkeit: Passt die Helligkeit des Bildes an.
       - Dunkel: Verdunkelt das Bild.
       - Pixel: Fügt einen Pixel-Effekt hinzu.
       - Konvertieren: Konvertiert das Bild in ein anderes Format.
       - Licht: Fügt Lichteffekte hinzu.
       - Schatten: Fügt Schatten hinzu.
       - Farbkanäle: Zeigt die Farbkanäle des Bildes an.
       - Sepia: Konvertiert das Bild in Sepia.
       - Sättigung: Ändert die Sättigung des Bildes.

    3. Bilderkennung und -transformation:
       - Gesichtserkennung: Erkennt Gesichter im Bild.
       - Objekterkennung: Erkennt Objekte im Bild.
       - Selfie: Wendet Effekte für Selfies an.

    4. OCR Funktionen:
       - OCR Start: Startet die Texterkennung im Bild.
       - Text 2 Speech: Spielt Audio-Datei mit dem extrahierten Text ab.
       - Sprache anzeigen: Anzeiger der erkannten Sprache.
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