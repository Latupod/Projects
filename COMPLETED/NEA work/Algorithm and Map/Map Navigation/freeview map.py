from tkinter import *
from PIL import Image,ImageTk


win = Tk()
width = 1200
height = 1200
win.geometry(f"{width}x{height}")

image = ImageTk.PhotoImage(Image.open('Map Navigation\HamptonMapMyVerChunks.png'))
imagesizex = 7168
imagesizey = 5195

adjust_x = int(width)/2
adjust_y = int(height)/2

startcoordtempx = -2068-(width/2)
startcoordtempy = -1545-(height/2)


start_proportion_x = startcoordtempx/imagesizex
start_proportion_y = startcoordtempy/imagesizey

translator_x = start_proportion_x*imagesizex
translator_y = start_proportion_y*imagesizey

x_coord = (translator_x)+int(width)/2
y_coord = (translator_y)+int(height)/2

canvas = Canvas(win, width=4200, height=3138, bg="black")
canvas.place(x=x_coord,y=y_coord)

img = canvas.create_image(0,0,anchor=NW,image=image)

def scroll_start(event):
   canvas.scan_mark(event.x, event.y)

def scroll_move(event):
   canvas.scan_dragto(event.x, event.y, gain=1)

def getcoord():
   img = canvas.create_image(0,0,anchor=NW,image=image)
   print(f"coordinates: ({canvas.winfo_x()},{canvas.winfo_y()})")

canvas.bind("<ButtonPress-1>", scroll_start)
canvas.bind("<B1-Motion>", scroll_move)
win.bind("<space>",lambda _: getcoord())


win.mainloop()
