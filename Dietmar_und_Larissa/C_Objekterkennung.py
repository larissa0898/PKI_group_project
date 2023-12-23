# Hier Objekterkennung abbilden #

import random
import os
import cv2
import numpy as np
from ultralytics import YOLO

# QUELLE der Grundlage: https://github.com/ultralytics/ultralytics/issues/561


#Modifikationen:
# Deutsch
# Suche nach Bildinhalten
# Durchsuchen von Ordnern nach Bildern mit bestimmten Objekten

Klassen_Namen = {0: 'Person', 1: 'Fahrrad', 2: 'Auto', 3: 'Motorrad', 4: 'Flugzeug', 5: 'Bus', 6: 'Zug', 7: 'LKW',
                 8: 'Boot', 9: 'Ampel', 10: 'Feuerhydrant', 11: 'Stoppschild', 12: 'Parkuhr', 13: 'Bank', 14: 'Vogel',
                 15: 'Katze', 16: 'Hund', 17: 'Pferd', 18: 'Schaf', 19: 'Kuh', 20: 'Elefant', 21: 'Bär', 22: 'Zebra',
                 23: 'Giraffe', 24: 'Rucksack', 25: 'Regenschirm', 26: 'Handtasche', 27: 'Krawatte', 28: 'Koffer',
                 29: 'Frisbee', 30: 'Skier', 31: 'Snowboard', 32: 'Sportball', 33: 'Drachen', 34: 'Baseballschläger',
                 35: 'Baseballhandschuh', 36: 'Skateboard', 37: 'Surfbrett', 38: 'Tennisschläger', 39: 'Flasche',
                 40: 'Weinglas', 41: 'Tasse', 42: 'Gabel', 43: 'Messer', 44: 'Löffel', 45: 'Schüssel', 46: 'Banane',
                 47: 'Apfel', 48: 'Sandwich', 49: 'Orange', 50: 'Brokkoli', 51: 'Karotte', 52: 'Hot Dog', 53: 'Pizza',
                 54: 'Donut', 55: 'Kuchen', 56: 'Stuhl', 57: 'Couch', 58: 'Topfpflanze', 59: 'Bett', 60: 'Esstisch',
                 61: 'Toilette', 62: 'Fernseher', 63: 'Laptop', 64: 'Maus', 65: 'Fernbedienung', 66: 'Tastatur',
                 67: 'Handy', 68: 'Mikrowelle', 69: 'Ofen', 70: 'Toaster', 71: 'Spülbecken', 72: 'Kühlschrank',
                 73: 'Buch', 74: 'Uhr', 75: 'Vase', 76: 'Schere', 77: 'Teddybär', 78: 'Haartrockner', 79: 'Zahnbürste'}



def get_Suchoptionen():
    return(list(Klassen_Namen.values()))

#Suche nach Bildern in einem übergeben Verzeichnis
#Rückgabe als Liste
def find_images(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff']

    image_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file_path)

    return image_files

def Suche_Bilinhalt(model, suchobjekt, suchordner=""):
    gefundene_bilder_Objektliste = {}
    gefundene_bilderliste = find_images(suchordner)
    counter = 0
    for bild in gefundene_bilderliste:
        counter += 1
        img = cv2.imread(bild)
        results = model.predict(img, stream=False)

        # Für jedes erkannte Objekt
        for r in results:
            boxes = r.boxes  # Boxes object for bbox outputs
            masks = r.masks  # Masks object for segment masks outputs
            probs = r.probs  # Class probabilities for classification outputs

            detection_count = r.boxes.shape[0]

            # Ermittlung der gefundenen Objekte
            for i in range(detection_count):
                cls = int(r.boxes.cls[i].item())
                name = Klassen_Namen[cls]#r.names[cls]
                #print("Objekt Preview: " + name)
                # Zählung der erkannten Objekte per Dictionary
                print("Name: "+name + " Sucheobjekt: "+suchobjekt)
                if name == suchobjekt:
                    print("Ist enthalten")
                    confidence = float(r.boxes.conf[i].item())
                    print("Objekt: " + name + " " + str(confidence))
                    gefundene_bilder_Objektliste[counter]=(bild,confidence)

    return(gefundene_bilder_Objektliste)

def overlay(image, mask, color, alpha, resize=None):
    """Combines image and its segmentation mask into a single image.
        QUELLE: https://github.com/ultralytics/ultralytics/issues/561
    Params:
        image: Training image. np.ndarray,
        mask: Segmentation mask. np.ndarray,
        color: Color for segmentation mask rendering.  tuple[int, int, int] = (255, 0, 0)
        alpha: Segmentation mask's transparency. float = 0.5,
        resize: If provided, both image and its mask are resized before blending them together.
        tuple[int, int] = (1024, 1024))

    Returns:
        image_combined: The combined image. np.ndarray

    """
    # color = color[::-1]
    colored_mask = np.expand_dims(mask, 0).repeat(3, axis=0)
    colored_mask = np.moveaxis(colored_mask, 0, -1)
    masked = np.ma.MaskedArray(image, mask=colored_mask, fill_value=color)
    image_overlay = masked.filled()

    if resize is not None:
        image = cv2.resize(image.transpose(1, 2, 0), resize)
        image_overlay = cv2.resize(image_overlay.transpose(1, 2, 0), resize)

    image_combined = cv2.addWeighted(image, 1 - alpha, image_overlay, alpha, 0)

    return image_combined


