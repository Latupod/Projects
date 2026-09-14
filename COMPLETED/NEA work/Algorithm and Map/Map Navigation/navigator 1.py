# Import the required libraries
from tkinter import *
from PIL import Image, ImageTk
import MainProgram

CorridorFloorMapper = MainProgram.CorridorFloorMapper
NodeCoords = MainProgram.NodeCoords
Nodes,Corridors,startnodepair,endnodepair,startroomplace,endroomplace,floors = MainProgram.maincode()
if len(list(set(floors))) == 1:
   floor = floors[0]
else:
   floor = None


nodecoordmapper = {NodeCoords[floor][node]:node for node in NodeCoords[floor]} #improt nodecorrds from data
nodecoordmapperground = {NodeCoords[floor][node]:node for node in NodeCoords["Ground Floor"]} 
nodecoordmapperfirst = {NodeCoords[floor][node]:node for node in NodeCoords["First Floor"]}

linkcorridor = []
for corridor in Corridors:
   if corridor in CorridorFloorMapper["Ground-First Floor"]: #means a change in floor has occurred
      linkcorridor.append([corridor,"Ground-First"])
   elif corridor in CorridorFloorMapper["First-Second Floor"]:
      linkcorridor.append([corridor,"First-Second"])

#movement spacing is 7
#find a corridor and take its two nodes
#Convert nodes to coordinates
print(f"start:{startnodepair} end:{endnodepair}")
startnodepair = (NodeCoords[floor][startnodepair[0]],NodeCoords[floors[0]][startnodepair[1]])
endnodepair = (NodeCoords[floor][endnodepair[0]],NodeCoords[floors[1]][endnodepair[1]])
print(f"start:{startnodepair} end:{endnodepair}")

startnodediff = (abs(startnodepair[1][0] - startnodepair[0][0]),abs(startnodepair[1][1] - startnodepair[0][1]))
endnodediff = (abs(endnodepair[1][0] - endnodepair[0][0]),abs(endnodepair[1][1] - endnodepair[0][1]))
print(f"startdiff:{startnodediff} enddiff:{endnodediff}")

startnodesections = int(startnodediff[1]/7) if startnodediff[0] == 0 else int(startnodediff[0]/7)
endnodesections = int(endnodediff[1]/7) if endnodediff[0] == 0 else int(endnodediff[0]/7)

startnoderem = startnodesections % 10
endnoderem = endnodesections % 10

def findroomcoord(nodediff,nodepair,remainder,changescale,sections,displacement = 0):
   try:
      addcoord = 10 // remainder
   except ZeroDivisionError:
      addcoord = 0
   jump = sections // 10
   scalefactors = []
   for pos in range(1,11):
      if (pos % addcoord) == 0:
         if displacement < remainder:
            displacement += 1
      scalefactors.append(jump*pos + displacement)
   print(scalefactors)
   if nodediff[0] == 0: #if no change in x
      return (nodepair[0][0] , min(nodepair[0][1],nodepair[1][1]) + (scalefactors[int(changescale)])*7 ) #then change y
   elif nodediff[1] == 0: #if no change in y
      return (max(nodepair[0][0],nodepair[1][0]) - (scalefactors[int(changescale)])*7 , nodepair[0][1] ) #then change x

startroomplace = findroomcoord(startnodediff,startnodepair,startnoderem,startroomplace[0],startnodesections)
endroomplace = findroomcoord(endnodediff,endnodepair,endnoderem,endroomplace[0],endnodesections)
print(f"startroom:{startroomplace} endroom:{endroomplace}")

# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
width = 400
height = 800
win.geometry(f"{width}x{height}")


# Add Images to Canvas widget
#image = ImageTk.PhotoImage(Image.open('Map Navigation\HamptonMapMyVerChunksCorridorsWithPath.png'))
if floor == "Ground Floor":
   image = ImageTk.PhotoImage(Image.open('Map Navigation\HamptonMapMyVerChunks.png'))
