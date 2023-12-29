# Hier Einstellungen für die einzelnen Funktionen
import customtkinter
import PIL.Image, PIL.ImageTk
from PIL import Image
from tkinter import StringVar, ttk
from CTkColorPicker import *
from C_Objekterkennung import *

#Funktion für die Settings der Standardeinstellungen#
def standard_einstellungen(root):
    # CustomTkinter root window erzeugen und Einstellungen vornehmen
    #root = customtkinter.CTk()

    custom_window = customtkinter.CTkToplevel(root)
    custom_window.title("STANDARDEINSTELLUNGEN")
    custom_window.attributes('-topmost', 1)  # Fenster in den Vordergrund holen
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    customtkinter.set_appearance_mode("dark")
    #customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    #customtkinter.set_appearance_mode("dark")

    # Hauptfenster in der Bildschirmmitte positionieren
    screen_width = custom_window.winfo_screenwidth()
    screen_height = custom_window.winfo_screenheight()
    window_width = 820 # Breite des Fensters erhöht
    window_height = 400
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    custom_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Frame für die Rotieren-Einstellungen
    rotieren_frame = customtkinter.CTkFrame(custom_window)
    rotieren_frame.place(x=50, y=50)

    rotieren_label = customtkinter.CTkLabel(rotieren_frame, text="Rotieren:")
    rotieren_label.place(x=0, y=0)

    rotieren_value_label = customtkinter.CTkLabel(rotieren_frame, text="45°")
    rotieren_value_label.place(x=100, y=0)

    def update_rotieren_label(value):
        rotieren_value_label.configure(text=f"{int(value)}°")

    rotieren_slider = customtkinter.CTkSlider(rotieren_frame, from_=0, to=360, command=update_rotieren_label)
    rotieren_slider.set(45)  # Setze den Default-Wert
    rotieren_slider.place(x=0, y=25)

    # Frame für die Skalieren-Einstellungen
    skalieren_frame = customtkinter.CTkFrame(custom_window)
    skalieren_frame.place(x=50, y=150)

    skalieren_label = customtkinter.CTkLabel(skalieren_frame, text="Skalieren:")
    skalieren_label.place(x=0, y=0)

    skalieren_value_label = customtkinter.CTkLabel(skalieren_frame, text="1%")
    skalieren_value_label.place(x=100, y=0)

    def update_skalieren_label(value):
        skalieren_value_label.configure(text=f"{int(value)}%")

    skalieren_slider = customtkinter.CTkSlider(skalieren_frame, from_=0, to=100, command=update_skalieren_label)
    skalieren_slider.set(1)  # Setze den Default-Wert
    skalieren_slider.place(x=0, y=20)

    # Frame für die Rahmen-Einstellungen
    rahmen_frame = customtkinter.CTkFrame(custom_window)
    rahmen_frame.place(x=50, y=250)

    rahmen_label = customtkinter.CTkLabel(rahmen_frame, text="Rahmen:")
    rahmen_label.place(x=0, y=0)

    rahmen_value_label = customtkinter.CTkLabel(rahmen_frame, text="1")
    rahmen_value_label.place(x=100, y=0)

    def update_rahmen_label(value):
        rahmen_value_label.configure(text=f"{int(value)}")

    rahmen_slider = customtkinter.CTkSlider(rahmen_frame, from_=1, to=5, command=update_rahmen_label)
    rahmen_slider.set(1)  # Setze den Default-Wert
    rahmen_slider.place(x=0, y=20)

    # Frame für die Eingabefelder
    eingabe_frame = customtkinter.CTkFrame(custom_window)
    eingabe_frame.place(x=350, y=50)

    x_label = customtkinter.CTkLabel(eingabe_frame, text="X:")
    x_label.place(x=0, y=0)
    x_var = StringVar()
    x_var.set("0")
    x_entry = customtkinter.CTkEntry(eingabe_frame, width=50, textvariable=x_var)
    x_entry.place(x=30, y=0)  # Auseinanderpositionierung

    y_label = customtkinter.CTkLabel(eingabe_frame, text="Y:")
    y_label.place(x=100, y=0)
    y_var = StringVar()
    y_var.set("0")
    y_entry = customtkinter.CTkEntry(eingabe_frame, width=50, textvariable=y_var)
    y_entry.place(x=130, y=0)  # Auseinanderpositionierung

    w_label = customtkinter.CTkLabel(eingabe_frame, text="w:")
    w_label.place(x=0, y=50)
    w_var = StringVar()
    w_var.set("100")
    w_entry = customtkinter.CTkEntry(eingabe_frame, width=50, textvariable=w_var)
    w_entry.place(x=30, y=50)  # Auseinanderpositionierung

    h_label = customtkinter.CTkLabel(eingabe_frame, text="h:")
    h_label.place(x=100, y=50)
    h_var = StringVar()
    h_var.set("100")
    h_entry = customtkinter.CTkEntry(eingabe_frame, width=50, textvariable=h_var)
    h_entry.place(x=130, y=50)  # Auseinanderpositionierung

    # Bild einfügen
    image_frame = customtkinter.CTkFrame(custom_window)
    image_frame.place(x=350, y=150)  # Neue Frame-Position

    # Hier soll das Bild eingefügt werden, passe den Dateipfad entsprechend an
    image_path = r".\Icons\icon_Abbildung.png"

    # Verwende PIL, um das Bild zu öffnen
    pil_image = PIL.Image.open(image_path)

    # Verkleinere das Bild (zum Beispiel um den Faktor 0.2)
    width, height = pil_image.size
    new_width = int(width * 0.2)
    new_height = int(height * 0.25)
    pil_image = pil_image.resize((new_width, new_height), PIL.Image.ANTIALIAS)

    # Konvertiere PIL Image zu PhotoImage
    tk_image = PIL.ImageTk.PhotoImage(pil_image)

    # Erzeuge ein Label und füge das Bild ein
    image_label = customtkinter.CTkLabel(image_frame, image=tk_image)
    image_label.place(x=0, y=0)

    color_label = customtkinter.CTkLabel(custom_window, text="FARBWERTE AUSLESEN")
    color_label.place(x=630, y=40)
    colorpicker = CTkColorPicker(custom_window, width=50)
    colorpicker.place(x=600, y=80)

    #root.mainloop()


