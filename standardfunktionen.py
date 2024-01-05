# Disclaimer von P. Balczukat
# Die hier definierten Funktionen wurden von mir vollständig selbst entwickelt.
# Beim "Finden" der richtigen Methoden aus der CV2 Bibliothek (opencv)
# habe ich mir von ChatGPT und Stackoverflow auf die Sprünge helfen lassen

# Hier Standardfunktionen abbilden #
import cv2

# Globale Variablen mit Default-Werten
# werden im 0_GUI.py beim Funktionsaufruf genutzt und via Dialog vom Nutzer manipuliert
rotation_angle = 90 #°
scale_factor = 0.5 # factor
cut_x_pos = 0 #px
cut_y_pos = 0 #px
cut_width = 300 #px
cut_height = 300 #px
frame_thickness = 20 #pt
frame_color = (0, 200, 0) # RGB Tupel

# function to rotate the image by an angle
def rotate_img(img, angle):
    # Get size (# of rows and columns) of image
    rows, cols = img.shape[:2]
    # Create Rotation matrix
    # ...center = center point of rotation --> Middle point of image
    # ...angle = user defined rotation angle
    # ...scale = scaling factor --> always =1 for this method
    rot_Mat = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    # Apply rotation matrix with target image size = original size
    return cv2.warpAffine(img, rot_Mat, (rows, cols))
    #return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# function to scale the image by a given factor
def scale_img(img, sfactor):
    # Get size (# of rows and columns) of image
    rows, cols = img.shape[:2]
    # set new size as integer
    new_size = (int(cols * sfactor), int(rows * sfactor))
    return cv2.resize(img, new_size)

# function to mirror the image vertically
def mirror_img_v(img):
    # flipcode 1 = horizontal
    return cv2.flip(img, 1)

# function to mirror the image horizontally
def mirror_img_h(img):
    # flipcode 0 = vertical
    return cv2.flip(img, 0)

# Transform image to greyscale
def grayscale_img(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Crop image...interactive???
def crop_img(img, x, y, w, h):
    # ...x,y = Start-Position of cropped image
    # ...w,h = width and height of cropped image starting from x,y coordinates
    # use slicing-syntax to get sector from image
    return img[y:y+h, x:x+w]

# Add a frame to image
def add_frame(img, thickness, color):
    # ...thickness = thickness of frame TOP, BOTTOM, LEFT, RIGHT --> use the same value in all directions
    # ...cv2.BORDER = Framestyle (bold frame)
    return cv2.copyMakeBorder(img, int(thickness), int(thickness), int(thickness), int(thickness), cv2.BORDER_ISOLATED, value=color)