# Import the required libraries
from tkinter import *
from PIL import Image, ImageTk
from random import randint


# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
width = 400
height = 800
win.geometry(f"{width}x{height}")

#choice = input("Would you like map 1,2 or 3?: ")
choice = "1"

# Add Images to Canvas widget
if choice == "1":
   #image = ImageTk.PhotoImage(Image.open('BaseMap.png'))
   #image = ImageTk.PhotoImage(Image.open('Ground Floor edirts 1.png'))
   image = ImageTk.PhotoImage(Image.open('Map Navigation\HamptonMapMyVerChunksCorridorsWithPathSecond.png'))
   imagesizex = 7168
   imagesizey = 5195

elif choice == "2":
   image = ImageTk.PhotoImage(Image.open('Map Navigation\First Floor.PNG'))
   imagesizex = 1466
   imagesizey = 908

elif choice == "3":
   image = ImageTk.PhotoImage(Image.open('Second Floor.PNG'))
   imagesizex = 909
   imagesizey = 890


adjust_x = int(width)/2
adjust_y = int(height)/2

#(-2472,-936)

startcoordtempx = -2472-(width/2)
startcoordtempy = -936-(height/2)


start_proportion_x = startcoordtempx/imagesizex#8.2/17.3
start_proportion_y = startcoordtempy/imagesizey#6.6/10.3


translator_x = start_proportion_x*imagesizex
translator_y = start_proportion_y*imagesizey

x_coord = (translator_x)+int(width)/2
y_coord = (translator_y)+int(height)/2

def changetext():
   global label
   if label["text"] == "Test2":
      label.config(text="Yo")
   else:
      label.config(text="Test2")

# Define a Canvas widget
canvas = Canvas(win, width=4200, height=3138, bg="black")
canvas.place(x=x_coord,y=y_coord)

#image = ImageTk.PhotoImage(Image.open("C:\\Users\\nggro\\OneDrive - Hampton School\\Coding\\Playing around with image animation or movement in tkinter\\BaseMap.png"))
img = canvas.create_image(0,0,anchor=NW,image=image)
image_test = PhotoImage(width=1,height=1)

label = Label(win,text="Test2",width=57,height=5,bg="white",anchor="s",bd=2,relief="solid")
#label.place(anchor="sw",relx=0,rely=1)

button = Button(win,text="Test",width=3,height=2,bg="light blue",command=changetext)
#button.place(anchor="sw",relx=0,rely=1)
#button.pack(fill=X,pady=(757,0))
#button.grid(sticky="s",column=0,row=0)

center_box_size = 3
size = center_box_size + 4
ds = center_box_size + 4

def move(dx,dy):
    newx = canvas.winfo_x() + dx
    newy = canvas.winfo_y() + dy
    #print(f"old coord canvas: ({canvas.winfo_x()},{canvas.winfo_y()}) || new coord canvas: ({newx},{newy})")
    canvas.place(x=newx,y=newy)
    #num = randint(0,1000000)
    #colour = f"{hex(num)[2:]}"
    #if len(colour) < 7:
    #    colour += (7-len(((colour))))*"0"
    #canvas.create_rectangle((-newx+adjust_x),(-newy+adjust_y),(-newx+adjust_x)+size,(-newy+adjust_y)+size,fill="red",width=0)

def getcoords(e):
    print(f"coordinates: ({canvas.winfo_x()},{canvas.winfo_y()})")

image_test = PhotoImage(width=1,height=1)
testbtn1 = Label(win,image=image_test,width=center_box_size,height=center_box_size,bg="black")
testbtn1.place(x=(int(width)/2),y=(int(height)/2))

print(f"{x_coord-adjust_x},{y_coord-adjust_y}")

canvas.create_rectangle(0,10,10,0,fill="green")


# Bind the move function
win.bind("<Left>", lambda _: move(ds,0))
win.bind("<Right>", lambda _: move(-ds,0))
win.bind("<Up>", lambda _: move(0,ds))
win.bind("<Down>", lambda _: move(0,-ds))
win.bind("<Return>",getcoords)
win.bind("<space>",getcoords)

# win.bind("w", lambda _: move(0,ds))
# win.bind("s", lambda _: move(0,-ds))
# win.bind("a", lambda _: move(ds,0))
# win.bind("d", lambda _: move(-ds,0))

win.bind("w", lambda _: travelup())
win.bind("s", lambda _: traveldown())
win.bind("a", lambda _: travelleft())
win.bind("d", lambda _: travelright())

