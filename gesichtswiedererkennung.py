from pathlib import Path
import cv2
import numpy as np
import json
from pathlib import Path
import os
import einstellungen


GesDatenbank_Datei = r"/GesichtDatenbank.xml"
GesLabel_Datei= r"/GesichtDatenbank_label.json"
FACE_FACT = 150

#Suche nach Bildern in einem übergeben Verzeichnis
#Rückgabe als Liste
#Quelle: ChatGPT 3.5
def find_images(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff']
    image_files = []
    print("Ordner: "+directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file_path)

    return image_files

def Suche_Bildinhalt_Bekannte_Gesichter(suchobjekte ,model_label, suchordner=""):
    '''Suche nach Bildern mit bekannten Personend
    Übergabeparameter:
    - Trainiertes Model
    - Verzeichnis mit Bildern das durchsucht werden soll
    - Suchobjekte


    Rückgabe:
    - Anzahl gefundener bekannter Personen
    - Liste mit Dateipfaden bekannter Personen
    '''
    gefundene_bilder_Gesichter = {}
    gefundene_bilderliste = find_images(suchordner)
    counter = 0
    for bild in gefundene_bilderliste:
        counter += 1

        img,img_path,name,confidence = Gesichtswiedererkennung(suchobjekte, bild, model_label)

        if(img is not None) and (float(confidence)>50):
            gefundene_bilder_Gesichter[counter]=(bild,confidence)
            print("Bekanntes Gesicht gefunden")

    return(counter,gefundene_bilder_Gesichter)



'''Funktion zum Testen der Gesichtswiedererkennung - Hier Bildanzeige'''
def display_image_center(image, window_name='Image Window'):

    # Get screen dimensions
    screen_width = 1920  # Set your screen width
    screen_height = 1080  # Set your screen height

    # Get image dimensions
    img_height, img_width = image.shape[:2]

    # Calculate the position to center the window
    x_position = max(0, int((screen_width - img_width) / 2))
    y_position = max(0, int((screen_height - img_height) / 2))

    # Display the image
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, x_position, y_position)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Gesichtswiedererkennung_Trainieren(data_folder_in,save_file_path_in):
    '''Funktion zum Trainieren von Gesichtern
    - 1. Parameter: Pfad zu den Ordnern mit Gesichtern zum Erlernen. Der Name des Ordners wird als Label verwendet
    - 2. Parameter: Speicherpfad für die erlernte Gesichtsdatenbank
    - Rückgabe:
    - 1. Parameter: Trainiertes Modell
    - 2. Parameter: Dictionary mit Labeln der Gesichter
    '''
    images = []
    labels = []
    label_map = {}
    current_label = 1
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("Folder Data: " + data_folder_in)
    print("Folder Save: " + save_file_path_in)
    try:
        for person_folder in Path(data_folder_in).iterdir():
            if person_folder.is_dir():
                label_map[current_label] = str(person_folder.name)
                counter = 0
                for image_path in person_folder.glob('*.jpg'):
                    print("Bildpfad: "+str(image_path))
                    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

                    # Gesichtserkennung im Bild, auf Basis von Haarcascade default Werten für Frontale Gesichter
                    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))
                    if faces is not None:
                        print("Gesicht erkannt")
                    # Vergleichen der gefundenen Gesichter mit bekannten Gesichtern die angelernt wurden

                    confidence = None

                    for (x, y, w, h) in faces:
                        counter += 1
                        face_roi = img[y:y + h, x:x + w]
                        # Einheitlich in der Größe skalieren
                        face_roi = cv2.resize(face_roi, (FACE_FACT, int((h / w) * FACE_FACT)))
                        #cv2.imshow("I" + str(counter)+str(current_label), face_roi)

                        images.append(face_roi)
                        labels.append(current_label)

                #print("Label Anz.: "+str(current_label))
            else:
                print("Kein gültiges Verzeichnis")
            current_label += 1
    except Exception as err:
        print(err)

    #Standard Gesichtserkennung von OpenCV initialisieren und trainieren
    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=90)
    recognizer.train(images, np.array(labels))

    # Speichern des trainierten Modells unter dem angegebenen Pfad
    recognizer.save(save_file_path_in+GesDatenbank_Datei)
    with open(save_file_path_in+GesLabel_Datei, 'w') as file:
        json.dump(label_map, file)
        file.close()
        print("Datei erfolgreich gespeichert")
    return recognizer, label_map


