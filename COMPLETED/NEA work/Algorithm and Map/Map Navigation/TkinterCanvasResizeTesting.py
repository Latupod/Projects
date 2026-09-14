from tkinter import *
from PIL import Image,ImageTk


#win = Tk()
# width = 1200
# height = 1200
# win.geometry(f"{width}x{height}")

# image = ImageTk.PhotoImage(Image.open('Map Navigation\HamptonMapMyVerChunks.png'))
# imagesizex = 7168
# imagesizey = 5195

# adjust_x = int(width)/2
# adjust_y = int(height)/2

# startcoordtempx = -2068-(width/2)
# startcoordtempy = -1545-(height/2)


# start_proportion_x = startcoordtempx/imagesizex
# start_proportion_y = startcoordtempy/imagesizey

# translator_x = start_proportion_x*imagesizex
# translator_y = start_proportion_y*imagesizey

# x_coord = (translator_x)+int(width)/2
# y_coord = (translator_y)+int(height)/2

# canvas = Canvas(win, width=4200, height=3138, bg="black")
# canvas.place(x=x_coord,y=y_coord)

# img = canvas.create_image(0,0,anchor=NW,image=image)

# def zoomin():
#    print("zoom in")
#    canvas.delete("all")
#    temp_image = Image.open('Map Navigation\HamptonMapMyVerChunks.png')
#    temp_image = temp_image.resize((int(temp_image.width*1.1),int(temp_image.height*1.1)),Image.LANCZOS)
#    image = ImageTk.PhotoImage(temp_image)
#    canvas.create_image(0,0,anchor=NW,image=image)
#    win.update()
   
# def zoomout():
#    print("zoom out")
#    canvas.delete("all")
#    temp_image = Image.open('Map Navigation\HamptonMapMyVerChunks.png')
#    temp_image = temp_image.resize((int(temp_image.width*0.9),int(temp_image.height*0.9)),Image.LANCZOS)
#    image = ImageTk.PhotoImage(temp_image)
#    canvas.create_image(0,0,anchor=NW,image=image)
#    win.update()
   
# def zoomin(event):
#    print("zoom in")
#    canvas.delete("all")
#    x,y = event.x , event.y
#    width = canvas.winfo_width()
#    height = canvas.winfo_height()
#    n_width = width + 1
#    n_height = height + 1
#    print(width,height)
#    print(n_width,n_height)
#    img_og = Image.open('Map Navigation\HamptonMapMyVerChunks.png')
#    #img_new = img_og.resize((n_width,n_height))
#    img_new = img_og.crop((x-45,y-30,x+45,y+30))
#    img_new = ImageTk.PhotoImage(img_new)
#    canvas.create_image(0,0,image=img_new)

# def zoomout():
#    print("zoom out")
#    image = Image.open('Map Navigation\HamptonMapMyVerChunks.png')
#    # Decrease the image size by a factor (e.g., 0.8)
#    image = image.resize((int(image.width * 0.8), int(image.height * 0.8)))
#    tk_image = ImageTk.PhotoImage(image)
#    canvas.delete("all")
#    canvas.create_image(0, 0, anchor=NW, image=tk_image)

# def scroll_start(event):
#    canvas.scan_mark(event.x, event.y)

# def scroll_move(event):
#    canvas.scan_dragto(event.x, event.y, gain=1)

# def getcoord():
#    img = canvas.create_image(0,0,anchor=NW,image=image)
#    print(f"coordinates: ({canvas.winfo_x()},{canvas.winfo_y()})")

# canvas.bind("<ButtonPress-1>", scroll_start)
# canvas.bind("<B1-Motion>", scroll_move)
# win.bind("<space>",lambda _: getcoord())


# win.bind("q",lambda _: zoomin())
# win.bind("e",lambda _: zoomout())

# win.mainloop()

class ImageZoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Zoom")

        # Create a Canvas widget
        self.canvas = Canvas(self.root, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

        # Initialize image and image reference
        self.image = None
        self.tk_image = None

        # Load an initial image (you can use your own image file)
        self.load_image('Map Navigation\HamptonMapMyVerChunks.png')

        # Create Zoom In and Zoom Out buttons
        zoom_in_button = Button(self.root, text="Zoom In", command=self.zoom_in)
        zoom_out_button = Button(self.root, text="Zoom Out", command=self.zoom_out)
        zoom_in_button.pack(side=LEFT)
        zoom_out_button.pack(side=LEFT)

        # Bind mouse wheel events for zooming
        self.canvas.bind("<Button-4>", self.zoom_in)
        self.canvas.bind("<Button-5>", self.zoom_out)

    def load_image(self, filename):
        # Load the image using PIL (Python Imaging Library)
        self.image = Image.open(filename)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Display the image on the Canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

    def zoom_in(self, event=None):
        # Increase the image size by a factor (e.g., 1.2)
        self.image = self.image.resize((int(self.image.width * 1.2), int(self.image.height * 1.2)))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

    def zoom_out(self, event=None):
        # Decrease the image size by a factor (e.g., 0.8)
        self.image = self.image.resize((int(self.image.width * 0.8), int(self.image.height * 0.8)))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

if __name__ == "__main__":
    root = Tk()
    app = ImageZoomApp(root)
    root.mainloop()