import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from future.moves import tkinter
import sys
import datetime

def evalRational(x,y, l):
    z = x + y * 1j
    p = 4 * z ** 2 * (2 * z + l)
    q = (2 * l + 3) * z * 2 - (l + 2)
    return 0.5 * p / q

def evalExample(x, y):
    z = x + y * 1j
    c = - ( z ** 2 + 2 * z) / (2 * z + 3)
    p = c ** 2 * (c + z)
    q = (2 * z + 3) * c - z - 2
    #p = - z ** 3 * (z + 2)
    #q = (2 * z + 3) ** 3
    return 0.5 * p / q

# Create the main window
mainWindow = tkinter.Tk()
mainWindow.resizable(False, False)
dpi = mainWindow.winfo_fpixels('1i')
print(dpi)

# Parameters
minX, maxX = -20, 20
minY, maxY = -20, 20
deltaX, deltaY = maxX - minX, maxY - minY
CanvasHeight = 554
CanvasWidth = 744

# Load the region for the parameter alpha
fig2, ax2 = plt.subplots()
width = CanvasWidth / dpi
height = CanvasHeight / dpi

fig2.set_size_inches(width + 2, height + 1.55)
delta = 0.05
u = np.arange(minX, maxX, delta)
v = np.arange(minY, maxY, delta)
X, Y = np.meshgrid(u, v)
A = evalExample(X, Y)
Z = abs(A)

ax2.contour(X, Y, Z, [1])
#plt.savefig("Region2.png", bbox_inches = "tight", dpi = dpi)
ax2.axis("off")
plt.savefig("Region.png", dpi=dpi, bbox_inches="tight")
region_picture = tkinter.PhotoImage(file="Region.png")

# draw the picture containing the lemniscate
fig, ax = plt.subplots()
fig.set_size_inches(width, height)

plt.savefig("Lemniscate.png", dpi=dpi)
lemniscate_picture = tkinter.PhotoImage(file="Lemniscate.png")

lemniscate_picture_canvas =  tkinter.Canvas(master=mainWindow, width=CanvasWidth, height=CanvasHeight)
lemniscate_picture_canvas.grid(row=0, column=0, padx = 10, pady = 10)

image_lemniscate = lemniscate_picture_canvas.create_image(0, 0, anchor='nw', image=lemniscate_picture)

# Draw the region for parameter alpha
canvas = tkinter.Canvas(master=mainWindow, width=CanvasWidth, height=CanvasHeight)
canvas.grid(row=0, column=1, padx=10, pady=10)

# Parameter CAnvas
canvas.create_image(0,0, anchor='nw', image=region_picture)
yCoordOfZero = int(CanvasHeight * (minY / deltaY + 1)) + 2
canvas.create_line(0, yCoordOfZero, CanvasWidth, yCoordOfZero)
xCoordOfZero = int(-minX * CanvasWidth / deltaX) + 2
canvas.create_line(xCoordOfZero, 0, xCoordOfZero, CanvasHeight)

ball = canvas.create_oval(241, 278, 245, 282, fill="red")
ball_coords = canvas.coords(ball)

x = (deltaX / CanvasWidth) * ball_coords[0] + minX
y = (deltaY / CanvasHeight) * (CanvasHeight - ball_coords[1]) + minY
a = x + y * 1j

# Create the left bottom pane for options
left_options_frame = tkinter.Frame(master=mainWindow)
left_options_frame.grid(row=1, column=0, padx=10, pady=10)

scale_label = tkinter.Label(master=left_options_frame, text="Window Size: ")
scale_label.grid(row=0, column=0, padx = 5, pady = 5, sticky="W")

scale_entry = tkinter.Entry(master=left_options_frame)
scale_entry.insert(0, "3")
scale_entry.grid(row=0,column=1, padx=5, pady=5, sticky="W")

open_button = tkinter.Button(master=left_options_frame, text="Open Image")
open_button.grid(row=1,column=0,columnspan=1)

def showPlot(e):
    plt.show()
open_button.bind("<Button-1>", showPlot)

extractInfo_button = tkinter.Button(master=left_options_frame, text="Extract")
extractInfo_button.grid(row=1, column=1, columnspan=1)

def writeComplexNumber(z):
    result = "{:.4f}".format(z.real)
    if z.imag < 0:
        result += " - "
    else:
        result += " + "
    result += "{:.4f}".format(abs(z.imag)) + "i"
    return result

