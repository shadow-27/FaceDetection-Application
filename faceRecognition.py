import os
import subprocess
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
LEFT_PANEL_WIDTH = 200
IMAGE_PANEL_WIDTH = 500
IMAGE_PANEL_HEIGHT = 600
SCALE_FACTOR = 1.5

folderPath = ''


def cursorSelect(evt):
    value = leftPanelListBox.get(leftPanelListBox.curselection())
    resizedImage = resizeImage(Image.open(folderPath + '/' + value))
    middlePanelCanvas.create_image(0, 0, image=resizedImage, anchor=NW)
    middlePanelCanvas.image = resizedImage
    subprocess.run("python detect.py --image {f}".format(f=value), shell=True)
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
                     and f.lower().endswith((".png", ".gif", ".jpg",".jfif"))]

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


# Root
root = Tk()
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.resizable(0, 0)
root.title("Face Recogniton Editor")

# Main Panel
mainPanel = PanedWindow(bg='gray', borderwidth=1)
mainPanel.pack(fill=BOTH, expand=1)

# Left Panel
leftPanel = PanedWindow(mainPanel, orient=VERTICAL)
leftPanelFrame = Frame(leftPanel)
leftPanel.add(leftPanelFrame)
leftPanelLabel1 = Label(leftPanelFrame, text="Details", anchor=N)
leftPanelLabel1.pack()
leftPanelLabel2 = Label(leftPanelFrame, text="Image Files", anchor=N)
leftPanelListBox = Listbox(leftPanelFrame, selectmode=SINGLE, width=30, height=20)
leftPanelListBox.bind('<<ListboxSelect>>', cursorSelect)
mainPanel.paneconfigure(leftPanel, width=LEFT_PANEL_WIDTH)
mainPanel.add(leftPanel)

# Middle Panel
middlePanel = PanedWindow(mainPanel, orient=VERTICAL)
middlePanelLabel = Label(middlePanel, text="Original Image", anchor=N)
middlePanel.add(middlePanelLabel)
middlePanelCanvas = Canvas(middlePanel, bd=3, relief=GROOVE)
middlePanel.add(middlePanelCanvas)
mainPanel.paneconfigure(middlePanel, width=IMAGE_PANEL_WIDTH)
mainPanel.add(middlePanel)

# Right Panel
rightPanel = PanedWindow(mainPanel, orient=VERTICAL)
rightPanelLabel = Label(rightPanel, text="Face(s) Detected", anchor=N)
rightPanel.add(rightPanelLabel)
rightPanelCanvas = Canvas(rightPanel, bd=3, relief=GROOVE)
rightPanel.add(rightPanelCanvas)
mainPanel.paneconfigure(rightPanel, width=IMAGE_PANEL_WIDTH)
mainPanel.add(rightPanel)

leftPanelButton = Button(leftPanelFrame, text='Browse', width=25, height=1,
                         command=lambda: getDirectoryFileItems())
leftPanelButton.pack()
leftPanelLabel2.pack()
leftPanelListBox.pack()

root.mainloop()
