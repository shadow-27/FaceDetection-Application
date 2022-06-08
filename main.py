import io
import os
import subprocess
from tkinter import *
from tkinter import filedialog

import numpy
from PIL import ImageTk, Image

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 620
LEFT_PANEL_WIDTH = 200
IMAGE_PANEL_WIDTH = 500
IMAGE_PANEL_HEIGHT = 600
SCALE_FACTOR = 1.5
BACKGROUND_COLOR = "#460669"
CONTRAST_COLOR="#e3c1f5"
FONT_COLOR = "white"

folderPath = ''
results = ''


def checkIfItsJpg(fileName):
    # convert to jpg if png
    if fileName[fileName.rfind('.') + 1:] != "jpg":
        tmpImage = Image.open(folderPath[folderPath.rfind('/') + 1:] + '\\' + fileName)
        fileName = 'tmp\\' + fileName[: fileName.rfind('.') + 1] + 'jpg'
        tmpImage.save(folderPath[folderPath.rfind('/') + 1:] + '\\' + fileName)
        return fileName
    return fileName


def cursorSelect(evt):
    global results
    # reset the canvases to null
    middlePanelCanvas.delete("all")
    rightPanelCanvas.delete("all")

    value = leftPanelListBox.get(leftPanelListBox.curselection())
    resizedImage = resizeImage(Image.open(folderPath + '/' + value))
    middlePanelCanvas.create_image(0, 0, image=resizedImage, anchor=NW)
    middlePanelCanvas.image = resizedImage
    results = subprocess.run("python detect.py --image {f}".format(f=folderPath[folderPath.rfind('/') + 1:] +
                                                                     "\\" + checkIfItsJpg(value)),
                             check=True, capture_output=True).stdout.decode("utf-8")
    resultLabel["text"] = results
    resizedImage = resizeImage(Image.open('results/' + value[: value.rfind('.') + 1] + "jpg"))
    rightPanelCanvas.create_image(0, 0, image=resizedImage, anchor=NW)
    rightPanelCanvas.image = resizedImage


def getDirectoryFileItems():
    global folderPath
    folderPath = filedialog.askdirectory()
    if folderPath != '':
        try:
            fileList = os.listdir(folderPath)
        except:
            fileList = []

        fileNames = [f for f in fileList if os.path.isfile(os.path.join(folderPath, f))
                     and f.lower().endswith((".png", ".jpg"))]

        leftPanelListBox.delete(0, END)
        for i in range(len(fileNames)):
            leftPanelListBox.insert(i, fileNames[i])


def resizeImage(originalImage):
    originalImageWidth = ImageTk.PhotoImage(originalImage).width()
    originalImageHeight = ImageTk.PhotoImage(originalImage).height()
    resizedImage = ImageTk.PhotoImage(
        originalImage.resize(
            (int(originalImageWidth / (originalImageHeight + originalImageWidth) * IMAGE_PANEL_WIDTH * SCALE_FACTOR),
             int(originalImageHeight / (originalImageHeight + originalImageWidth) * IMAGE_PANEL_HEIGHT * SCALE_FACTOR)),
            Image.ANTIALIAS))
    return resizedImage


def authors():
    authorsPopUp = Toplevel(root)
    authorsPopUp.geometry("150x70")
    authorsPopUp.resizable(0, 0)
    authorsPopUp.title("Authors")
    Label(authorsPopUp, text="Ayetijhya Desmukhya\nSujith Madesh\nJan Maliborski\nKuba Woch").pack()


# Root
root = Tk()
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.resizable(0, 0)
root.title("Face Recogniton Editor")
infoPhoto = PhotoImage(file='images/tmp/info.png')
root.iconphoto(False, infoPhoto)

# Main Panel
mainPanel = PanedWindow(bg=BACKGROUND_COLOR, borderwidth=1)
mainPanel.pack(fill=BOTH, expand=1)

# Left Panel
leftPanel = PanedWindow(mainPanel, orient=VERTICAL)
leftPanelFrame = Frame(leftPanel, bg=CONTRAST_COLOR)
leftPanel.add(leftPanelFrame)
Label(leftPanelFrame, text="Details", anchor=N, bg=CONTRAST_COLOR).pack()
leftPanelLabel1 = Label(leftPanelFrame, text="Image Files", anchor=N, bg=CONTRAST_COLOR)
leftPanelListBox = Listbox(leftPanelFrame, selectmode=SINGLE, width=30, height=15)
leftPanelListBox.bind('<<ListboxSelect>>', cursorSelect)
mainPanel.paneconfigure(leftPanel, width=LEFT_PANEL_WIDTH)
mainPanel.add(leftPanel)

# Middle Panel
middlePanel = PanedWindow(mainPanel, orient=VERTICAL)
middlePanelLabel = Label(middlePanel, text="Original Image", anchor=N, bg=BACKGROUND_COLOR, fg=FONT_COLOR)
middlePanel.add(middlePanelLabel)
middlePanelCanvas = Canvas(middlePanel, bd=3, relief=GROOVE)
middlePanel.add(middlePanelCanvas)
mainPanel.paneconfigure(middlePanel, width=IMAGE_PANEL_WIDTH)
mainPanel.add(middlePanel)

# Right Panel
rightPanel = PanedWindow(mainPanel, orient=VERTICAL)
rightPanelLabel = Label(rightPanel, text="Face(s) Detected", anchor=N, bg=BACKGROUND_COLOR, fg=FONT_COLOR)
rightPanel.add(rightPanelLabel)
rightPanelCanvas = Canvas(rightPanel, bd=3, relief=GROOVE)
rightPanel.add(rightPanelCanvas)
mainPanel.paneconfigure(rightPanel, width=IMAGE_PANEL_WIDTH)
mainPanel.add(rightPanel)

leftPanelButton = Button(leftPanelFrame, text='Browse', width=25, height=1, bg=BACKGROUND_COLOR,
                         command=lambda: getDirectoryFileItems(), fg=FONT_COLOR, borderwidth=0)
leftPanelButton.pack()
leftPanelLabel1.pack()
leftPanelListBox.pack()
Label(leftPanelFrame, text="Results", anchor=N, bg=CONTRAST_COLOR).pack()
resultLabel = Label(leftPanelFrame, text=results, anchor=N, width=25, height=15, bg="white", relief=SUNKEN, bd=1)
resultLabel.pack()
Label(leftPanelFrame, text="", anchor=N, bg=CONTRAST_COLOR).pack()
Button(leftPanelFrame, text="Authors", width=25, height=1, anchor=S, command=authors, bg=BACKGROUND_COLOR,
       fg=FONT_COLOR, borderwidth=0).pack()
root.mainloop()
