from tkinter import *
import os
import ctypes
from PIL import Image
from PIL import ImageTk
from PIL import ImageOps
from PIL import ImageDraw
from tkinter import filedialog
from tkinter import messagebox
import imghdr
from collections import *

"""
CITATIONS
I found the command for changing the desktop background from this webpage:
http://stackoverflow.com/questions/14426475/change-wallpaper-in-python-for-user-while-being-system
"""


################ DRAW ################

def drawOnImage(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = True
    drawWindow = Toplevel(canvas.data.mainWindow)
    drawWindow.title = "Draw"
    drawFrame = Frame(drawWindow)
    redButton = Button(drawFrame, bg="red", width=2, \
                       command=lambda: colourChosen(drawWindow, canvas, "red"))
    redButton.grid(row=0, column=0)
    blueButton = Button(drawFrame, bg="blue", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "blue"))
    blueButton.grid(row=0, column=1)
    greenButton = Button(drawFrame, bg="green", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "green"))
    greenButton.grid(row=0, column=2)
    magentaButton = Button(drawFrame, bg="magenta", width=2, \
                           command=lambda: colourChosen(drawWindow, canvas, "magenta"))
    magentaButton.grid(row=1, column=0)
    cyanButton = Button(drawFrame, bg="cyan", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "cyan"))
    cyanButton.grid(row=1, column=1)
    yellowButton = Button(drawFrame, bg="yellow", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "yellow"))
    yellowButton.grid(row=1, column=2)
    orangeButton = Button(drawFrame, bg="orange", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "orange"))
    orangeButton.grid(row=2, column=0)
    purpleButton = Button(drawFrame, bg="purple", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "purple"))
    purpleButton.grid(row=2, column=1)
    brownButton = Button(drawFrame, bg="brown", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "brown"))
    brownButton.grid(row=2, column=2)
    blackButton = Button(drawFrame, bg="black", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "black"))
    blackButton.grid(row=3, column=0)
    whiteButton = Button(drawFrame, bg="white", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "white"))
    whiteButton.grid(row=3, column=1)
    grayButton = Button(drawFrame, bg="gray", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "gray"))
    grayButton.grid(row=3, column=2)
    drawFrame.pack(side=BOTTOM)


def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image != None:
        canvas.data.drawColour = colour
        canvas.data.mainWindow.bind("<B1-Motion>", \
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()
    clickedPositions.clear()

clickedPositions = list()

def drawDraw(event, canvas):
    if canvas.data.drawOn == True:
        #clickedPositions.append((event.x, event.y))

        x = int(round((event.x - canvas.data.imageTopX) * canvas.data.imageScale))
        y = int(round((event.y - canvas.data.imageTopY) * canvas.data.imageScale))
        clickedPositions.append((x, y))
        draw = ImageDraw.Draw(canvas.data.image)

        draw.line(clickedPositions, fill=(0, 0, 255), width=1)
        #draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=canvas.data.drawColour, \
        #             outline=None)

        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


######################## FEATURES ###########################
def reset(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    ### change back to original image
    if canvas.data.image != None:
        canvas.data.image = canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


################ EDIT MENU FUNCTIONS ############################

def keyPressed(canvas, event):
    if event.keysym == "z":
        undo(canvas)
    elif event.keysym == "y":
        redo(canvas)


# we use deques so as to make Undo and Redo more efficient and avoid
# memory space isuues
# after each change, we append the new version of the image to
# the Undo queue
def undo(canvas):
    if len(canvas.data.undoQueue) > 0:
        # the last element of the Undo Deque is the
        # current version of the image
        lastImage = canvas.data.undoQueue.pop()
        # we would want the current version if wehit redo after undo
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue) > 0:
        # the previous version of the image
        canvas.data.image = canvas.data.undoQueue[-1]
    save(canvas)
    canvas.data.imageForTk = makeImageForTk(canvas)
    drawImage(canvas)


def redo(canvas):
    if len(canvas.data.redoQueue) > 0:
        canvas.data.image = canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue) > 0:
        # we remove this version from the Redo Deque beacuase it
        # has become our current image
        lastImage = canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk = makeImageForTk(canvas)
    drawImage(canvas)


