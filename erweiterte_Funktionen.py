import customtkinter
import cv2
import numpy as np
from CTkColorPicker import AskColor
from customtkinter import CTk, HORIZONTAL

# globale variablen
img = None
color = None
thickness = None

# Markup Draw Funktion globale Variablen
drawing = False  # true if mouse is pressed
ix, iy = -1, -1


# Farbauswahlfunktion
def choose_color():
    # globale variablen
    global color
    # Öffne den Farbwähler und rufe die Farbzeichenfolge ab
    pick_color = AskColor(title="Farbauswahlfunktion")
    color = pick_color.get()
    return color


# Maus-Callback-Funktion
def draw(event, x, y, flags, param):
    # globale variablen
    global ix, iy, drawing, thickness

    # Falls keine Farbe ausgewählt ist, Default ist Schwarz
    if param is not None:
        blue, green, red = tuple(int(param[i:i + 2], 16) for i in (1, 3, 5))
    else:
        red = 0
        green = 0
        blue = 0

    # Falls keine Schriftstärke ausgewählt ist, Default ist 7
    if thickness is None:
        thickness = 7

    # Maus Events
    # lenke Maustaste ist gedrückt, malen ist erlaubt!
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # lenke Maustaste ist gedrückt, malen!
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(img, (ix, iy), (x, y), (red, green, blue), thickness)
            ix = x
            iy = y

    # lenke Maustaste ist losgelassen, malen ist NICHT erlaubt!
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


# Funktion zum Freischreiben bzw. Malen auf einem Bild
def markup_image_function(image):
    # globale variablen
    global img, color, thickness

    # lokale variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Schriftstärke Funktion
    def font_thickness():
        # globale variablen
        global thickness

        # Bearbeitung bzw. Einstellung beenden
        def finish_thickness():
            global thickness
            thickness = int(thickness_scale.get())
            sub_root.quit()  # Schließe das Tkinter-Fenster
            sub_root.destroy()

        # GUI erstellen
        sub_root = CTk()
        sub_root.title('Markup Funktion Schriftstärke')

        # Einstellung der Größe des Fensters
        sub_root_screen_width = 350
        sub_root_screen_height = 145
        sub_root.geometry(f"{sub_root_screen_width}x{sub_root_screen_height}")
        sub_root.resizable(False, False)

        # Label hinzufügen
        customtkinter.CTkLabel(sub_root, text="Schriftstärke (0 - 100):").place(x=30, y=10)

        # Slider hinzufügen
        thickness_scale = customtkinter.CTkSlider(sub_root, from_=1, to=100, number_of_steps=99, orientation=HORIZONTAL,
                                                  width=290)
        thickness_scale.set(1)
        thickness_scale.place(x=27, y=43)

        # Button hinzufügen
        customtkinter.CTkButton(sub_root, text='Fertig', command=finish_thickness, width=290).place(x=30, y=109)

        # GUI starten
        sub_root.mainloop()

    def markup():
        # globale variablen
        global img, color

        # lokale variablen
        nonlocal adjusted

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Markup Funktion Bild Vorschau', cv2.WINDOW_NORMAL)

        while 1:
            # zeige das Bild, um es zu bearbeiten
            cv2.imshow('Markup Funktion Bild Vorschau', img)
            cv2.setMouseCallback('Markup Funktion Bild Vorschau', draw, param=color)

            # Drücke Esc, um den Vorgang zu beenden
            if cv2.waitKey(1) & 0xFF == 27:
                adjusted = img
                return

            # Fall das Fenster nicht mit Esc zugemacht wird, wieder anzeigen
            if cv2.getWindowProperty('Markup Funktion Bild Vorschau', cv2.WND_PROP_VISIBLE) < 1:
                # Fenster erstellen und Größe anpassen
                cv2.namedWindow('Markup Funktion Bild Vorschau', cv2.WINDOW_NORMAL)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        # globale variablen
        global color

        # Reset Farbe beim Beenden
        color = None
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Markup Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 145
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Farbe", command=choose_color, width=290).place(x=30, y=10)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Schriftstärke", command=font_thickness, width=290).place(x=30, y=43)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Markup", command=markup, width=290).place(x=30, y=76)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=109)

    # GUI starten
    root.mainloop()
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Cany-Filter - Kantenerkennung
def filter_effect(image):
    # globale Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def cany_filter(cany_filter_image, threshold_1, threshold_2):
        # lokale Variablen
        nonlocal adjusted

        # Filtereffekte
        adjusted = cv2.Canny(cany_filter_image, threshold_1, threshold_2)

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Filtereffekt Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Bild anzeigen
        cv2.imshow('Filtereffekt Funktion Vorschau', adjusted)
        cv2.waitKey(0)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Filtereffekt Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 287
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Grenzwert 1: (1 - 1000):").place(x=30, y=10)

    # Slider hinzufügen
    Grenzwert_1 = customtkinter.CTkSlider(root, from_=0, to=1000, number_of_steps=1000, orientation=HORIZONTAL,
                                          width=290)
    Grenzwert_1.set(100)
    Grenzwert_1.place(x=27, y=43)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Grenzwert 2: (1 - 1000):").place(x=30, y=109)

    # Slider hinzufügen
    Grenzwert_2 = customtkinter.CTkSlider(root, from_=0, to=1000, number_of_steps=1000, orientation=HORIZONTAL,
                                          width=290)
    Grenzwert_2.set(200)
    Grenzwert_2.place(x=27, y=142)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Filtereffekt',
                            command=lambda: cany_filter(img, int(Grenzwert_1.get()), int(Grenzwert_2.get())),
                            width=290).place(x=30, y=208)
    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=241)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Schwarz-weiße Filter
