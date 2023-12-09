import cv2
from tkinter import filedialog

f_types = [('JPEG Files', '*.jpg'), ('PNG Files', '*.png'), ('BMP Files', '*.bmp')]
filename = filedialog.askopenfilename(filetypes=f_types)

img = cv2.imread(filename)
#img = cv2.flip(img, 0)

def savefile():
    # filename from beginning (openfiledialog)
    if filename:
        cv2.imwrite(filename, img)

def savefileas():
    file = filedialog.asksaveasfilename(defaultextension=".*",filetypes = f_types) #mode='w', defaultextension=".jpeg"
    if file:
        cv2.imwrite(file, img)

#savefile()
#savefileas()