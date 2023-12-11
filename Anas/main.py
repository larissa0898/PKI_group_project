import cv2
import numpy as np
from tkinter import Tk, Label, Frame, Button, filedialog, Scale, HORIZONTAL
from PIL import Image, ImageTk

# Create the Label widget outside the open_image function
image_label = None
img = None
image_path = None

drawing = False # true if mouse is pressed
ix,iy = -1,-1

# mouse callback function
def draw(event,x,y,flags,param):
    global ix,iy,drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(img,(ix,iy),(x,y),(255,0,0),5)
            ix = x
            iy = y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img,(ix,iy),(x,y),(255,0,0),5)
def open_image():
    global image_label
    global img
    global image_path
    # Open a file dialog to select the image
    image_path = filedialog.askopenfilename(filetypes=[
                                                    ("JPEG", "*.jpg"),
                                                    ("PNG", "*.png"),
                                                    ("GIF", "*.gif"),
                                                    ("All Files", "*.*")
                                                ])

    # Load the image with OpenCV
    image = cv2.imread(image_path)
    img = cv2.imread(image_path)
    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the image to a PIL image
    image = Image.fromarray(image)

    # Scale the image to the size of the frame
    image = image.resize((frame_width, frame_height), Image.LANCZOS)

    # Convert the PIL image to a Tkinter-compatible PhotoImage object
    tk_image = ImageTk.PhotoImage(image)

    # Update the image of the existing Label widget
    image_label.config(image=tk_image)
    image_label.image = tk_image  # Store the PhotoImage object in the .image property of the label

def update(image):
    # Convert the image to a PIL image
    image = Image.fromarray(image)

    # Scale the image to the size of the frame
    image = image.resize((frame_width, frame_height), Image.LANCZOS)

    # Convert the PIL image to a Tkinter-compatible PhotoImage object
    tk_image = ImageTk.PhotoImage(image)

    # Update the image of the existing Label widget
    image_label.config(image=tk_image)
    image_label.image = tk_image  # Store the PhotoImage object in the .image property of the label

def save_image():
    global img
    if img is not None:
        #filename = filedialog.asksaveasfilename(defaultextension=".jpg")
        filename = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                filetypes=[
                                                    ("JPEG", "*.jpg"),
                                                    ("PNG", "*.png"),
                                                    ("GIF", "*.gif"),
                                                    ("All Files", "*.*")
                                                ])
        cv2.imwrite(filename, img)
    else:
        return

def original_image():
    global img
    global image_path
    if img is not None:
        # Load the image with OpenCV
        img = cv2.imread(image_path)
        update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        return