def black_white(image):
    # globale Variablen
    global img

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Umwandlung in Schwarzweiß
    adjusted = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Funktion zum Weichzeichnen eines Bildes
def blur(image):
    # globale variablen
    global img

    # lokale variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # #Verwischfunktion Einstellungen
    def adjust_blur(k1, k2, sigma_x, blur_image):
        # lokale variablen
        nonlocal adjusted

        adjusted = cv2.GaussianBlur(blur_image, (k1, k2), sigma_x)  # GaussianBlur

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Blur Funktion Vorschau', cv2.WINDOW_NORMAL)
        cv2.imshow('Blur Funktion Vorschau', adjusted)
        cv2.waitKey()

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Blur Funktion")

    screen_width = 350
    screen_height = 376
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="K1 (0 - 100):").place(x=30, y=10)

    # Slider hinzufügen
    k1_slider = customtkinter.CTkSlider(root, from_=1, to=99, number_of_steps=49, orientation=HORIZONTAL, width=290)
    k1_slider.set(1)
    k1_slider.place(x=27, y=43)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="K2 (0 - 100):").place(x=30, y=109)

    # Slider hinzufügen
    k2_slider = customtkinter.CTkSlider(root, from_=1, to=99, number_of_steps=49, orientation=HORIZONTAL, width=290)
    k2_slider.set(1)
    k2_slider.place(x=27, y=142)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="sigmaX (0 - 100):").place(x=30, y=208)

    # Slider hinzufügen
    sigma_x_slider = customtkinter.CTkSlider(root, from_=0, to=100, number_of_steps=100, orientation=HORIZONTAL,
                                             width=290)
    sigma_x_slider.set(0)
    sigma_x_slider.place(x=27, y=241)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Blur Effekt',
                            command=lambda: adjust_blur(int(k1_slider.get()), int(k2_slider.get()),
                                                        int(sigma_x_slider.get()), img),
                            width=290).place(x=30, y=307)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=340)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Funktion zum Schreiben auf einem Bild
