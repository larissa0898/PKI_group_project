# Hier Standardfunktionen abbilden #
import cv2

# function to rotate the image by an angle
def rotate_img(img, angle):
    # Get size (# of rows and columns) of image
    rows, cols = img.shape[:2]
    # Create Rotation matrix
    # ..center = center point of rotation --> Middle point of image
    # ..angle = user defined rotation angle
    # ..scale = scaling factor --> always =1 for this method
    rot_Mat = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    # Apply rotation matrix with target image size = original size
    return cv2.warpAffine(img, rot_Mat, (cols, rows))
    #return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# function to scale the image by a factor
def scale_img(img, sfactor):
    # Get size (# of rows and columns) of image
    rows, cols = img.shape[:2]
    # set new size as integer
    new_size = (int(cols * sfactor), int(rows * sfactor))
    return cv2.resize(img, new_size)

# function to mirror the image horizontally
def mirror_img_h(img):
    # flipcode 1 = horizontal
    return cv2.flip(img, 1)

# function to mirror the image horizontally
def mirror_img_v(img):
    # flipcode 0 = vertical
    return cv2.flip(img, 0)

# Transform image to greyscale
def grayscale_img(img):
    # cv2.COLOR_BGR2GRAY = python color2gray code
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Crop image...interactive???
def crop_img(img, x, y, w, h):
    # ..x,y = Start-Position of cropped image
    # ..w,h = width and height of cropped image starting from x,y coordinates
    # use slicing-syntax to get sector from image
    return img[y:y+h, x:x+w]

# Add a frame to image
# Verbesserungsideen: Drop-Down-Feld für Border-Styles und Farbskala für Farbe zum Auswählen
def add_frame(img, thickness, color):
    # ..thickness = thickness of frame TOP, BOTTOM, LEFT, RIGHT --> use the same value in all directions
    # ..cv2.BORDER = Framestyle
    return cv2.copyMakeBorder(img, thickness, thickness, thickness, thickness, cv2.BORDER_ISOLATED, value=color)