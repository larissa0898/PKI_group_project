
from langdetect import detect
from pytesseract import Output
from reportlab.lib.pagesizes import letter
import reportlab.pdfgen.canvas as pdf_canvas
import pytesseract
import cv2
from gtts import gTTS
import pygame
import os


def get_img(img_path):
    image = cv2.imread(img_path)
    return image


def transform_image(image): # Text und Metadaten des Bildes werden für die OCR Boxes extracted
    custom_config = r'--oem 3 --psm 6 -l deu'  # Deutsche Sprache (deu) und zusätzliche Konfigurationen
    text = pytesseract.image_to_string(image, config=custom_config)
    results = pytesseract.image_to_data(image, output_type=Output.DICT)
    return text, results


def get_OCRboxes(image, text, results):
    for i in range(0, len(results['text'])):
        x = results['left'][i]
        y = results['top'][i]
        
        w = results['width'][i]
        h = results['height'][i]    
        text = results['text'][i]
        conf = int(results['conf'][i])    
        if conf > 58:
            text = ''.join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)


def show_image_with_ocr(image, text):
    cv2.imshow(' ', image)
    cv2.waitKey(0) 
  
    cv2.destroyAllWindows() # Alle offenen Fenster werden geschlossen


def detect_language(text):
    language = detect(text)
    return language


def text_to_speech(text):
    language = detect_language(text)
    
    # text-to-speech Objekt wird erstellt und entsprechende Audio-Datei temporär gespeichert
    tts_obj = gTTS(text=text, lang=language, slow=False)
    tts_obj.save('tmp.mp3')
    
    # mp3-Datei wird geladen und abgespielt
    pygame.mixer.init()
    pygame.mixer.music.load('tmp.mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
       continue  # Warten, bis das Abspielen beendet ist

    pygame.mixer.quit()  # Beende den Mixer
    os.remove("tmp.mp3")


def text_to_pdf(text, img_path):
    output_name = img_path.split('/')[-1].split('.')[0]
    pdf_path = f"{output_name}.pdf"

    c = pdf_canvas.Canvas(pdf_path, pagesize=letter)
    textobject = c.beginText()

    textobject.setTextOrigin(100, 700)  # Textposition festlegen
    textobject.setFont("Helvetica", 12)  # Schriftart und -größe festlegen

    # Breite und Höhe des Textfeldes festlegen
    width = 400
    height = 200

    lines = text.split('\n')  # Teile den Text in Zeilen auf
    for line in lines:
        textobject.textLine(line[:width])  # Füge jede Zeile hinzu, beschränkt auf die angegebene Breite

    textobject = c.drawText(textobject)  # Zeichne den Text

    c.save()


pytesseract.pytesseract.tesseract_cmd =r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'