if floor == "First Floor":
   image = ImageTk.PhotoImage(Image.open('Map Navigation\HamptonMapMyVerChunksCorridorsWithPathFirst.png'))
imagesizex = 4200
imagesizey = 3138

adjust_x = int(width)/2
adjust_y = int(height)/2

startcoordtempx = -2068-(width/2)
startcoordtempy = -1608-(height/2)


start_proportion_x = startcoordtempx/imagesizex
start_proportion_y = startcoordtempy/imagesizey


translator_x = start_proportion_x*imagesizex
translator_y = start_proportion_y*imagesizey

x_coord = (translator_x)+int(width)/2
y_coord = (translator_y)+int(height)/2


# Define a Canvas widget
canvas = Canvas(win, width=4200, height=3138, bg="black")
canvas.place(x=x_coord,y=y_coord)

img = canvas.create_image(0,0,anchor=NW,image=image)

center_box_size = 3
size = center_box_size + 4
ds = center_box_size + 4

def move(dx,dy):
    newx = canvas.winfo_x() + dx
    newy = canvas.winfo_y() + dy
    canvas.place(x=newx,y=newy)
    #canvas.create_rectangle((-newx+adjust_x),(-newy+adjust_y),(-newx+adjust_x)+size,(-newy+adjust_y)+size,fill="red",width=0) #TRAIL

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
 
#write a function that when given a corridor it can find the pair nodes connecting
#so i can get the two nodes connecting floors on stairs

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

nodecoordmapper[startroomplace] = "StartTempNode"
nodecoordmapper[endroomplace] = "EndTempNode"

def navigate(Nodes):
   if len(floors) == 1 :
      CoordPath = [NodeCoords[floor][node]for node in Nodes]
      CoordPath.insert(0,startroomplace)
      CoordPath.append(endroomplace)
            #print(CoordPath)
   #  for x in nodecoordmapper:
   #     print(f"{x}:{nodecoordmapper[x]}")
      canvas.place(x=CoordPath[0][0],y=CoordPath[0][1])
      win.update()
      win.after(500)
      for coord in range(len(CoordPath)-1):
         print(coord)
         current_x = CoordPath[coord][0]
         current_y = CoordPath[coord][1]
         next_x = CoordPath[coord+1][0]
         next_y = CoordPath[coord+1][1]
         if (canvas.winfo_x,canvas.winfo_y) != (CoordPath[-1]):
            if next_y > current_y:
                  travelup()
                  win.update()
            if next_y < current_y:
                  traveldown()
                  win.update()
            if next_x > current_x:
                  travelleft()
                  win.update()
            if next_x < current_x:
                  travelright()
                  win.update()
   if len(floors) != 1:
      CoordPath = []
      for floor in floors:
         toadd = []
         for corridor in Corridors:
            if corridor in CorridorFloorMapper:
               break 
         CoordPath.append(toadd)

                

def getcoords(e):
    print(f"coordinates: ({canvas.winfo_x()},{canvas.winfo_y()})")

image_test = PhotoImage(width=1,height=1)
testbtn1 = Label(win,image=image_test,width=center_box_size,height=center_box_size,bg="black")
testbtn1.place(x=(int(width)/2),y=(int(height)/2))

print(f"{x_coord},{y_coord}")

canvas.create_rectangle(0,10,10,0,fill="green")

# Bind the move function
win.bind("<Left>", lambda _: move(ds,0))
win.bind("<Right>", lambda _: move(-ds,0))
win.bind("<Up>", lambda _: move(0,ds))
win.bind("<Down>", lambda _: move(0,-ds))
win.bind("<space>",getcoords)

win.bind("w", lambda _: travelup())
win.bind("s", lambda _: traveldown())
win.bind("a", lambda _: travelleft())
win.bind("d", lambda _: travelright())
win.bind("b", lambda _: navigate(Nodes))

win.mainloop()
