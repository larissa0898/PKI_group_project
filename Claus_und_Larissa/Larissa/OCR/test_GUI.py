import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from OCR_functions import *

img_path = None

def browse_image():
    global img_path, img_label, extracted_text
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    image = Image.open(img_path)
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo
    extracted_text = None
    enable_functions()

def enable_functions():
    btn_ocr.config(state=tk.NORMAL)
    btn_read.config(state=tk.NORMAL)
    btn_language.config(state=tk.NORMAL)
    btn_extract.config(state=tk.NORMAL)

""" def perform_ocr_with_translation():
    perform_ocr(translate=True)

def perform_ocr_without_translation():
    perform_ocr(translate=False) """

def perform_ocr():
    global extracted_text
    image = get_img(img_path)
    text, results = transform_image(image)
    image_with_text = get_OCRboxes(image, text, results)
    show_image_with_ocr(image_with_text, text)
    extracted_text = text 

def read_text():
    global extracted_text
    text_to_speech(extracted_text)

def show_language():
    global extracted_text
    if extracted_text:
        language = detect_language(extracted_text)
        language_display.config(text=f'Erkannte Sprache: {language}')

def extract_to_pdf():
    global extracted_text
    text_to_pdf(extracted_text, img_path)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


root = tk.Tk()
root.title("OCR GUI")

# Scrollbar und Canvas
scrollbar = tk.Scrollbar(root, orient="vertical")
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

scrollbar.config(command=canvas.yview)
canvas.bind("<Configure>", on_configure)

# Frame im Canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")


# Schaltflächen
btn_browse = tk.Button(root, text="Bild auswählen", command=browse_image)
btn_browse.pack()

btn_ocr = tk.Button(root, text="OCR ausführen", command=perform_ocr, state=tk.DISABLED)
btn_ocr.pack()

btn_read = tk.Button(root, text="Text vorlesen", command=read_text, state=tk.DISABLED)
btn_read.pack()

btn_language = tk.Button(root, text="Sprache anzeigen", command=show_language, state=tk.DISABLED)
btn_language.pack()

btn_extract = tk.Button(root, text="Extrahieren zu PDF", command=extract_to_pdf, state=tk.DISABLED)
btn_extract.pack()

# Bildanzeige
img_label = tk.Label(root)
img_label.pack()

# Textanzeige
text_display = tk.Text(root, height=10, width=50, state=tk.DISABLED)
text_display.pack()

# Sprachanzeige
language_display = tk.Label(root, text="")
language_display.pack()

# Diese Zeile aktualisiert das Canvas-Scrollgebiet basierend auf dem Inhalt des Frames
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()