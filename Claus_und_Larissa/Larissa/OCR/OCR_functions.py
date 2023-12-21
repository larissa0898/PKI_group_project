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


def get_img(img_path):
    image = cv2.imread(img_path)
    return image


def transform_image(image):
    text = pytesseract.image_to_string(image)
    language= detect(text)
    if language == 'de':
        language = 'deu'
    elif language == 'en':
        language = 'eng'
    elif language == 'fr':
        language = 'fra'
    elif language == 'es':
        language = 'spa'
    elif language == 'it':
        language = 'ita'
    
    text = pytesseract.image_to_string(image, lang=language)
    results = pytesseract.image_to_data(image, lang=language, output_type=Output.DICT)

    return text, results


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
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    font_path = "Arial.ttf"
    font = ImageFont.truetype(font_path, size=10)

    # Zeichne den Text mit der ausgewählten Schriftart
    draw.text((x, y - 10), text, font=font, fill=(100, 0, 0))
    
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


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

    c = canvas.Canvas(pdf_path, pagesize=letter)
    textobject = c.beginText()

    x_coordinate = 50  # Start x-coordinate
    y_coordinate = 750  # Start y-coordinate

    textobject.setTextOrigin(x_coordinate, y_coordinate)  # Text position
    textobject.setFont("Helvetica", 12)  # Font and size

    lines = text.split('\n')
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


pytesseract.pytesseract.tesseract_cmd =r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'