def text_effect(image):
    # globale Variablen
    global img, color

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Einstellungen des Schreibens
    def text(text_image, text_color, font_scale, font_thickness):

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Texteffekt Funktion Vorschau', cv2.WINDOW_NORMAL)
        cv2.imshow('Texteffekt Funktion Vorschau', text_image)

        # Maus-Callback Funktion
        def write_text(event, x, y, flags, param):
            # lokale Variablen
            nonlocal adjusted

            # Schriftart
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Falls keine Farbe ausgewählt ist, Default ist Schwarz
            if text_color is None:
                red = 0
                green = 0
                blue = 0
            else:
                blue, green, red = tuple(int(text_color[i:i + 2], 16) for i in (1, 3, 5))

            # Maus-Event prüfen
            if event == cv2.EVENT_LBUTTONDOWN:
                i = 0

                while True:
                    # Initialisierung
                    k = cv2.waitKey(0)

                    # Nur zeichnen, wenn die gedrückte Taste ein druckbares Zeichen ist
                    if 32 <= k <= 126:
                        adjusted = cv2.putText(text_image, chr(k), (x + i, y), font, font_scale,
                                               (red, green, blue), font_thickness, cv2.LINE_AA)
                        cv2.imshow('Texteffekt Funktion Vorschau', text_image)

                    i += 10

                    # Drücke Esc, um den Vorgang zu beenden
                    if k == 27:
                        break

                    # Falls es keine Tastatureingabe gibt, BREAK
                    if k == -1:
                        break

        cv2.namedWindow('Texteffekt Funktion Vorschau')
        cv2.setMouseCallback('Texteffekt Funktion Vorschau', write_text)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        # globale variablen
        global color

        # Reset Farbe beim Beenden
        color = None
        cv2.destroyAllWindows()
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Texteffekt Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 312
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Schriftskala (1 - 100):").place(x=30, y=10)

    # Slider hinzufügen
    font_scale_slider = customtkinter.CTkSlider(root, from_=1, to=100, number_of_steps=99, orientation=HORIZONTAL,
                                                width=290)
    font_scale_slider.set(1)
    font_scale_slider.place(x=27, y=43)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Schriftstärke (1 - 100):").place(x=30, y=112)

    # Slider hinzufügen
    font_thickness_slider = customtkinter.CTkSlider(root, from_=1, to=100, number_of_steps=99, orientation=HORIZONTAL,
                                                    width=290)
    font_thickness_slider.set(1)
    font_thickness_slider.place(x=27, y=145)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Farbe", command=choose_color, width=290).place(x=30, y=211)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Text Effekt',
                            command=lambda: text(img, color, int(font_scale_slider.get()),
                                                 int(font_thickness_slider.get())),
                            width=290).place(x=30, y=243)
    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=276)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Kontrast Verbesserung
def contrast(image):
    # globale Variablen
    global img

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Ermittel den minimalen und maximalen Pixelwert
    minimumColor = np.amin(img)
    maximumColor = np.amax(img)

    # Erstelle zwei Matrizen basierend auf dem Durchschnittspixelwert
    avg = np.mean(img)
    colorDownMatrix = img < avg
    colorUpMatrix = img > avg

    # Passen Sie den Bildkontrast an
    adjusted = img - minimumColor * colorDownMatrix
    adjusted = adjusted + maximumColor * colorUpMatrix

    # Sicherstellen, dass die Pixelwerte im richtigen Bereich bleiben
    lessThen0 = adjusted < 0
    moreThen255 = adjusted > 255
    adjusted[lessThen0] = 0
    adjusted[moreThen255] = 255

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Helligkeit Anpassung Funktion
def brightness(image):
    # globale Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Funktion zum Anpassen des Kontrasts
    def adjust_brightness(alpha, beta, brightness_image):
        nonlocal adjusted

        # Anpassung durchführen
        if alpha == 1:  # Nur Aufhellen
            adjusted = cv2.convertScaleAbs(brightness_image, alpha=float(1), beta=float(beta))
        else:
            adjusted = cv2.convertScaleAbs(brightness_image, alpha=float(alpha) / 100.0, beta=float(beta))

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Helligkeit Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Ergebnis anzeigen
        cv2.imshow('Helligkeit Funktion Vorschau', adjusted)
        cv2.waitKey()

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Helligkeit Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 343
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Zum Aufhellen Alpha = 1 ein und ändern Beta!").place(x=30, y=10)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Zum Abdunkeln Beta = 0 und ändern Alpha!").place(x=30, y=43)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Alpha (1 - 100):").place(x=30, y=76)

    # Slider hinzufügen
    alpha_slider = customtkinter.CTkSlider(root, from_=1, to=100, number_of_steps=99, orientation=HORIZONTAL, width=290)
    alpha_slider.set(1.0)
    alpha_slider.place(x=27, y=109)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Beta (0 - 100):").place(x=30, y=175)

    # Slider hinzufügen
    beta_slider = customtkinter.CTkSlider(root, from_=0, to=100, number_of_steps=100, orientation=HORIZONTAL, width=290)
    beta_slider.set(0)
    beta_slider.place(x=27, y=208)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Helligkeit',
                            command=lambda: adjust_brightness(int(alpha_slider.get()), int(beta_slider.get()), img),
                            width=290).place(
        x=30, y=274)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=307)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Schatten hinzufügen Funktion