def extractInfo(e):
    global a
    # Draw Roots
    # Create object for capturing the current time
    current_time = datetime.datetime.now()
    root = -a / 2
    stringA = writeComplexNumber(a)
    toWriteInFile = "-------------------------------\n"
    toWriteInFile += str(current_time.year) + "/" + str(current_time.month) + "/" + str(current_time.day) + "  " + str(current_time.time()) + "\n"
    toWriteInFile += "Rational Function:\n"
    toWriteInFile += "( 4 * z^2 * (2 * z  + (" + stringA + " ) ) ) / (2 * ( " + stringA + " ) + 3) * z * 2 - ( " + stringA + " 2 ) )" + "\n"
    toWriteInFile += "Roots:\n"
    toWriteInFile += "   1) z_1 = 0 (ordre 2).\n"
    toWriteInFile += "   2) z_2 = "
    toWriteInFile += writeComplexNumber(a) + " (ordre 1).\n\n"

    # Draw poles
    pole = (a + 2) / (4 * a + 6.0)
    toWriteInFile += "Poles:\n"
    toWriteInFile += "   1) p_1 = infinity (ordre 2).\n"
    toWriteInFile += "   2) p_2 = " + writeComplexNumber(pole) + " (ordre 1).\n\n"

    # Draw Critical Numbers
    critNumber = - 0.5 * (a ** 2 + 2 * a) / (2 * a + 3)
    toWriteInFile += "Critical Numbers:\n"
    toWriteInFile += "   1) c_1 = 0 (ordre 1).\n"
    toWriteInFile += "   2) c_2 = 0.5 (ordre 1).\n"
    toWriteInFile += "   3) c_3 = " + writeComplexNumber(critNumber) + " (ordre 1).\n"
    toWriteInFile += "   4) c_4 = infinity (ordre 1).\n"

    toWriteInFile += "-------------------------------\n"
    print(toWriteInFile)

extractInfo_button.bind("<Button-1>", extractInfo)

# Create the right bottom pane for coordinates of alpha
right_coord_frame = tkinter.Frame(master=mainWindow)
right_coord_frame.grid(row=1, column=1, padx = 10, pady = 10)

paramCoord_label = tkinter.Label(master=right_coord_frame, text="Coord: ")
paramCoord_label.grid(row=0, column = 0, padx = 5, pady = 5)

paramCoord_entry = tkinter.Label(master=right_coord_frame, text="0.5 + 0i")
paramCoord_entry.config(text = "{:.4f}".format(a.real) + "+ " + "{:.4f}".format(a.imag) + "i")
paramCoord_entry.grid(row=0, column=1, padx = 5, pady = 5)

# Movement of the ball
ball_clicked = False
prev_x, prev_y = 0, 0
def start_move(event):
    global ball_clicked, prev_x, prev_y
    ball_clicked = True
    prev_x, prev_y = event.x, event.y
def move_ball(event):
    global ball_clicked, prev_x, prev_y
    if ball_clicked:
        x, y = event.x, event.y
        if x >= 0 and x <= CanvasWidth and y <= CanvasHeight and y >= 0:
            dx, dy = x - prev_x, y - prev_y
            prev_x, prev_y = x, y
            canvas.move(ball, dx, dy)

def stop_move(event):
    global ball_clicked
    global window, lemniscate_picture_canvas, lemniscate_picture
    global fig, ax
    global a, minX, maxX, minY, maxY, deltaX, deltaY, width, height

    ball_clicked = False

    #plt.cla()
    ball_coords = canvas.coords(ball)

    x = (deltaX / CanvasWidth) * ball_coords[0] + minX
    y = (deltaY / CanvasHeight) * (CanvasHeight - ball_coords[1]) + minY
    paramCoord_entry.config(text = "{:.4f}".format(x) + "+ " + "{:.4f}".format(y) + "i")

    a = x + y * 1j
    window = float(scale_entry.get())
    delta = 0.01  # side of the meshgrid
    u = np.arange(-window, window, delta)
    v = np.arange(-window, window, delta)
    X, Y = np.meshgrid(u, v)

    A = evalRational(X, Y, a)
    Z = abs(A)

    plt.close()
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)

    ax.contour(X, Y, Z, [1.0])

    # Draw Roots
    root = -a / 2
    ax.plot([root.real], [root.imag], marker='o', markersize='2', color='g')
    #ax.plot([0],[0], marker='o', markersize='2', color='g')

    # Draw poles
    pole = (a + 2) / (4 * a + 6.0)
    ax.plot([pole.real], [pole.imag], marker='o', markersize='2', color='b')

    # Draw Critical Numbers
    critNumber = - 0.5 * (a ** 2 + 2 * a) / (2 * a + 3)
    ax.plot([critNumber.real], [critNumber.imag], marker='o', markersize='2', color='r')
    ax.plot([0], [0], marker='o', markersize='2', color='k')
    ax.plot([0.5], [0], marker='o', markersize='2', color='r')

    plt.savefig("Lemniscate.png", dpi=dpi)
    lemniscate_picture = tkinter.PhotoImage(file="Lemniscate.png")
    lemniscate_picture_canvas.create_image(0, 0, anchor='nw', image=lemniscate_picture)

canvas.bind("<Button-1>", start_move)
canvas.bind("<B1-Motion>", move_ball)
canvas.bind("<ButtonRelease>", stop_move)

mainWindow.mainloop()