#Funktion für die Settings der Bildtransformation und Objekterkennung#
def objekte_einstellungen(root):
    # CustomTkinter root window erzeugen und Einstellungen vornehmen
    #Erstellen eines Unterfensters
    custom_window = customtkinter.CTkToplevel(root)
    custom_window.title("BILDERKENNUNG UND OBJEKTSUCHE")
    custom_window.attributes('-topmost', 1) #Fenster in den Vordergrund holen
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    customtkinter.set_appearance_mode("dark")

    # Hauptfenster in der Bildschirmmitte positionieren
    screen_width = custom_window.winfo_screenwidth()
    screen_height = custom_window.winfo_screenheight()
    window_width = 680 # Breite des Fensters erhöht
    window_height = 280
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    custom_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Frame für die Objektauswahl
    objekt_frame = customtkinter.CTkFrame(custom_window, width=200, height=50)
    objekt_frame.place(x=50, y=50)

    objekt_label = customtkinter.CTkLabel(objekt_frame, text="Objekt:")
    objekt_label.place(x=0, y=0)

    # Dropdown-Liste mit den gewünschten Objekten
    # Laden der Liste aus den Einträgen der C_Objekterkennung
    listenrtrys = get_Suchoptionen_values()

    objekt_combobox = customtkinter.CTkComboBox(custom_window,values=listenrtrys )
    objekt_combobox.place(x=100, y=50)

    #Frame für die Auswahl vom YOLO Modell
    objekt_frame = customtkinter.CTkFrame(custom_window, width=600, height=50)
    objekt_frame.place(x=50, y=100)

    objekt_label = customtkinter.CTkLabel(objekt_frame, text="YOLO:")
    objekt_label.place(x=0, y=0)

    # Dropdown-Liste mit den gewünschten Modellen
    yolo_options = {
        0: 'YOLOv8n', 1: 'YOLOv8s', 2: 'YOLOv8m', 3: 'YOLOv8l', 4: 'YOLOv8x'
    }

    yolo_combobox = customtkinter.CTkComboBox(custom_window, values=list(yolo_options.values()))
    yolo_combobox.set("YOLOv8m")
    yolo_combobox.place(x=100, y=100)

    # Bild einfügen
    image_frame = customtkinter.CTkFrame(custom_window, width=600)
    image_frame.place(x=270, y=50)  # Neue Frame-Position

    # Anzeigebild laden - Yolo
    image_path = r".\Icons\icon_yolomodelle.png"

    # Verwende PIL, um das Bild zu öffnen
    pil_image = PIL.Image.open(image_path)

    # Verkleinere das Bild (zum Beispiel um den Faktor 0.2)
    width, height = pil_image.size
    new_width = int(width * 0.6)
    new_height = int(height * 0.6)
    pil_image = pil_image.resize((new_width, new_height), PIL.Image.ANTIALIAS)

    # Konvertiere PIL Image zu PhotoImage
    tk_image = PIL.ImageTk.PhotoImage(pil_image)

    # Erzeuge ein Label und füge das Bild ein
    image_label = customtkinter.CTkLabel(image_frame, image=tk_image)
    image_label.place(x=0, y=0)

    # Funktion für Frame eigenen OK-Button
    result = None
    def ok_button_click():
        result = objekt_combobox.get()
        print("Gewählt: " + result)
        custom_window.destroy()  # Fenster schließen

    objekte_button = customtkinter.CTkButton(custom_window, text="OK",command=lambda:ok_button_click())
    result = objekt_combobox.get(), yolo_combobox.get()
    objekte_button.place(x=20, y=200)  # 530
    custom_window.wait_window()  # Warte bis das Fenster geschlossen wird
    if result is None:
        result = ""
    return result

if __name__ == "__main__":
    # Die Funktion wird nur aufgerufen, wenn das Skript direkt ausgeführt wird
    standard_einstellungen()
    objekte_einstellungen()