def Lade_TrainiertesModell(save_file_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=90)
    recognizer.read(save_file_path+GesDatenbank_Datei)
    file_path_map = save_file_path+GesLabel_Datei
    with open(file_path_map, 'r') as file:
        label_map_load = json.load(file)
        file.close()
    return recognizer, label_map_load

def Gesichtswiedererkennung(trained_recognizer,image_path,label_map_loaded):
    '''Funktion zum erkennen von Gesichtern in Bildern
    1.Prameter: Vortrainierte Gesichtserkennung mit bekannten Gesichtern
    2.Parameter: Pfad zum Original-Bild in dem nach bekannten Gesichtern gesucht werden soll
    3.Parameter: Label der bekannten Gesichter für Anzeigetext
    Rückgabe:
    1. Parameter: Bild mit gekennzeichneten bekannten Personen
    '''
    anz_wiedererkannte_pers = 0
    for key, value in label_map_loaded.items():
        print(f'{key}: {value}')
    print("Pfad des Bildes: "+image_path)
    img = cv2.imread(image_path)
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Starte Erkennung")
        #Gesichtserkennung im Bild, auf Basis von Haarcascade default Werten für Frontale Gesichter
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

        #Vergleichen der gefundenen Gesichter mit bekannten Gesichtern die angelernt wurden
        counter = 0
        confidence = None

        for (x, y, w, h) in faces:
            counter+=1
            face_roi = gray[y:y + h, x:x + w]
            #Einheitlich in der Größe skalieren
            face_roi = cv2.resize(face_roi,(FACE_FACT,int((h/w)*FACE_FACT)))
            cv2.imshow("I"+str(counter),face_roi)
            try:
                #Prüfung der Übereinstimmung und Genauigkeit
                label, confidence = trained_recognizer.predict(face_roi)
                if label == -1:
                    print("Unbekannte Gesichter ")
                    continue
                else:
                    #print("Bekanntes Gesicht")
                    print("Person: ", label)
                    print("Confidence: ", confidence)
            except Exception as err3:
                print("ERR-Trained Recognition: ", err3)

            try:
                #Wenn das Gesicht dem einer angelernten Person entspricht:
                if (confidence is not None) and (confidence < 100):
                    person_name = label_map_loaded[str(label)]
                    print("Person :" +person_name)
                    print("Confidence: " + str(confidence))
                    anz_wiedererkannte_pers+=1
                    #Markierung der Gesichter mit Rechteck, Name und Übereinstimmungsgrad
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(img, f'{person_name} ({confidence:.2f}%)', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 0, 255), 2)
                else:
                    person_name = "Unknown"
            except:
                print("ERROR - Auswertung Gesichtswiedererkennung")
    else:
        print("Bild konnte nicht geladen werden!")

    #Falls kein bekanntes Gesicht dabei ist:
    if(anz_wiedererkannte_pers==0):
        img = None
        image_path = None
        person_name = None
        confidence = None

    out_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return(out_img,image_path,person_name,confidence)

if __name__ == "__main__":
    global label_map
    data_folder = Path(r"/known")
    file_path_map = r"./Gesichtswiedererkennung/known/ElonMusk"
    file_path_training = r"./Gesichtswiedererkennung/training/ElonMusk/"
    file_path_known = r"./Gesichtswiedererkennung/known/ElonMusk/"
    test_image_path = r"./Gesichtswiedererkennung/search/ElonMusk_Gruppe.jpg"
    try:

        recognizer, label_map = Gesichtswiedererkennung_Trainieren(data_folder,file_path_training)
        print("Training done")
        #Speichern der trainierten Label Daten in einer JSON Datei
        with open(file_path_map,'w') as file:
            json.dump(label_map, file)
            file.close()
            print("Datei gespeichert")
        try:
            #Laden der trainierten Label Daten aus einer JSON Datei
            trained_recognizer, label_map_load = Lade_TrainiertesModell(file_path_training)

            #Test mit bekannten Bildern auf Basis der bekannten Gesichtsdatenbank

            img = Gesichtswiedererkennung(trained_recognizer,test_image_path, label_map_load)
            cv2.imshow('Erkannte Gesichter',img)

        except Exception as err2:
            print("Error: ",err2)

    except Exception as err1:
        print("exception:", err1)

    print("Programm Ende")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
