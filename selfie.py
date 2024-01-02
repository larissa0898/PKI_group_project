import cv2
import numpy as np
import subprocess

#Funktion zum automatischen Installieren von Paketen die benötigt werden
def install_package(package_name):
    try:
        subprocess.check_call(["pip", "install", package_name])
    except subprocess.CalledProcessError:
        print(f"Error: Failed to install {package_name}.")

# Example usage:
package_to_install = "mediapipe"

try:
    import mediapipe as mp # Attempt to import the package
except ImportError:
    print(f"{package_to_install} is not installed. Installing...")
    install_package(package_to_install)
    import mediapipe as mp # Try to import it again

### Quelle: https://www.youtube.com/watch?v=9DiHbmLgitw (08:36 im Video zeigt Quellcode)

### Modifikation:
### Funktion
### Übergabe von Videoquelle und Hintergrund möglich
### Speichern eines Bildes als "selfie.jpg" wenn Taste s gedrückt wird
### Beenden wenn ESC gedrückt wird

def Hintergrund_Ausblendung(videoquelle=0, background_img_path=None, width=640, height=480):
    """ Funktion startet eine Livebild Anzeige in einem separaten Fenster. Der Hintergrund wird dabei durch einen
    beliebig anderen ersetzt.

    Erfordert:
    - Mediapipe
    - OpenCV
    - Numpy

    Parameter:
    videoquelle - default: 0 - integrierte Kamera
    background_img_path - Pfad der das Bild zum Hintergrund beinhaltet - ohne Angabe: schwarzer Hintergrund
    """
    segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)
    #Wenn der Pfad eines Hintergrundbildes übergeben wird, nutze dieses Bild
    if(background_img_path):
        background = cv2.imread(background_img_path)
    else:
        # Nutze ein leeres schwarzes Bild
        background = np.zeros((height, width, 3), dtype=np.uint8)
    #Abruf der Videodaten aus der übergebenen Quelle (Kamera)
    cap = cv2.VideoCapture(videoquelle)

    #Wenn die Quelle verfügbar ist und geöffnet werden konnte
    while cap.isOpened():
        #Zyklisches Lesen der Frames des Videostreams
        ret, frame = cap.read()
        height, width, channel = frame.shape

        #Wandlung des OpenCV BGR ind RGB Bild
        RGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        #Segmentierung des RGB Bildes
        results = segmentation.process(RGB)
        mask = results.segmentation_mask

        rsm = np.stack((mask,)*3, axis=-1)
        condition = rsm > 0.6
        condition = np.reshape(condition, (height,width,3))

        background = cv2.resize(background, (width,height))

        output = np.where(condition, frame,background)
        #Text in die Anzeige einfügen, damit der User die Tastenkürzel kennt
        osd_text1 = "s: Schnappschuss"
        osd_text2 = "ESC: Verlassen"
        output_with_text = output.copy()
        cv2.putText(output_with_text, osd_text1, (10, height - 50), cv2.FONT_HERSHEY_SIMPLEX, int(height / 400), [0, 255, 0],
                    int(height / 300))
        cv2.putText(output_with_text, osd_text2, (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, int(height / 400), [0, 255, 0],
                    int(height / 300))
        cv2.imshow('Selfie Live', output_with_text)

        k = cv2.waitKey(30) & 0xFF
        if k == (27): #ESC
            cap.release()
            cv2.destroyWindow("Selfie Live")
            break

        elif k == ord('s'):
            success=cv2.imwrite("selfie.jpg",output)
            output_with_text = ""
            if success:
                output_with_text = "Gespeichert unter selfie.jpg"
            else:
                output_with_text = "ERR - nicht gespeichert"
            img_output_mit_text = output.copy()
            cv2.putText(img_output_mit_text, output_with_text, (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, int(height / 400),
                        [0, 255, 0], int(height / 300))
            cv2.imshow("Selfie",output)

    output = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
    return(output)

if __name__ == "__main__":
    Hintergrund_Ausblendung()

