# Disclaimer von Phil Balczukat, 10043796
# Die hier definierten Funktionen wurden von mir vollständig selbst entwickelt.
# Beim "Finden" der richtigen Methoden aus der CV2 Bibliothek (opencv)
# habe ich mir von ChatGPT und Stackoverflow auf die Sprünge helfen lassen.

# Einzig die Funktion rotate_img() wurde sinngemäß aus Stackoverflow übernommen, da eigene Lösungen
# zu einem unerwünschten Abschneiden des Bildes führten.

# Hier Standardfunktionen abbilden #
import cv2
import math
import numpy as np

# Globale Variablen mit Default-Werten
# werden im 0_GUI.py beim Funktionsaufruf genutzt und via Dialog vom Nutzer manipuliert
rotation_angle = 90 #°
scale_factor = 0.5 # factor
cut_x_pos = 0 #px
cut_y_pos = 0 #px
cut_width = 300 #px
cut_height = 300 #px
frame_thickness = 20 #pt
frame_color = (0, 200, 0) # RGB Tupel

# Funktion zum Rotieren eines Bildes um einen beliebigen Winkel in Grad
def rotate_img(img, angle):
    #----------------- Vorherige Lösung -------------------
    # Get size (# of rows and columns) of image
    # rows, cols = img.shape[:2]
    # Create Rotation matrix
    # ...center = center point of rotation --> Middle point of image
    # ...angle = user defined rotation angle
    # ...scale = scaling factor --> always =1 for this method
    # rot_Mat = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    # Apply rotation matrix with target image size = original size
    # return cv2.warpAffine(img, rot_Mat, (rows, cols))
    # return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #-------------------------------------------------------
    # ----------------- Neue Lösung -------------------
    # Extrahiere Bildgröße
    h, w = img.shape[:2]

    # Rotationspunkt=Mittelpunkt setzen
    centerpoint = (w / 2, h / 2)

    # Rotationsmatrix berechnen
    rot = cv2.getRotationMatrix2D(centerpoint, angle, 1)

    # Winkel von Grad in Rad umrechnen
    rad = math.radians(angle)

    # Sinus und Cosinuswert des Rotationswinkels bestimmen
    sin = math.sin(rad)
    cos = math.cos(rad)

    # Verschiebungswerte des Mittelpunktes ermitteln
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))

    # Rotationsmatrix anpassen gemäß Verschiebung des Mittelpunktes
    rot[0, 2] += ((b_w / 2) - centerpoint[0])
    rot[1, 2] += ((b_h / 2) - centerpoint[1])

    print("Bild rotiert.")
    # Rotiertes Bild erzeugen (Rotationsmatrix auf Bild anwenden)
    exp_image = cv2.warpAffine(img, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)

    # Hinzugekommene Kanten entfernen
    # In Graustufen umwandeln
    gray = cv2.cvtColor(exp_image, cv2.COLOR_BGR2GRAY)

    # Definiere den Schwellenwert für die schwarze Farbe
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Finde die Koordinaten der nicht schwarzen Pixel
    konturen, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(konturen[0])
    #print(cv2.boundingRect(konturen[0]))
    
    # Schneide den schwarzen Rand aus dem Bild
    exp_image = exp_image[y:y + h, x:x + w]

    return exp_image

# Funktion zum skalieren des Bildes um einen beliebigen Faktor
def scale_img(img, sfactor):
    # Extrahiere Bildgröße
    rows, cols = img.shape[:2]

    # Neue Größe bestimmen und Typenkonvertierung durchführen
    new_size = (int(cols * sfactor), int(rows * sfactor))

    print("Bild skaliert.")
    # Skalierung durchführen und Bild zurückgeben
    return cv2.resize(img, new_size)

# Funktion zum vertikalen spiegeln
def mirror_img_v(img):
    # flipcode 1 = horizontal
    print("Bild vertikal gespiegelt.")
    return cv2.flip(img, 1)

# fFunktion zum horizontalen spiegeln
def mirror_img_h(img):
    # flipcode 0 = vertical
    print("Bild horizontal gespiegelt.")
    return cv2.flip(img, 0)

# Bild in Graustufen umwandeln
def grayscale_img(img):
    print("Bild in Graustufen umgewandelt.")
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Funktion zum Erzeugen eines Bildausschnitts
def crop_img(img, x, y, w, h):
    # ...x,y = Start-Position des Ausschnitts
    # ...w,h = Höhe und Breite des Ausschnitts ausgehend vom Start-Punkt
    # Bildausschnitt mittels Array-Slicing erzeugen
    print("Bildausschnitt erzeugt.")
    return img[y:y+h, x:x+w]

# Einen voll-farbigen Rahmen um das Bild hinzufügen
def add_frame(img, thickness, color):
    # ...thickness = Dicke des Rahmens
    # gleiche Dicke für alle Seiten nutzen --> TOP, BOTTOM, LEFT, RIGHT
    # ...cv2.BORDER = Framestyle (bold frame)
    print("Rahmen zum Bild hinzugefügt")
    return cv2.copyMakeBorder(img, int(thickness), int(thickness), int(thickness), int(thickness), cv2.BORDER_ISOLATED, value=color)