def darken(image):
    # globale Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def darken_image_function(darken_img, intensity):
        nonlocal adjusted

        # Bild in float32 konvertieren
        edit_image = np.float32(darken_img)

        # Schatteneffekt erstellen
        darken_image = edit_image * intensity

        # Werte auf den Bereich 0-255 begrenzen
        darken_image = np.clip(darken_image, 0, 255)

        # Bild in uint8 konvertieren und zurückgeben
        adjusted = np.uint8(darken_image)

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Dunkel Funktion Vorschau', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Image with Shadow', int (frame_width/1.5), int (frame_height/1.5))

        # Bild anzeigen
        cv2.imshow('Dunkel Funktion Vorschau', adjusted)
        cv2.waitKey(0)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Dunkel Funktion")

    # Set the size of the window to the size of the screen
    screen_width = 350
    screen_height = 176
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Intensität (0 - 1):").place(x=30, y=10)

    # Slider hinzufügen
    intensity_slider = customtkinter.CTkSlider(root, from_=0, to=1, number_of_steps=100, orientation=HORIZONTAL,
                                               width=290)
    intensity_slider.set(0)
    intensity_slider.place(x=28, y=43)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Dunkel',
                            command=lambda: darken_image_function(img, float(intensity_slider.get())), width=290).place(
        x=30, y=109)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=142)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Verpixelung Funktion
def pixelate(image):
    # globale Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Verpixelung Funktion Einstellungen
    def pixelate_image(pixel_image, pixel_size):
        # lokale Variablen
        nonlocal adjusted

        pixelate_img = pixel_image

        # Bildgröße ermitteln
        height, width = pixelate_img.shape[:2]

        # Bild verkleinern
        img_small = cv2.resize(pixelate_img, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)

        # Verkleinertes Bild wieder vergrößern
        adjusted = cv2.resize(img_small, (width, height), interpolation=cv2.INTER_NEAREST)

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Pixel Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Ergebnis anzeigen
        cv2.imshow('Pixel Funktion Vorschau', adjusted)
        cv2.waitKey()

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Pixel Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 178
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Pixelgröße (1 - 100):").place(x=30, y=10)

    # Slider hinzufügen
    pixel_size_slider = customtkinter.CTkSlider(root, from_=1, to=100, number_of_steps=99, orientation=HORIZONTAL,
                                                width=290)
    pixel_size_slider.set(1)
    pixel_size_slider.place(x=28, y=43)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Pixel',
                            command=lambda: pixelate_image(img, int(pixel_size_slider.get())), width=290).place(x=30,
                                                                                                                y=109)
    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=142)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Weißabgleich Funktion
