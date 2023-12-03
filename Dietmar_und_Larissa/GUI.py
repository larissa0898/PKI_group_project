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

# Hauptfenster (Viewport) erstellen und Größe setzen
viewport_title = 'Bildbearbeitung und Bildanalyse'
viewport_width, viewport_height = 1200, 1000
dpg.create_viewport(title=viewport_title, width=viewport_width, height=viewport_height)

# Fenster in der Mitte des Bildschirms positionieren (ohne genaue Größenabfrage)
dpg.set_viewport_pos(pos=(400, 10))  # Position relativ zum Hauptbildschirm

# Hintergrundfarbe des Hauptfensters setzen (optional)
dpg.set_viewport_clear_color(color=(234,234,213,255))  # Parameter Hintergrund setzen

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
        dpg.add_checkbox(label="Pick Me", callback=print_me)
        dpg.add_button(label="Press Me", callback=print_me)
        dpg.add_color_picker(label="Color Me", callback=print_me)

    with dpg.menu(label="Info"):
        dpg.add_menu_item(label="Hilfe", callback=print_me)
        dpg.add_menu_item(label="Programmversion", callback=print_me)

# Bereich für Standardsettings rechts oben
with dpg.group(pos=(900, 20), width=280):
    dpg.add_text("Standardsettings")
    dpg.add_checkbox(label="Option 1", default_value=True)
    dpg.add_slider_float(label="Einstellung 1", default_value=0.5, max_value=1.0)

# Dear PyGui initialisieren und starten
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Dear PyGui-Context zerstören
dpg.destroy_context()