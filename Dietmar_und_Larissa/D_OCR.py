from langdetect import detect
from pytesseract import Output
from reportlab.lib.pagesizes import letter
import pytesseract
import cv2
from gtts import gTTS
import pygame
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

audio_paused = False 
extracted_text = ''

pytesseract.pytesseract.tesseract_cmd =r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def get_OCRboxes(image, text, results):
    for i in range(0, len(results['text'])):
        x = results['left'][i]
        y = results['top'][i]
        
        w = results['width'][i]
        h = results['height'][i]    
        detected_text = results['text'][i]
        conf = int(results['conf'][i])    
        if conf > 58: 
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            image = add_text_with_pillow(image, detected_text, x, y)

    return image


def add_text_with_pillow(image, text, x, y):
    # OpenCV Image wird in Pillow Image umgewandelt, um den Text hinzufügen zu können
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Verwendung von Arial zur Darstellung deutscher Umlaute und besseren Lesbarkeit
    font_path = ".\Dietmar_und_Larissa\Arial.ttf"
    font = ImageFont.truetype(font_path, size=10)

    # Zeichne den Text mit der ausgewählten Schriftart
    draw.text((x, y - 10), text, font=font, fill=(100, 0, 0))
    
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


""" def show_image_with_ocr(image, text):
    cv2.namedWindow('OCR Ergebnis', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('OCR Ergebnis', 650, 900)
    cv2.imshow('OCR Ergebnis', image)
    cv2.setWindowTitle('OCR Ergebnis', 'Ergebnis der Texterkennung')
    cv2.waitKey(0) 
  
    cv2.destroyAllWindows()
    return image """

def start_ocr(image):
    global extracted_text

    try:
        text = pytesseract.image_to_string(image)

        language= detect(text)
        language_mappings = {'de': 'deu', 'en': 'eng','fr': 'fra','es': 'spa','it': 'ita'}

        if language in language_mappings:
            language = language_mappings[language]
            
        text = pytesseract.image_to_string(image, lang=language)
        results = pytesseract.image_to_data(image, lang=language, output_type=Output.DICT)

    except:
        print("Es wurde kein Text gefunden.")
        return "Fehler"
    
    image_with_text = get_OCRboxes(image, text, results)
    #show_image_with_ocr(image_with_text, text)
    extracted_text = text
    return "Erfolg", image_with_text

    
def detect_language(use_conditions=False):
    language = detect(extracted_text)
    lang_dict = {'de': 'Deutsch', 'en': 'Englisch','fr': 'Französisch','es': 'Spanisch','it': 'Italienisch'}
    if use_conditions:

        if language in lang_dict:
            language = lang_dict[language]

    return language


def on_pause_click():
    pause_audio()

def on_resume_click():
    resume_audio()

def on_stop_click():
    stop_audio()


def text_to_speech():
    language = detect_language()

    # text-to-speech Objekt wird erstellt und entsprechende Audio-Datei temporär gespeichert
    tts_obj = gTTS(text=extracted_text, lang=language, slow=False)
    tts_obj.save('tmp.mp3')
    
    # mp3-Datei wird geladen und abgespielt
    pygame.mixer.init()
    pygame.mixer.music.load('tmp.mp3')
    pygame.mixer.music.play()
    

def pause_audio():
    global audio_paused

    if pygame.mixer.music.get_busy() and not audio_paused:
        pygame.mixer.music.pause()
        audio_paused = True

def resume_audio():
    global audio_paused
    if pygame.mixer.music.get_busy()==False and audio_paused:
        pygame.mixer.music.unpause()
        audio_paused = False

def stop_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove("tmp.mp3")



def text_to_pdf(img_path):
    output_name = img_path.split('/')[-1].split('.')[0]
    pdf_path = f"{output_name}.pdf"

    c = canvas.Canvas(pdf_path, pagesize=letter)
    textobject = c.beginText()

    x_coordinate = 50  # Start x-coordinate
    y_coordinate = 750  # Start y-coordinate

    textobject.setTextOrigin(x_coordinate, y_coordinate)  # Text position
    textobject.setFont("Helvetica", 12)  # Font and size

    lines = extracted_text.split('\n')
    line_height = 14  # Height between lines

    for line in lines:
        textobject.textLine(line)  # Add each line without limiting width
        y_coordinate -= line_height  # Adjust vertical position

        if y_coordinate <= 50:  # Check if approaching page bottom
            c.drawText(textobject)  # Draw the text on the page
            c.showPage()  # Add a new page
            y_coordinate = 750  # Reset y-coordinate for new page
            textobject = c.beginText()  # Begin new text object for the new page
            textobject.setTextOrigin(x_coordinate, y_coordinate)  # Reset text position

    c.drawText(textobject)  # Draw the text on the last page
    c.save()