# if choice == "1":
#    NodeCoords = {
#     "Node 1":(-2068,-1426),
#     "Reception Stairs Ground":(-2068,-1510), 
#     "Node 1x":(-2068,-1608),
#     "Node 2a":(-2705,-1426),
#     "Node 2b":(-2845,-1426),
#     "Library Stairs Ground":(-2775,-1426),
#     "Node 2x":(-2705,-1629),
#     "Node 3a":(-2705,-950),
#     "Node 3b":(-2705,-901),
#     "Language Stairs Ground":(-2705,-862),
#     "Node 4":(-2845,-901),
#     "Node 4x":(-3034,-901),
#     "Node 5":(-2845,-789),
#     "History Stairs Ground":(-2845,-705),
#     "Node 5xa":(-3034,-705),
#     "Node 5xb":(-2908,-705),
#     "Node 6":(-2705,-789),
#     "Node 7":(-2509,-789),
#     "Node 8":(-2908,-579),
#     "Node 9":(-2705,-579),
#     "Node 10":(-2509,-579),
#     "Chemistry Stairs Ground":(-2579,-579),
#     "Node 10x":(-2509,-404),
#     "Node 11":(-2313,-579),
#     "Node 12":(-2068,-579),
#     "Node 13":(-1893,-579),
#     "Bioligy Stairs Ground":(-1956,-579),
#     "Node 13x":(-1893,-404),
#     "Node 14":(-1739,-579),
#     "Node 15":(-1382,-579),
#     "Art Stairs Ground":(-1522,-579),
#     "Node 16":(-2068,-789),
#     "Node 17":(-1739,-719),
#     "Node 18":(-2068,-950),
#     "Node 19":(-1739,-950),
#     "Latin Stairs Ground":(-1886,-950),
#     "Node 20":(-1382,-670),
#     "Node 20xa":(-1235,-719),
#     "Node 20xb":(-976,-670),
#     "Node 20x":(-1382,-719), 
#     "English Stairs Ground":(-927,-670),
#     "Node 21":(-1382,-950),
#     "Dance Studio Stairs Ground":(-906,-1244),
#     "Node 22":(-1382,-1181),
#     "Node 23":(-1739,-1181),
#     "Node 24":(-2068,-1181),
#     "Node 25":(-1382,-1426),
#     "Staff Dining Stairs Ground":(-1382,-1580),
#     "Node 25x":(-1382,-1503),
#     "Node 25xa":(-976,-1503),
#     "Node 25xb":(-1382,-1797),
#     "Node 26":(-1739,-1426),
#     "Node 26x":(-1739,-1580),
#     "Node 27":(-906,-1181),
#     "Node 27x":(-906,-1433),
#     "Node 28":(-1578,-2098),
#     "Node 28xb":(-878,-2098),
#     "Node 28xa":(-1578,-1930),
#     "Node 28xc":(-1578,-2308),
#     }
if choice == "1":
   NodeCoords = {    
    "Latin Stairs Second":(-1837,-936),
    "Node 37a":(-2117,-936),
    "Node 37b":(-2472,-936),
    "Node 37c":(-2677,-936),
    "Node 37d":(-2901,-936),
    "Node 37e":(-2472,-1230),
    "Node 37f":(-2677,-1195),
    "Language Stairs Second":(-2677,-838),
    "Atrium Stairs Second":(-2901,-1321),
    "Bioligy Stairs Second":(-1935,-481),
    "Node 38a":(-2116,-481),
    "Node 38b":(-2740,-481),
    "Chemistry Stairs Second":(-2509,-481),
    "RS Stairs Second":(-2068,-1328),
    "Node 39":(-2404,-1328),
    "Library Stairs Second":(-2740,-1468),
    "Node 40":(-2740,-1398),
    }
nodecoordmapper = {NodeCoords[node]:node for node in NodeCoords}

def adjustnodescoords(node):
    adjust = center_box_size-1
    #print(f"{adjust}")
    node[0],node[1] = node[0]+(adjust),node[1]+(adjust)
    return[node[0],node[1]]
#coords = list(map(adjustnodescoords,coords))

path = [] #to track the path and maybe go back thru steps
count = 0

#use classes

def travelup():
   global count
   x = canvas.winfo_x()
   y = canvas.winfo_y()
   if (x,y) not in nodecoordmapper:
      count = 1
      move(0,ds)
      win.after(1,travelup)
   elif (x,y) in nodecoordmapper and count == 0:
      count = 1
      move(0,ds)
      win.after(1,travelup)
   elif (x,y) in nodecoordmapper and count != 0:
      count = 0
      print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")

def travelright():
   global count
   x = canvas.winfo_x()
   y = canvas.winfo_y()
   if (x,y) not in nodecoordmapper:
      count = 1
      move(-ds,0)
      win.after(1,travelright)
   elif (x,y) in nodecoordmapper and count == 0:
      count = 1
      move(-ds,0)
      win.after(1,travelright)
   elif (x,y) in nodecoordmapper and count != 0:
      count = 0
      print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")
      
def travelleft():
   global count
   x = canvas.winfo_x()
   y = canvas.winfo_y()
   if (x,y) not in nodecoordmapper:
      count = 1
      move(ds,0)
      win.after(1,travelleft)
   elif (x,y) in nodecoordmapper and count == 0:
      count = 1
      move(ds,0)
      win.after(1,travelleft)
   elif (x,y) in nodecoordmapper and count != 0:
      count = 0
      print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")
 
def traveldown():
   global count
   x = canvas.winfo_x()
   y = canvas.winfo_y()
   if (x,y) not in nodecoordmapper:
      count = 1
      move(0,-ds)
      win.after(1,traveldown)
   elif (x,y) in nodecoordmapper and count == 0:
      count = 1
      move(0,-ds)
      win.after(1,traveldown)
   elif (x,y) in nodecoordmapper and count != 0:
      count = 0
      print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")
      
'''
win.bind("u",lambda _: zoomin())
#win.bind("",lambda _: zoomout()

def zoomin():
   global image
   canvas.delete("all")
   temp_image = Image.open('BaseMap.png')
   temp_image = temp_image.resize((int(temp_image.width*0.8),int(temp_image.height*0.8)),Image.LANCZOS)
   image = ImageTk.PhotoImage(temp_image)
   canvas.create_image(0,0,anchor=NW,image=image)
   
def zoomout():
   pass
'''

def navigate():
   pass


frame = Frame(win)
frame.grid(sticky="s",column=0,row=0)

buttonup = Button(frame,text="up",command = travelup)
buttonup.grid(row=0,column=1,sticky="nsew")
buttondown = Button(frame,text="down",command = traveldown)
buttondown.grid(row=0,column=2,sticky="nsew")
buttonleft = Button(frame,text="left",command = travelleft)
buttonleft.grid(row=0,column=3,sticky="nsew")
buttonright = Button(frame,text="right",command = travelright)
buttonright.grid(row=0,column=4,sticky="nsew")
   

win.mainloop()