def white_balance(image):
    # globale Variablen
    global img

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    adjusted = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    avg_a = np.average(adjusted[:, :, 1])
    avg_b = np.average(adjusted[:, :, 2])
    adjusted[:, :, 1] = adjusted[:, :, 1] - ((avg_a - 128) * (adjusted[:, :, 0] / 255.0) * 1.1)
    adjusted[:, :, 2] = adjusted[:, :, 2] - ((avg_b - 128) * (adjusted[:, :, 0] / 255.0) * 1.1)

    adjusted = cv2.cvtColor(adjusted, cv2.COLOR_LAB2BGR)

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Licht hinzufügen Funktion
def add_light(image):
    # globale Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def light(light_image, radius, center_x, center_y, intensity):
        # lokale Variablen
        nonlocal adjusted

        # Lichtquelle hinzufügen
        center = (center_x, center_y)  # Zentrum der Lichtquelle

        # Bild in float32 konvertieren
        edit_image = np.float32(light_image)

        # Lichtquelle erstellen
        mask = np.zeros(edit_image.shape, dtype=np.float32)
        cv2.circle(mask, center, radius, (intensity, intensity, intensity), -1)

        # Lichtquelle zum Bild hinzufügen
        edit_image += mask

        # Werte auf den Bereich 0-255 begrenzen
        edit_image = np.clip(edit_image, 0, 255)

        # Bild in uint8 konvertieren und zurückgeben
        adjusted = np.uint8(edit_image)

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Licht Hinzufuegen Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Bild anzeigen
        cv2.imshow('Licht Hinzufuegen Funktion Vorschau', adjusted)
        cv2.waitKey(0)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Licht Hinzufuegen Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 478
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Lichtradius (1 - 5000):").place(x=30, y=10)

    # Slider hinzufügen
    radius_slider = customtkinter.CTkSlider(root, from_=1, to=5000, number_of_steps=4999, orientation=HORIZONTAL,
                                            width=290)
    radius_slider.set(0)
    radius_slider.place(x=28, y=43)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Mittelpunkt des Lichtkreises X (1-Frame Width):").place(x=30, y=109)

    # Slider hinzufügen
    center_x_slider = customtkinter.CTkSlider(root, from_=0, to=500, number_of_steps=500, orientation=HORIZONTAL,
                                              width=290)
    center_x_slider.set(0)
    center_x_slider.place(x=28, y=142)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Mittelpunkt des Lichtkreises Y (1-Frame Height):").place(x=30, y=208)

    # Slider hinzufügen
    center_y_slider = customtkinter.CTkSlider(root, from_=0, to=500, number_of_steps=500, orientation=HORIZONTAL,
                                              width=290)
    center_y_slider.set(0)
    center_y_slider.place(x=28, y=241)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Lichtintensität (1 - 255):").place(x=30, y=307)

    # Slider hinzufügen
    intensity_slider = customtkinter.CTkSlider(root, from_=1, to=255, number_of_steps=255, orientation=HORIZONTAL,
                                               width=290)
    intensity_slider.set(0)
    intensity_slider.place(x=28, y=340)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Licht',
                            command=lambda: light(img, int(radius_slider.get()), int(center_x_slider.get()),
                                                  int(center_y_slider.get()),
                                                  int(intensity_slider.get())), width=290).place(x=30, y=409)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=442)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Schatten Funktion
def add_shadow(image):
    # globle Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def adjust_shadows(shadow_image, gamma, clip_limit):
        # lokale Variablen
        nonlocal adjusted

        # Konvertierung in das Lab-Farbraumformat
        lab = cv2.cvtColor(shadow_image, cv2.COLOR_BGR2LAB)

        # Aufteilen in Kanäle
        l, a, b = cv2.split(lab)

        # Gamma-Korrektur auf dem L-Kanal (Helligkeit)
        l = cv2.pow(l / 255.0, gamma)
        l = np.uint8(l * 255)

        # Kontrast Limited Adaptive Histogram Equalization (CLAHE) auf dem L-Kanal
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        l = clahe.apply(l)

        # Zusammenführen der Kanäle
        lab = cv2.merge((l, a, b))

        # Zurückkonvertieren in das BGR-Farbraumformat
        adjusted = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Schatten Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Bild anzeigen
        cv2.imshow('Schatten Funktion Vorschau', adjusted)
        cv2.waitKey(0)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Schatten Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 287
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Gamma (0.1 - 3):").place(x=30, y=10)

    # Slider hinzufügen
    gamma_slider = customtkinter.CTkSlider(root, from_=0.1, to=3, number_of_steps=290, orientation=HORIZONTAL,
                                           width=290)
    gamma_slider.set(0)
    gamma_slider.place(x=28, y=43)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="clip limit (2 - 4):").place(x=30, y=109)

    # Slider hinzufügen
    clip_limit_slider = customtkinter.CTkSlider(root, from_=2, to=4, number_of_steps=200, orientation=HORIZONTAL,
                                                width=290)
    clip_limit_slider.set(0)
    clip_limit_slider.place(x=28, y=142)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Schatten',
                            command=lambda: adjust_shadows(img, float(gamma_slider.get()),
                                                           float(clip_limit_slider.get())), width=290).place(x=30,
                                                                                                             y=208)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=241)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Farbeffekte Funktion