############# MENU COMMANDS ################

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image != None:
        filename = filedialog.asksaveasfilename(defaultextension=".jpg")
        im = canvas.data.image
        im.save(filename)


def save(canvas):
    if canvas.data.image != None:
        im = canvas.data.image
        im.save(canvas.data.imageLocation)


def newImage(canvas):
    imageName = filedialog.askopenfilename()
    filetype = ""
    # make sure it's an image file
    try:
        filetype = imghdr.what(imageName)
    except:
        messagebox.showinfo(title="Image File", \
                              message="Choose an Image File!", parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        canvas.data.imageLocation = imageName
        im = Image.open(imageName)
        canvas.data.image = im
        canvas.data.originalImage = im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize = im.size  # Original Image dimensions
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)
    else:
        messagebox.showinfo(title="Image File", \
                              message="Choose an Image File!", parent=canvas.data.mainWindow)


######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im = canvas.data.image
    if canvas.data.image != None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
        imageWidth = canvas.data.image.size[0]
        imageHeight = canvas.data.image.size[1]
        # To make biggest version of the image fit inside the canvas
        if imageWidth > imageHeight:
            resizedImage = im.resize((canvas.data.width, \
                                      int(round(float(imageHeight) * canvas.data.width / imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale = float(imageWidth) / canvas.data.width
        else:
            resizedImage = im.resize((int(round(float(imageWidth) * canvas.data.height / imageHeight)), \
                                      canvas.data.height))
            canvas.data.imageScale = float(imageHeight) / canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm = resizedImage
        return ImageTk.PhotoImage(resizedImage)


def drawImage(canvas):
    if canvas.data.image != None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0,
                            canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX = int(round(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0))
        canvas.data.imageTopY = int(round(canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0))


############ INITIALIZE ##############

def init(root, canvas):
    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image = None
    canvas.data.angleSelected = None
    canvas.data.rotateWindowClose = False
    canvas.data.brightnessWindowClose = False
    canvas.data.brightnessLevel = None
    canvas.data.histWindowClose = False
    canvas.data.solarizeWindowClose = False
    canvas.data.posterizeWindowClose = False
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.endCrop = False
    canvas.data.drawOn = True

    canvas.data.undoQueue = deque([], 10)
    canvas.data.redoQueue = deque([], 10)
    canvas.pack()


def buttonsInit(root, canvas):
    backgroundColour = "white"
    buttonWidth = 14
    buttonHeight = 2
    toolKitFrame = Frame(root)
    drawButton = Button(toolKitFrame, text="Draw", \
                        background=backgroundColour, width=buttonWidth, \
                        height=buttonHeight, command=lambda: drawOnImage(canvas))
    drawButton.grid(row=8, column=0)
    resetButton = Button(toolKitFrame, text="Reset", \
                         background=backgroundColour, width=buttonWidth, \
                         height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=9, column=0)
    toolKitFrame.pack(side=LEFT)


def menuInit(root, canvas):
    menubar = Menu(root)
    menubar.add_command(label="New", command=lambda: newImage(canvas))
    menubar.add_command(label="Save", command=lambda: save(canvas))
    menubar.add_command(label="Save As", command=lambda: saveAs(canvas))
    ## Edit pull-down Menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo   Z", command=lambda: undo(canvas))
    editmenu.add_command(label="Redo   Y", command=lambda: redo(canvas))
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)

def run():
    # create the root and the canvas
    root = Tk()
    root.title("Image Editor")
    canvasWidth = 500
    canvasHeight = 500
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="gray")

    # Set up canvas data and call init
    class Struct: pass

    canvas.data = Struct()
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.mainWindow = root
    init(root, canvas)
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits)


run()