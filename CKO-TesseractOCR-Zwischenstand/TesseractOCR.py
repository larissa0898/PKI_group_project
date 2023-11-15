import pytesseract
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

########################################################################################################################
## ZWISCHENSTAND - der Texterkennung -> Kritik willkommen :) insbesondere bei Quellen, Doku, und allem anderen auch :)
## 15.11.2023 CKO
##
##
##
##
## ToDo:
## Nach Absprache mit Larissa und dem Team
## - Parameter als Übergabewerte z.B. aus einem Menü "Einstellungen" heraus
## - Ggf. Zusätzlich weitere Sprachen mit anbieten
## -- option: Wie im Skript/Praktikum selbständige Spracherkennung
## - Entfernen der Consolenausgaben
########################################################################################################################

"""
    Projektgruppe A1-1 Tesseract OCR
    Tersseract OCR Texterkennung auf Basis von Tesseract 5.3.3.20231005
    Das Programm erkennt aktuell deutsche Texte in einem Bild und gibt diese in einer Textdatei aus
    Zur manuellen Verifikation werden im Originalbild Boxen um die Wörter gezogen und der erkannte Text wird darüber angezeigt.

    Zur Anzeige der Umlaute im Bild im deutschen muss eine Textfont verwendet werden, die auch die Umlaute beinhaltet. Hier wurde Arial.ttf verwendet.  


    :param: path_output: Pfad + Name der Ausgabe Datei
    :param: path_traindata: Pfad + Name der Sprachdatei der trainierten Texterkennung
    :param: path_font: Pfad + Name der Font Datei.
    :param: path_image: Pfad + Name der auszulesenden Bilddatei.
    :param: path_image_output: Pfad + Name der auszugebenden Bilddatei als Referenz
    :output: Text in Ausgabedatei 

    :return: String mit erkanntem Text

    :exception OSError: t.b.d.

    Quellen:
    - https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
    - Grundlage des Quellcode basiert auf dem Youtube Video  https://www.youtube.com/watch?v=6DjFscX4I_c von Murtaza's Workshop
    - Arial.ttf - Kopie aus Windows Systemverzeichnis Claus-Peter Koch (CKO)
    - 
    
    Verwendete Packages:
    Pillow	10.1.0	
    Pillow-PIL	0.1.dev0	
    numpy	1.26.2	
    opencv-python	4.8.1.78	
    packaging	23.2	
    pip	23.3.1	
    pytesseract	0.3.10	
    setuptools	60.2.0	
    style	1.1.0	
    update	0.0.1	
    wheel	0.37.1	
    
"""
#Default Werte auf meinem PC
path_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"                                                        # Installationspfad von Tesseract-OCR inkl. der Tesseract.exe QUELLE: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
path_traindata = r'"C:\Program Files\Tesseract-OCR\tessdata\deu.traineddata"'                                           # Pfad der Trainingsdaten - hier deu
path_font = r"Arial.ttf"                                                                                                # Pfad der Anzeigetexte. Diese müssen die entsprechende Sonderzeichen wie Ä Ü Ö ä ü ö ß enthalten, in Groß- und Kleinbuchstaben
path_image = r"Eingescannte Seite.png"                                                                                  # Pfad und Name von dem das Bild geladen werden soll
path_image_output = r"Textausgabe.png"                                                                                  # Pfad und Name unter dem das Bild gespeichert werden soll
path_output = r"Textausgabe.txt"                                                                                        # Pfad der Dateiausgabe inkl.Dateiname