def color_balance(image):
    # globale Variablen
    global img, color

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Farbeffekte Funktion Einstellungen
    def adjust_color_balance(adjust_color_img, adjust_color):
        # lokale Variablen
        nonlocal adjusted

        b, g, r = cv2.split(adjust_color_img)

        # Falls keine Farbe ausgewählt ist, Default ist Schwarz
        if adjust_color is None:
            red = 100
            green = 100
            blue = 100
        else:
            red, green, blue = tuple(int(adjust_color[i:i + 2], 16) for i in (1, 3, 5))

        b = cv2.convertScaleAbs(b, alpha=blue)  # Blau
        g = cv2.convertScaleAbs(g, alpha=green)  # Grün
        r = cv2.convertScaleAbs(r, alpha=red)  # Rot

        # Bild in uint8 konvertieren und zurückgeben
        adjusted = cv2.merge([b, g, r])

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Farbeffekte Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Bild anzeigen
        cv2.imshow('Farbeffekte Funktion Vorschau', adjusted)
        cv2.waitKey(0)

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        # globale variablen
        global color

        # Reset Farbe beim Beenden
        color = None
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Farbeffekte Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 112
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Button hinzufügen
    customtkinter.CTkButton(root, text="Farbe", command=choose_color, width=290).place(x=30, y=10)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Farbeffekte',
                            command=lambda: adjust_color_balance(img, color), width=290).place(x=30, y=43)
    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=76)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Sepia Filter
def sepia(image):
    # globale Variablen
    global img

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Sepia-Filter erstellen
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])

    # Sepia-Filter anwenden
    adjusted = cv2.transform(img, sepia_filter)

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)


# Sättigungsfunktion
def saturation(image):
    # globale Variablen
    global img

    # lokale Variablen
    adjusted = None

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def saturation_function(saturate_image, saturate_value):
        # lokale Variablen
        nonlocal adjusted

        # Bild in HSV umwandeln
        hsv = cv2.cvtColor(saturate_image, cv2.COLOR_RGB2HSV)

        # Sättigung ändern
        hsv[:, :, 1] = hsv[:, :, 1] * saturate_value

        # Bild zurück in RGB umwandeln
        adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

        # Fenster erstellen und Größe anpassen
        cv2.namedWindow('Saetigung Funktion Vorschau', cv2.WINDOW_NORMAL)

        # Ergebnis anzeigen
        cv2.imshow('Saetigung Funktion Vorschau', adjusted)
        cv2.waitKey()

    # Bearbeitung bzw. Einstellung beenden
    def finish_image():
        root.quit()  # Schließe Tkinter-Fenster
        root.destroy()

    # GUI erstellen
    root = CTk()
    root.title("Saetigung Funktion")

    # Einstellung der Größe des Fensters
    screen_width = 350
    screen_height = 178
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(False, False)

    # Label hinzufügen
    customtkinter.CTkLabel(root, text="Saetigung (0 - 2):").place(x=30, y=10)

    # Slider hinzufügen
    saturation_value = customtkinter.CTkSlider(root, from_=0, to=2, number_of_steps=200, orientation=HORIZONTAL,
                                               width=290)
    saturation_value.set(1.25)
    saturation_value.place(x=28, y=43)

    # Button hinzufügen
    customtkinter.CTkButton(root, text='Saetigung',
                            command=lambda: saturation_function(img, float(saturation_value.get())), width=290).place(
        x=30,
        y=109)
    # Button hinzufügen
    customtkinter.CTkButton(root, text="Fertig", command=finish_image, width=290).place(x=30, y=142)

    # GUI starten
    root.mainloop()

    # Falls nichts bearbeiten wurde, return Original
    if adjusted is None:
        return None
    else:
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