def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    '''Funktion zum Zeichnen einer Box und eines Labels in das Bild
    QUELLE: https://github.com/ultralytics/ultralytics/issues/561'''
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def Yolo_run(img, model, background=None, segment_out_path=None):
    '''Funktion zur Detektion und Markierung von klassifizierten Objekten
    QUELLE: https://github.com/ultralytics/ultralytics/issues/561
    modifiziert und erweitert'''
    erkannte_Objekte = {}

    img_orig = out_img = img.copy()
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in Klassen_Namen]
    #Speichern der Bildgröße in Variablen für Höhe h und Breite w
    h, w, _ = img.shape

    # YOLO Objekterkennung durchführen
    results = model.predict(img, stream=False)

    # Für jedes erkannte Objekt Boxen, Masken für Segmente und Klassen übernehmen
    for r in results:
        #print("PROBS: ",r.probs)
        boxes = r.boxes  # Boxes object for bbox outputs
        masks = r.masks  # Masks object for segment masks outputs
        probs = r.probs  # Class probabilities for classification outputs

        detection_count = r.boxes.shape[0]

        #Ermittlung der gefundenen Objekte
        for i in range(detection_count):
            cls = int(r.boxes.cls[i].item())
            name = Klassen_Namen[cls]

            #Zählung der erkannten Objekte per Dictionary
            if name in erkannte_Objekte:
                erkannte_Objekte[name] += 1
            else:
                erkannte_Objekte[name] = 1

            confidence = float(r.boxes.conf[i].item())
            print("Objekt: "+name+" "+str(confidence))

    mask_counter = 0
    if masks is not None:
        masks = masks.data.cpu()
        for seg, box in zip(masks.data.cpu().numpy(), boxes):

            # Segment auf Hintergrund anpassen
            seg = cv2.resize(seg, (w, h))

            # ----
            # Einblendung der Segmentierung im Bild
            if background is None:
                img = overlay(img, seg, colors[int(box.cls)], 0.5)
            else:
                img = overlay(img, seg, colors[int(box.cls)], 0.7)

            # Erzeuge ein leeres Bild für die Maske und fülle dieses
            blank_image = np.zeros((h, w, 3), dtype=np.uint8)
            blank_image_seg = overlay(blank_image, seg, (255, 255, 255), 1.0)
            result_image = cv2.bitwise_and(blank_image_seg, img_orig)

            xmin = int(box.data[0][0])
            ymin = int(box.data[0][1])
            xmax = int(box.data[0][2])
            ymax = int(box.data[0][3])

            # Bildausschnitt
            ausschnitt = result_image[ymin: ymax, xmin: xmax]
            mask_counter += 1

            # Wenn ein Pfad übergeben wird, soll das Bild auch gespeichert werden:
            if segment_out_path is not None:
                cv2.imwrite("segment_out_path_" + str(mask_counter) + ".jpg", ausschnitt)

            if background is not None:
                # Segment einem neuen Hintergrund hinzufügen:
                background = cv2.resize(background, (w, h))

                # Bild invertieren
                inv_backgroundmask = cv2.bitwise_not(blank_image_seg)

                # Bild maskieren
                background_masked = cv2.bitwise_and(inv_backgroundmask, background)

                # Bildausschnitt einfügen
                img_out2 = cv2.bitwise_or(result_image, background_masked)

                # Größe anpassen
                out_img = cv2.resize(img_out2, (w, h))

                plot_one_box([xmin, ymin, xmax, ymax], img, colors[int(box.cls)],
                             f'{Klassen_Namen[int(box.cls)]} {float(box.conf):.3}')

                out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)

            else:
                out_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #Wandlung der Klassen + Anzahl in Text
    text_labels =""
    for word, count in erkannte_Objekte.items():
        text_labels += " " + word + ": " + str(count)

    cv2.putText(out_img, text_labels, (10,h-50), cv2.FONT_HERSHEY_SIMPLEX,int(h/500), [0, 255, 0], int(h/250))

    return (out_img)


###
#Funktion zum Testen des Moduls
###
if __name__ == "__main__":
    model = YOLO("yolov8m-seg.pt")
    ergenbnis = Suche_Bilinhalt(model,'Person',"C:\Temp\Bilder")
    for key, value in ergenbnis.items():
        bild, confidence = value
        print(f"Eintrag Nr.: {key}: Bild: = {bild}, Übereinstimmung: = {confidence}")