def A1_1_TesseractOCR():
    font_size = 10                                                                                                      # (Noch) statische Festlegung der Font Texteinblendung
    output_text = ""                                                                                                    # Ausgabetext

    font = ImageFont.truetype(path_font, font_size)                                                                     # Laden eines Font mit deutschen Sonderzeichen

    pytesseract.pytesseract.tesseract_cmd = path_tesseract                                                              # Verlinkung zur Applikation tesseract.exe herstellen

    img_input = cv2.imread(path_image)                                                                                  # Bild per OpenCV laden

    img = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)                                                                    # Bild vom OpenCV Standard BGR in RGB wandeln

    # Wörter mit Boxen im Bild kennzeichnen
    img_h, img_w, _ = img.shape                                                                                         # Speichern der Zeichenfläche in Variablen für Höhe und Breite

    boxen = pytesseract.image_to_boxes(img)                                                                             # Per Tesseract OCR eine Bilderkennung durchführen.

    boxen_words = pytesseract.image_to_data(img, lang='deu',config=path_traindata)                                      # Per image_to_data werden hier Boxen gesucht, die Wörter umschließen #Alternativen wäre pytesseract.image_to_data(***) zum finden von Buchstaben

    for x, b in enumerate(boxen_words.splitlines()):                                                                    # Schleife zum Auswerten der gefundenen Boxen
        if (x != 0):
            b = b.split()
            # print(b)                                                                                                  #Test Ausgabe der einzelnen erkannten Texte inkl. Positionen
            if len(b) == 12:                                                                                            # Im 12. Element steht der erkannte Text, der Rest kann hier ignoriert werden.
                output_text += b[11] + ' '                                                                              # Ausgabetext den neuen Text hinzufügen zzgl. Leerzeichen
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])                                                 # In den Positionen 6 steht der x-Offset des zu zeichnenden Rechtecks, 7-Y-Offset, 8-Breite, 9-Höhe
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0),1)                                               # Da Zeichnen umgekeht zum Erfassen ausgewertet wird, muss das Rechteck mit Offset berücksichtigt werden

                ##################################################
                # Da OpenCV nur UTF-8 Schrfitsätze ohne Sonderzeichen unterstützt muss hier auf einen Schriftsatz für DEU zurückgegriffen werden. Hierfür ist eine Übergabe an die PIL Funktionen notwendig
                ##################################################
                # cv2.putText(img,(b[11]),(x,y),font,1,(0,255,0),2)                                                      #Für englische Texte, jedoch nicht für DE, da standard Fonts keine DE Sonderzeichen enthalten

                # Draw text using Pillow (PIL)                                                                           #QUELLE: ChatGPT 3.5 - 14.11.2023 - CKO
                pil_img = Image.fromarray(
                    cv2.cvtColor(img, cv2.COLOR_BGR2RGB))                                                               # Wandlung des Bildes in ein für PIL akzeptables Format
                draw = ImageDraw.Draw(pil_img)                                                                          # Zeichenfläche erstellen

                # Assuming 'font_path' is the path to your TrueType or OpenType font file
                draw.text((x, y - int(font_size)), b[11], font=font, fill=(0, 0,
                                                                           255))                                        # Zeichensatz in Ladessprache verwenden, Standard .ttf Format, Text in definierte Farb und Größe an Position der oberen rechten Kante des Rechtecks in Bild schreiben

                # Convert the PIL image back to OpenCV format
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)                                                # Wandlung zurück in OpenCV Format

            elif len(b) == 11:                                                                                          # Zur Einhaltung des Versmaßes Zeilenumbrüche erkennen
                output_text += "\n"                                                                                     # Ausgabetext einen Zeilenumbruch hinzufügen

    print(output_text)                                                                                                  # Ausgabe erkannter Text
    cv2.imshow('Testerkennung', img)                                                                                    # Anzeige erkannter Texte

    cv2.imwrite(path_image_output,img)                                                                                  # Speichern des Bildes mit eingeblendetem erkannten Text als "Entwickler" Referenz und für Fehlersuche

    datei = open(path_output, 'w')                                                                                      # Datei zum Schreiben öffnen/erstellen
    datei.write(output_text)                                                                                            # Text in Datei schreiben
    datei.close()                                                                                                       # Datei schließen
    print("Datei schreiben erfolgreich")

    cv2.waitKey(0)                                                                                                      # Auf Tasteneingabe warten vor beenden

    return (output_text)


if __name__ == '__main__':
    A1_1_TesseractOCR()