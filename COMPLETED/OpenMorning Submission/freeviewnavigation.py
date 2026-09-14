# Import the required libraries
from tkinter import * #Used to run GUI
from PIL import Image, ImageTk #Used to load Images 

class window(): #Class to run all code
    def __init__(self,win,file):
        self.file = file #the desired to be floor 
        self.win = win #the window the map will appear on
        self.winwidth = 400 #initialising the window width
        self.winheight = 800 #initialising the window height
        self.win.geometry(f"{self.winwidth}x{self.winheight}") #initialising the window size

        self.imagesizex = 4200 #initialising the image size
        self.imagesizey = 3138
        self.adjust_x = (self.winwidth)/2 #the adjustment to place the user in the centre of the screen
        self.adjust_y = (self.winheight)/2

        self.makecanvas()

    def makecanvas(self):
        startcoordtempx = -2068-self.adjust_x # the values 2068 and 1608 just depict the chosen start coordinates
        startcoordtempy = -1608-self.adjust_y
        x_coord = (startcoordtempx)+int(self.winwidth)/2 #the coordinates that the canvas and so image will be placed
        y_coord = (startcoordtempy)+int(self.winheight)/2
        self.canvas = Canvas(self.win, width=self.imagesizex, height=self.imagesizey, bg="black") #setting up the canvas
        self.canvas.place(x=x_coord,y=y_coord) #placing the canvas
        self.canvas.bind("<ButtonPress-1>", self.scroll_start) #setting up the freeview scrolling option to the mouse 
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.drawcanvas(self.file)
    
    def drawcanvas(self,file): #pass image as the file name
        self.canvas.delete("all") #clear the canvas
        #selecting the corresponding file image
        if file == "Ground Floor":
            file = ('HamptonMapMyVerGroundFloor.drawio.png')
        elif file == "First Floor":
            file = ('HamptonMapMyVerFirstFloor.drawio.png')
        elif file == "Second Floor":
            file = ('HamptonMapMyVerSecondFloor.drawio.png')

        self.image = ImageTk.PhotoImage(Image.open(file)) #load the image
        self.canvas.create_image(0,0,anchor=NW,image=self.image) #create the image onto the canvas
        self.win.update() #update the screen

    '''Following two functions are used to move the canvas freely using the mouse'''
    def scroll_start(self,event): 
        self.canvas.scan_mark(event.x, event.y)
    def scroll_move(self,event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def start(self): #start the window
        self.win.mainloop()    

def startground():
    win = Toplevel() #setup the window
    travel_interface = window(win,"Ground Floor") #initialise the interface
    travel_interface.start() #start the program

def startfirst():
    win = Toplevel() #setup the window
    travel_interface = window(win,"First Floor") #initialise the interface
    travel_interface.start() #start the program

def startsecond():
    win = Toplevel() #setup the window
    travel_interface = window(win,"Second Floor") #initialise the interface
    travel_interface.start() #start the program