def markup_image():
    global img
    if img is not None:

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('markup image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('markup image', int(frame_width / 1.5), int(frame_height / 1.5))

        while(1):
            cv2.imshow('markup image',img)
            cv2.setMouseCallback('markup image', draw)

            if cv2.waitKey(1) & 0xFF == 27:  # hit esc to exit
                # Convert the image to RGB
                update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                break
            if cv2.getWindowProperty('markup image', cv2.WND_PROP_VISIBLE) < 1:
                # Fenster erstellen und Größe anpassen
                cv2.namedWindow('markup image', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('markup image', int(frame_width / 1.5), int(frame_height / 1.5))

    else:
        return

def filter_effect():
    global img
    if img is not None:
        # Filtereffekte
        img = cv2.Canny(img, 100, 200)
        update(img)  # Beispiel für einen Filter
    else:
        return

def black_white():
    global img
    if img is not None:
        # Farbeffekte
        # Umwandlung in Schwarzweiß
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        update(img)
    else:
        return

def blur():
    global img
    if img is not None:
        # Weichzeichner für Hintergrund
        wz = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.cvtColor(wz, cv2.COLOR_BGR2RGB)
        update(img)
    else:
        return

def text_effect():
    global img
    a = None
    if img is not None:
        # Funktion zum Anpassen des Kontrasts
        def text(img, blue, green, red, font_scale, font_thickness):
            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('text on image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('text on image', int (frame_width/1.5), int (frame_height/1.5))

            cv2.imshow('text on image', img)
            # mouse callback function
            def draw_circle(event, x, y, flags, param):
                global a
                font = cv2.FONT_HERSHEY_SIMPLEX
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    i = 0
                    
                    while True:
                        k = cv2.waitKey(0)
                        # Only draw if the key pressed is a printable character
                        if 32 <= k <= 126:
                            a = cv2.putText(img, chr(k), (x + i, y), font, font_scale, (blue, green, red), font_thickness, cv2.LINE_AA)
                            cv2.imshow('text on image', img)
                        i += 10
                        # Press 'q' to stop writing
                        if k == 27:
                            break

            cv2.namedWindow('text on image')
            cv2.setMouseCallback('text on image', draw_circle)

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Text")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 500
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="Enter your text:").pack()

        # Labels und Schieberegler erstellen
        Label(root, text="blue (0-255):").pack()
        blue = Scale(root, from_=0, to=255, resolution=1, orient=HORIZONTAL)
        blue.pack()

        Label(root, text="green (0-255):").pack()
        green = Scale(root, from_=0, to=255, resolution=1, orient=HORIZONTAL)
        green.pack()

        Label(root, text="red (0-255):").pack()
        red = Scale(root, from_=0, to=255, resolution=1, orient=HORIZONTAL)
        red.pack()

        Label(root, text="font scale (1-100):").pack()
        font_scale = Scale(root, from_=1, to=100, resolution=1, orient=HORIZONTAL)
        font_scale.pack()

        Label(root, text="font thickness (1-100):").pack()
        font_thickness = Scale(root, from_=1, to=100, resolution=1, orient=HORIZONTAL)
        font_thickness.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: text(img, blue.get(), green.get(), red.get(), font_scale.get(), font_thickness.get())).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def contrast():
    global img
    a = None
    if img is not None:
        # Funktion zum Anpassen des Kontrasts
        def adjust_contrast(alpha, beta, img):
            global a
            # Anpassung durchführen
            adjusted = cv2.convertScaleAbs(img, alpha=float(alpha), beta=int(beta))
            a = adjusted

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('contrast', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('contrast', int (frame_width/1.5), int (frame_height/1.5))

            # Ergebnis anzeigen
            cv2.imshow('contrast', adjusted)
            cv2.waitKey()

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Contrast")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="Alpha (1.0-3.0):").pack()
        alpha = Scale(root, from_=1.0, to=3.0, resolution=0.1, orient=HORIZONTAL)
        alpha.pack()

        Label(root, text="Beta (0-100):").pack()
        beta = Scale(root, from_=0, to=100, resolution=1, orient=HORIZONTAL)
        beta.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: adjust_contrast(alpha.get(), beta.get(), img)).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def brightness():
    global img
    a = None
    if img is not None:
        # Funktion zum Anpassen des Kontrasts
        def adjust_contrast(beta, img):
            global a
            # Anpassung durchführen
            adjusted = cv2.convertScaleAbs(img, alpha=float(1), beta=int(beta))
            a = adjusted

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('brightness', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('brightness', int (frame_width/1.5), int (frame_height/1.5))

            # Ergebnis anzeigen
            cv2.imshow('brightness', adjusted)
            cv2.waitKey()

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Brightness")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="Beta (0-100):").pack()
        beta = Scale(root, from_=0, to=100, resolution=1, orient=HORIZONTAL)
        beta.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: adjust_contrast(beta.get(), img)).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def darken():
    global img
    a = None
    if img is not None:
        # Funktion zum Anpassen des Kontrasts
        def adjust_contrast(alpha, img):
            global a
            # Anpassung durchführen
            adjusted = cv2.convertScaleAbs(img, alpha=float(alpha)/100.0, beta=int(0))
            a = adjusted

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('darken', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('darken', int (frame_width/1.5), int (frame_height/1.5))

            # Ergebnis anzeigen
            cv2.imshow('darken', adjusted)
            cv2.waitKey()

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Darken")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="alpha (0-100):").pack()
        alpha = Scale(root, from_=0, to=100, resolution=1, orient=HORIZONTAL)
        alpha.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: adjust_contrast(alpha.get(), img)).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def pixelate():
    global img
    a = None
    if img is not None:
        def pixelate_image(img, pixel_size):
            global a
            # Bildgröße ermitteln
            height, width = img.shape[:2]

            # Bild verkleinern
            img_small = cv2.resize(img, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)

            # Verkleinertes Bild wieder vergrößern
            img_pixelated = cv2.resize(img_small, (width, height), interpolation=cv2.INTER_NEAREST)

            a = img_pixelated

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('pixelate', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('pixelate', int (frame_width/1.5), int (frame_height/1.5))

            # Ergebnis anzeigen
            cv2.imshow('pixelate', img_pixelated)
            cv2.waitKey()

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Pixelate")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="pixel size (1-100):").pack()
        pixel_size = Scale(root, from_=1, to=100, resolution=1, orient=HORIZONTAL)
        pixel_size.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: pixelate_image(img, pixel_size.get())).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def white_balance():
    global img
    if img is not None:
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        img = result
        update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        return

def add_light():
    global img
    a = None

    if img is not None:
        def light(img, radius, center_x, center_y, intensity):
            global a

            # Lichtquelle hinzufügen
            center = (center_x, center_y)  # Zentrum der Lichtquelle

            # Bild in float32 konvertieren
            image = np.float32(img)

            # Lichtquelle erstellen
            mask = np.zeros(image.shape, dtype=np.float32)
            cv2.circle(mask, center, radius, (intensity, intensity, intensity), -1)

            # Lichtquelle zum Bild hinzufügen
            image += mask

            # Werte auf den Bereich 0-255 begrenzen
            image = np.clip(image, 0, 255)

            # Bild in uint8 konvertieren und zurückgeben
            image_edited = np.uint8(image)
            a = image_edited

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('Image with Light', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image with Light', int (frame_width/1.5), int (frame_height/1.5))

            # Bild anzeigen
            cv2.imshow('Image with Light', image_edited)
            cv2.waitKey(0)

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Add Light")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 500
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="light radius (1-5000):").pack()
        radius = Scale(root, from_=0, to=5000, resolution=10, orient=HORIZONTAL)
        radius.pack()

        Label(root, text="center x(1-Frame Width):").pack()
        center_x = Scale(root, from_=0, to=frame_width, resolution=1, orient=HORIZONTAL)
        center_x.pack()

        Label(root, text="center y (1-Frame Height):").pack()
        center_y = Scale(root, from_=0, to=frame_height, resolution=1, orient=HORIZONTAL)
        center_y.pack()

        Label(root, text="light intensity (1-255):").pack()
        intensity = Scale(root, from_=0, to=255, resolution=1, orient=HORIZONTAL)
        intensity.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: light(img, radius.get(), center_x.get(), center_y.get(), intensity.get())).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def add_shadow():
    global img
    a = None

    if img is not None:
        def light(img, intensity):
            global a

            # Bild in float32 konvertieren
            image = np.float32(img)

            # Schatteneffekt erstellen
            shadow = image * intensity

            # Werte auf den Bereich 0-255 begrenzen
            shadow = np.clip(shadow, 0, 255)

            # Bild in uint8 konvertieren und zurückgeben
            image_edited = np.uint8(shadow)
            a = image_edited

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('Image with Shadow', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image with Shadow', int (frame_width/1.5), int (frame_height/1.5))

            # Bild anzeigen
            cv2.imshow('Image with Shadow', image_edited)
            cv2.waitKey(0)

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Add Shadow")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="intensity (0-1):").pack()
        intensity = Scale(root, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        intensity.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: light(img, intensity.get())).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def color_balance():
    global img
    a = None

    if img is not None:
        def adjust_color_balance(img, blue, green, red):
            global a

            b, g, r = cv2.split(img)
            b = cv2.convertScaleAbs(b, alpha=blue)
            g = cv2.convertScaleAbs(g, alpha=green)
            r = cv2.convertScaleAbs(r, alpha=red)

            # Bild in uint8 konvertieren und zurückgeben
            image_edited = cv2.merge([b, g, r])
            a = image_edited

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('Color Balance', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Color Balance', int (frame_width/1.5), int (frame_height/1.5))

            # Bild anzeigen
            cv2.imshow('Color Balance', image_edited)
            cv2.waitKey(0)

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Color Balance")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="blue (0-255):").pack()
        blue = Scale(root, from_=0, to=255, resolution=0.01, orient=HORIZONTAL)
        blue.pack()

        Label(root, text="green (0-255):").pack()
        green = Scale(root, from_=0, to=255, resolution=0.01, orient=HORIZONTAL)
        green.pack()

        Label(root, text="red (0-255):").pack()
        red = Scale(root, from_=0, to=255, resolution=0.01, orient=HORIZONTAL)
        red.pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: adjust_color_balance(img, blue.get(), green.get(), red.get())).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def Sepia():
    global img
    a = None

    if img is not None:
        def sepia_filter():
            global a

            # Sepia-Filter erstellen
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])

            # Sepia-Filter anwenden
            sepia_img = cv2.transform(img, sepia_filter)

            a = sepia_img

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('Sepia', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Sepia', int (frame_width/1.5), int (frame_height/1.5))

            # Bild anzeigen
            cv2.imshow('Sepia', sepia_img)
            cv2.waitKey(0)

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Sepia")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="sepia filter").pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: sepia_filter()).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

def saturation():
    global img
    a = None

    if img is not None:
        def image_saturation():
            global a

            # Bild in HSV umwandeln
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Sättigung erhöhen
            hsv[:, :, 1] = hsv[:, :, 1] * 1.25

            # Bild zurück in BGR umwandeln
            img_saturation = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            a = img_saturation

            # Fenster erstellen und Größe anpassen
            cv2.namedWindow('Saturation', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Saturation', int (frame_width/1.5), int (frame_height/1.5))

            # Bild anzeigen
            cv2.imshow('Saturation', img_saturation)
            cv2.waitKey(0)

        def finish_image():
            global a, img
            img = a
            update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # GUI erstellen
        root = Tk()
        root.title("Saturation")

        # Set the size of the window to the size of the screen
        screen_width = 250
        screen_height = 250
        root.geometry(f"{screen_width}x{screen_height}")

        # Labels und Schieberegler erstellen
        Label(root, text="image saturation").pack()

        # Button zum Öffnen der Dateiauswahl und Anpassen des Kontrasts
        Button(root, text='show picture',
               command=lambda: image_saturation()).pack()
        Button(root, text="finish", command=finish_image).pack()
        # GUI starten
        root.mainloop()

    else:
        return

# Create the Tkinter window
root = Tk()
root.title("AKI-PROJEKT")

# Set the size of the window to the size of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

frame_width = screen_width - int(screen_width * 0.1)
frame_height  = screen_height - 80

# Create a Frame widget for the image
image_frame = Frame(root, width = frame_width, height = frame_height)
image_frame.pack(side="left", expand=False, fill="both")

# Create the Label widget for the image
image_label = Label(image_frame)
image_label.pack()

# Create a Frame widget for other content (e.g., buttons, text fields, etc.)
content_frame = Frame(root)
content_frame.pack(side="bottom", expand=True, fill="both")

# Calculate the size and position of the button
button_width = int(screen_width * 0.1)
button_height = int(screen_height * 0.05)
button_x = (screen_width - button_width)
button_y = 0

# Create the button and place it in the center of the window
btn_open = Button(root, text="open", width=button_width, height=button_height, command=open_image)
btn_save = Button(root, text="save", width=button_width, height=button_height, command=save_image)
btn_original = Button(root, text="original", width=button_width, height=button_height, command=original_image)
btn_markup = Button(root, text="markup", width=button_width, height=button_height, command=markup_image)
btn_filter = Button(root, text="filter", width=button_width, height=button_height, command=filter_effect)
btn_contrast = Button(root, text="contrast", width=button_width, height=button_height, command=contrast)
btn_invert = Button(root, text="invert", width=button_width, height=button_height, command=black_white)
btn_blur = Button(root, text="blur", width=button_width, height=button_height, command=blur)
btn_text = Button(root, text="text", width=button_width, height=button_height, command=text_effect)
btn_brightness = Button(root, text="brightness", width=button_width, height=button_height, command=brightness)
btn_darken = Button(root, text="darken", width=button_width, height=button_height, command=darken)
btn_pixelate = Button(root, text="pixelate", width=button_width, height=button_height, command=pixelate)
btn_whitebalance = Button(root, text="white balance", width=button_width, height=button_height, command=white_balance)
btn_addlight = Button(root, text="add light", width=button_width, height=button_height, command=add_light)
btn_addshadow = Button(root, text="add shadow", width=button_width, height=button_height, command=add_shadow)
btn_colorbalance = Button(root, text="color balance", width=button_width, height=button_height, command=color_balance)
btn_sephiafilter = Button(root, text="sepia filter", width=button_width, height=button_height, command=Sepia)
btn_saetigung = Button(root, text="saturation", width=button_width, height=button_height, command=saturation)

btn_open.place(x=button_x, y=button_y, width=button_width, height=button_height)
btn_save.place(x=button_x, y=button_y + button_height, width=button_width, height=button_height)
btn_original.place(x=button_x, y=button_y + 2 * button_height, width=button_width, height=button_height)
btn_markup.place(x=button_x, y=button_y + 3 * button_height, width=button_width, height=button_height)
btn_filter.place(x=button_x, y=button_y + 4 * button_height, width=button_width, height=button_height)
btn_contrast.place(x=button_x, y=button_y + 5 * button_height, width=button_width, height=button_height)
btn_invert.place(x=button_x, y=button_y + 6 * button_height, width=button_width, height=button_height)
btn_blur.place(x=button_x, y=button_y + 7 * button_height, width=button_width, height=button_height)
btn_text.place(x=button_x, y=button_y + 8 * button_height, width=button_width, height=button_height)
btn_brightness.place(x=button_x, y=button_y + 9 * button_height, width=button_width, height=button_height)
btn_darken.place(x=button_x, y=button_y + 10 * button_height, width=button_width, height=button_height)
btn_pixelate.place(x=button_x, y=button_y + 11 * button_height, width=button_width, height=button_height)
btn_whitebalance.place(x=button_x, y=button_y + 12 * button_height, width=button_width, height=button_height)
btn_addlight.place(x=button_x, y=button_y + 13 * button_height, width=button_width, height=button_height)
btn_addshadow.place(x=button_x, y=button_y + 14 * button_height, width=button_width, height=button_height)
btn_colorbalance.place(x=button_x, y=button_y + 15 * button_height, width=button_width, height=button_height)
btn_sephiafilter.place(x=button_x, y=button_y + 16 * button_height, width=button_width, height=button_height)
btn_saetigung.place(x=button_x, y=button_y + 17 * button_height, width=button_width, height=button_height)

# Start the Tkinter event loop
root.mainloop()
