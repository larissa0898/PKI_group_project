########################### BIBLIOTHEKEN LADEN #########################
import dearpygui.dearpygui as dpg
import sys
import os
import cv2

########################################################################
########################### FUNKTIONSAUFRUFE ###########################
########################################################################

def print_me(sender):
    print(f"Datei: {sender}")

def color_me(sender):
    if sender == color_picker_id:  # Überprüfe, ob der Aufruf vom Color Picker kommt
        current_image_path = dpg.get_value("##ImageLabel").replace("Aktuelles Bild: ", "")
        selected_color = dpg.get_value(sender)
        print(f"Ausgewählte Farbe: {selected_color} für das Bild: {current_image_path}")
def close_program(sender):
    print("Programm wird geschlossen.")
    dpg.destroy_context()
    sys.exit()
def callback(sender, app_data, user_data):
    print("Sender: ", sender)
    assert isinstance(app_data, object)
    print("App Data: ", app_data)
def show_info_dialog():
    with dpg.handler_registry():
        with dpg.window(label=" ",pos=(460,50), width=280, height=260):
            dpg.add_text("BILDBEARBEITUNG UND BILDANALYSE")
            dpg.add_separator()
            dpg.add_spacing(count=4)  # Leerzeile
            dpg.add_text("Entwicklerteam Gruppe a1-1:")
            dpg.add_spacing(count=3)  # Leerzeile
            dpg.add_text("Al-Atrash, Anas Abdelsaman Ramadan")
            dpg.add_spacing(count=1)
            dpg.add_text("Balczukat, Phil")
            dpg.add_spacing(count=1)
            dpg.add_text("Ferme, Larissa")
            dpg.add_spacing(count=1)
            dpg.add_text("Koch, Claus-Peter")
            dpg.add_spacing(count=1)
            dpg.add_text("Ysop, Dietmar")
            dpg.add_spacing(count=3)
def show_version_dialog():
    with dpg.handler_registry():
        with dpg.window(label=" ",pos=(460,50), width=280, height=160):
            dpg.add_text("BILDBEARBEITUNG UND BILDANALYSE")
            dpg.add_separator()
            dpg.add_spacing(count=4)  # Leerzeile
            dpg.add_text("Programmversion 3.0")
            dpg.add_spacing(count=1)
            dpg.add_text("(c) 2024")
            dpg.add_spacing(count=3)
def save_file_callback(sender):
    file_path = dpg.save_file_dialog()
    if file_path:
        print(f"Datei speichern: {file_path}")
def save_file_as_callback(sender):
    file_path = dpg.save_file_dialog()
    if file_path:
        print(f"Datei speichern unter: {file_path}")
        # Hier könntest du die Logik für das Speichern des aktuellen Bildes an einem anderen Ort implementieren

def print_callback(sender):
    # Hier öffnen wir den Druckdialog
    dpg.show_tool(dpg.mvTool_Print)

def show_properties_callback(sender):
    current_image_path = dpg.get_value("##ImageLabel").replace("Aktuelles Bild: ", "")
    if current_image_path:
        file_size = os.path.getsize(current_image_path)
        file_size_kb = file_size / 1024.0  # Konvertiere Bytes in Kilobytes

        image = cv2.imread(current_image_path)
        image_height, image_width, _ = image.shape

        properties_text = (
            f"Dateipfad: {current_image_path}\n"
            f"Dateigröße: {file_size_kb:.2f} KB\n"
            f"Bildbreite: {image_width}px\n"
            f"Bildhöhe: {image_height}px"
        )

def load_image_callback(sender):
    dpg.add_file_dialog(directory_selector=True, show=False, callback=callback, id="file_dialog_id", width=800, height=600)
    dpg.add_file_extension("", color=(150, 250, 150, 255), parent="file_dialog_id")
    dpg.add_file_extension("Source files (*.jpg *.png *.bmp){.jpg,.png,.bmp}", color=(0, 255, 255, 255), parent="file_dialog_id")
    dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]", parent="file_dialog_id")
    dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]", parent="file_dialog_id")

def update_image_texture(image_path):
    texture_id = dpg.get_item_info(id="file_dialog_id")['children'][0]
    texture_data = cv2.imread(image_path)
    dpg.set_value(texture_id, texture_data)

#############################################################################
########################### FUNKTIONSAUFRUFE ENDE ###########################
#############################################################################

# Dear PyGui-Context erstellen
dpg.create_context()

# Hauptfenster (Viewport) erstellen und Parameter Titel, Größe und Hintergrund festlegen
dpg.create_viewport(title="BILDBEARBEITUNG UND BILDANALYSE", width=1200, height=950, x_pos=(400), y_pos=(10), clear_color=(234, 234, 213, 255))

# Menüleiste erstellen
with dpg.viewport_menu_bar():
    with dpg.menu(label="Datei"):
        dpg.add_menu_item(label="Datei öffnen", callback=load_image_callback)
        dpg.add_menu_item(label="Datei speichern", callback=save_file_callback)
        dpg.add_menu_item(label="Datei speichern unter", callback=save_file_as_callback)
        dpg.add_separator()
        dpg.add_menu_item(label="Datei schließen", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="PDF Drucken", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Eigenschaften", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Ende", callback=close_program)

    with dpg.menu(label="Bearbeiten"):
        dpg.add_menu_item(label="Reset / Default", callback=print_me)

    with dpg.menu(label="Einstellungen"):
        dpg.add_menu_item(label="Standardeinstellungen", callback=print_me)
        dpg.add_menu_item(label="Erweiterte Einstellungen", callback=print_me)
        dpg.add_menu_item(label="Bildtransformation", callback=print_me)
        dpg.add_menu_item(label="OCR und Video", callback=print_me)

    with dpg.menu(label="Color Picker"):
        dpg.add_color_picker(label="Color Me", callback=color_me)

    with dpg.menu(label="Info"):
        dpg.add_menu_item(label="Hilfe", callback=print_me)
        dpg.add_menu_item(label="Entwicklerteam", callback=show_info_dialog)
        dpg.add_menu_item(label="Programmversion", callback=show_version_dialog)

# Zusätzliches Image Viewer-Fenster
with dpg.window(label="Bildanzeige", pos=(20, 50), width=750, height=800, no_title_bar=True):
    dpg.add_image(parent="file_dialog_id", texture_tag=2, width=750, height=800)

#Fenster, um die Bedienung vorzunehmen
with dpg.window(label="Bedienung", pos=(825,50), width=320, height=800, no_title_bar=True):
    dpg.add_text("Bedienungselemente")
    with dpg.group(pos=(20, 50), width=50, height=50):
        dpg.add_text('Standardfunktionen')
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)

    # Bereich für erweiterte Funktionen rechts
    with dpg.group(pos=(20, 200), width=50, height=50):
        dpg.add_text("Erweiterte Funktionen")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

    # Bereich für Bilderkennung und -transformation
    with dpg.group(pos=(20, 350), width=50, height=50):
        dpg.add_text("Bilderkennung und -transformation")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

    # Bereich für Video Features
    with dpg.group(pos=(20, 500), width=50, height=50):
        dpg.add_text("Video Features")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

    # Bereich für OCR Erkennung
    with dpg.group(pos=(20, 650), width=50, height=50):
        dpg.add_text("OCR Erkennung")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

# Dear PyGui initialisieren und starten
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Dear PyGui-Context zerstören
dpg.destroy_context()
