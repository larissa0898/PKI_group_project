import dearpygui.dearpygui as dpg
import sys
def print_me(sender):
    print(f"Datei: {sender}")

def close_program(sender):
    print("Programm wird geschlossen.")
    dpg.destroy_context()
    sys.exit()

# Dear PyGui-Context erstellen
dpg.create_context()

# Hintergrundfarbe definieren (im Bereich von 0 bis 1 für jeden Kanal)
background_color = (234 / 255.0, 234 / 255.0, 213 / 255.0, 1.0)

# Hauptfenster (Viewport) erstellen und Parameter Titel, Größe und Hintergrund übernehmen
dpg.create_viewport(title="Bildbearbeitung und Bildanalyse", width=1200, height=1000, clear_color=background_color)

# Fenster in der Mitte des Bildschirms positionieren (ohne genaue Größenabfrage)
dpg.set_viewport_pos(pos=(400, 10))  # Position relativ zum Hauptbildschirm

# Hintergrundfarbe des Hauptfensters setzen (optional)
dpg.set_viewport_clear_color(color=(234, 234, 213, 255))  # Parameter Hintergrund setzen

# Menüleiste erstellen
with dpg.viewport_menu_bar():
    with dpg.menu(label="Datei"):
        dpg.add_menu_item(label="Datei öffnen")
        dpg.add_menu_item(label="Datei speichern", callback=print_me)
        dpg.add_menu_item(label="Datei speichern unter", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Datei schließen", callback=print_me)
        dpg.add_menu_item(label="Zuletzt verwendet", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Drucken", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Eigenschaften", callback=print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Ende", callback=close_program)

    with dpg.menu(label="Bearbeiten"):
        dpg.add_menu_item(label="Rückgängig", callback=print_me)

    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Setting 1", callback=print_me)
        dpg.add_menu_item(label="Setting 1", callback=print_me)
        dpg.add_menu_item(label="Setting 1", callback=print_me)
        dpg.add_menu_item(label="Setting 1", callback=print_me)
        dpg.add_menu_item(label="Setting 1", callback=print_me)

    with dpg.menu(label="Color Picker"):
        dpg.add_color_picker(label="Color Me", callback=print_me)

    with dpg.menu(label="Info"):
        dpg.add_menu_item(label="Hilfe", callback=print_me)
        dpg.add_menu_item(label="Programmversion", callback=print_me)

with (dpg.window(tag="Primary Window")):

    # Bereich für Standardfunktionen rechts
    with dpg.group(pos=(700, 50), width=50, height=50):
        dpg.add_text('Standardfunktionen')
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)
            dpg.add_button(label="Button", callback=print_me, width=50, height=50)

    # Bereich für Erweiterte Funktionen rechts
    with dpg.group(pos=(700, 200), width=50, height=50):
        dpg.add_text("Erweiterte Funktionen")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

    # Bereich für Bilderkennung und -transformation
    with dpg.group(pos=(700, 350), width=50, height=50):
        dpg.add_text("Bilderkennung und -transformation")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

    # Bereich für Video Features
    with dpg.group(pos=(700, 500), width=50, height=50):
        dpg.add_text("Video Features")
        dpg.add_separator()  # Trennlinie einfügen
        with dpg.group(horizontal=True, horizontal_spacing=5):  # Buttons nebeneinander anordnen
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)
            dpg.add_button(label="Button", callback=print_me)

    # Bereich für OCR Erkennung
    with dpg.group(pos=(700, 650), width=50, height=50):
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
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()

# Dear PyGui-Context zerstören
dpg.destroy_context()