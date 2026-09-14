# Import the required libraries
from tkinter import *
from PIL import Image, ImageTk
import MainProgram


class navUI():
    def __init__(self,room1,room2):
        self.NodeConnections = MainProgram.NodeConnections
        self.CorridorFloorMapper = MainProgram.CorridorFloorMapper #maps the stair connection corridors so they can be recpgnised if a change in floor is occuring
        self.NodeCoords = MainProgram.NodeCoords #contains coordinates of every node for every floor
        self.Nodes,self.Corridors,startnodepair,endnodepair,startroomplace,endroomplace,self.floors = MainProgram.maincode(room1,room2)
        self.nodecoordmapperground = {self.NodeCoords["Ground Floor"][node]:node for node in self.NodeCoords["Ground Floor"]} 
        self.nodecoordmapperfirst = {self.NodeCoords["First Floor"][node]:node for node in self.NodeCoords["First Floor"]}
        self.nodecoordmappersecond = {self.NodeCoords["Second Floor"][node]:node for node in self.NodeCoords["Second Floor"]}
        self.startroomplace = self.getnodepos(self.floors[0],startroomplace,startnodepair)
        self.endroomplace = self.getnodepos(self.floors[-1],endroomplace,endnodepair)
        self.linkfloors = self.checkfloors()
    
    def checkfloors(self,linkfloors = []): #checks what floors are involved in the navigation e.g. ground to first or first to second or both (so ground to second)
        for corridor in self.Corridors: #for each corridor in the corridors involved in the path 
            if corridor in self.CorridorFloorMapper["Ground-First Floor"]: #if the corridor is in the ground-first floor section, 
                linkfloors.append([corridor,"Ground-First"]) #recongise that ground and first floors are involved, and note which corridor is causing this
            elif corridor in self.CorridorFloorMapper["First-Second Floor"]: #if the corridor is in the first-second floor section, 
                linkfloors.append([corridor,"First-Second"]) #recongise that first and second floors are involved, and note which corridor is causing this
        if len(linkfloors) == 2:
            self.floors = ["Ground Floor","First Floor","Second Floor"]
        return linkfloors #return the linkfloors list, if empty then all navigation occurs on one floor

    def getnodepos(self,floor,roomplace,nodepair):
        nodepair = (self.NodeCoords[floor][nodepair[0]],self.NodeCoords[floor][nodepair[1]])
        nodediff = (abs(nodepair[1][0] - nodepair[0][0]),abs(nodepair[1][1] - nodepair[0][1]))
        nodesections = int(nodediff[1]/7) if nodediff[0] == 0 else int(nodediff[0]/7)
        #print(f"nodepair: {nodepair} nodediff: {nodediff} nodesections: {nodesections}")
        
        return self.findroomcoord(nodediff,nodepair,roomplace[0],nodesections)

    def findroomcoord(self,nodediff,nodepair,changescale,sections,displacement = 0): #using maths to work out the position of a room in a corridor
        sections = int(sections)
        remainder = sections % 10
        #print(f"remainder: {remainder}")
        try:
            addcoord = 10 // remainder
        except ZeroDivisionError: #if remainder is zero, then except a zero division error and just consider addcord as 0
            addcoord = 0
        jump = sections // 10
        #print(f"sections: {sections}")
        #print(f"jumps: {jump}")
        scalefactors = []
        for pos in range(1,11):
            try:
                if (pos % addcoord) == 0:
                    if displacement < remainder:
                        displacement += 1
            except ZeroDivisionError:
                pass
            scalefactors.append(jump*pos + displacement)
        #print(f"Scalefactors: {scalefactors}")
        #print(f"nodediff: {nodediff}")
        if nodediff[0] == 0: #if no change in x
            return (nodepair[0][0] , min(nodepair[0][1],nodepair[1][1]) + (scalefactors[int(changescale)])*7 ) #then change y
        elif nodediff[1] == 0: #if no change in y
            return (max(nodepair[0][0],nodepair[1][0]) - (scalefactors[int(changescale)])*7 , nodepair[0][1] ) #then change x

class window(navUI):
    def __init__(self, room1, room2,win):
        super().__init__(room1, room2)
        self.win = win
        self.winwidth = 400
        self.winheight = 800
        self.win.geometry(f"{self.winwidth}x{self.winheight}")

        self.imagesizex = 4200
        self.imagesizey = 3138
        self.adjust_x = (self.winwidth)/2
        self.adjust_y = (self.winheight)/2

        self.center_box_size = 3
        self.size = self.center_box_size + 4
        self.makecanvas()

    def makecanvas(self):
        startcoordtempx = -2068-self.adjust_x # the values 2068 and 1608 just depict the start coordinates
        startcoordtempy = -1608-self.adjust_y
        x_coord = (startcoordtempx)+int(self.winwidth)/2
        y_coord = (startcoordtempy)+int(self.winheight)/2
        self.canvas = Canvas(self.win, width=self.imagesizex, height=self.imagesizey, bg="black")
        self.canvas.place(x=x_coord,y=y_coord)
        self.drawcanvas('HamptonMapMyVerChunksCorridorsWithPathSecond.png')
    
    def drawcanvas(self,file): #pass image as the file name
        self.canvas.delete("all")
        self.image = ImageTk.PhotoImage(Image.open(file))
        self.canvas.create_image(0,0,anchor=NW,image=self.image)
        self.win.update()
        print("canvas drawn")

    def start(self):
        self.win.mainloop()    
        
class Travel(window):

    def __init__(self, room1, room2, win):
        super().__init__(room1, room2, win)
        self.count = 0

        image_test = PhotoImage(width=1,height=1)
        testbtn1 = Label(self.win,image=image_test,width=self.center_box_size,height=self.center_box_size,bg="black")
        testbtn1.place(x=(int(self.winwidth)/2),y=(int(self.winheight)/2))
        self.splitnav()

    def getcoords(self,e):
        print(f"coordinates: ({self.canvas.winfo_x()},{self.canvas.winfo_y()})")

    def move(self,dx,dy): #call move dx,dy with either 1,-1,0 to depict how i want movement
        dx = self.size * dx
        dy = self.size * dy
        newx = self.canvas.winfo_x() + dx
        newy = self.canvas.winfo_y() + dy
        self.canvas.place(x=newx,y=newy)
        self.canvas.create_rectangle((-newx+self.adjust_x),(-newy+self.adjust_y),(-newx+self.adjust_x)+self.size,(-newy+self.adjust_y)+self.size,fill="red",width=0) #TRAIL

    def travelup(self,dx=0,dy=1):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelup) #XTX
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelup)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0
            print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")

    def traveldown(self,dx=0,dy=-1):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.traveldown) #XTX
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.traveldown)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0
            print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")

    def travelleft(self,dx=1,dy=0):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelleft) #XTX
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelleft)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0
            print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")
    
    def travelright(self,dx=-1,dy=0):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelright) #XTX
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelright)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0
            print(f"{nodecoordmapper[(x,y)]}:{(x,y)}")

    def navigate(self,floor,path,startroomplace,endroomplace): #pass the floor and path
        if floor == "Ground Floor":
            print("Ground")
            self.nodecoordmapper = self.nodecoordmapperground
            self.drawcanvas('HamptonMapMyVerChunksCorridorsWithPath.png')
        elif floor == "First Floor":
            print("First")
            self.nodecoordmapper = self.nodecoordmapperfirst
            self.drawcanvas('HamptonMapMyVerChunksCorridorsWithPathFirst.png')
        elif floor == "Second Floor":
            print("Second")
            self.nodecoordmapper = self.nodecoordmappersecond
            self.drawcanvas('HamptonMapMyVerChunksCorridorsWithPathSecond.png')
        
        CoordPath = [self.NodeCoords[floor][node]for node in path]
 
        if startroomplace == self.startroomplace:
            print("startroom added")
            CoordPath.insert(0,startroomplace)
            self.nodecoordmapper[startroomplace] = "StartTempNode"
        if endroomplace == self.endroomplace:
            print("endroom added")
            CoordPath.append(self.endroomplace)
            self.nodecoordmapper[self.endroomplace] = "EndTempNode"
        self.canvas.place(x=CoordPath[0][0],y=CoordPath[0][1])
        self.win.update()
        self.win.after(500)

        position = 0
        while (self.canvas.winfo_x(),self.canvas.winfo_y()) != (CoordPath[-1]):
            choice,current_x,current_y = self.autonav(CoordPath,position,floor)
            if choice == "back":
                self.canvas.place(x=current_x,y=current_y)
            else:
                position += 1

    def autonav(self,CoordPath,position,floor):    
        current_x = CoordPath[position][0]
        current_y = CoordPath[position][1]
        next_x = CoordPath[position+1][0]
        next_y = CoordPath[position+1][1]
        if next_y > current_y:
            print("travel up")
            self.travelup()
            self.win.update()
            self.win.after(75)
        if next_y < current_y:
            print("travel down")
            self.traveldown()
            self.win.update()
            self.win.after(75)
        if next_x > current_x:
            print("travel left")
            self.travelleft()
            self.win.update()
            self.win.after(75)
        if next_x < current_x:
            print("travel right")
            self.travelright()
            self.win.update()
            self.win.after(75)
        return None,current_x,current_y
    
    
    def splitnav(self):
        print("navigatiing")
        if self.linkfloors == []:
            print("single floor")
            self.navigate(self.floors[0],self.Nodes,self.startroomplace,self.endroomplace)
        else:
            path = {}
            toadd = []
            nodeconnectionlist = []
            floornum = 0 

            for corridor in self.linkfloors:
                nodeconnectionlist.append(self.linkcorridortonode(corridor[0]))

            for node in self.Nodes:
                toadd.append(node)
                try:
                    if node == nodeconnectionlist[floornum][0]:
                        path[self.floors[floornum]] = toadd
                        toadd = []
                        floornum += 1
                except IndexError:
                    pass
            # print(floornum)
            # print(self.floors)
            # print(path)
            # print(toadd)
            try:
                path[self.floors[floornum]] = toadd
            except IndexError:
                pass
            for part in path:
                print(part,path[part])
            for part in path:
                self.navigate(part, path[part], self.startroomplace if part == self.floors[0] else None, self.endroomplace if part == self.floors[-1] else None) #floor and path

    def linkcorridortonode(self,corridor):
        nodes = []
        for node in self.NodeConnections:
            for neighbournode in self.NodeConnections[node]:
                if self.NodeConnections[node][neighbournode] == corridor:
                    nodes.append(node)
        return nodes

def start(room1="S11",room2="S16"):
    print(room1,room2)
    win = Toplevel()
    travel_interface = Travel(room1,room2,win)
    travel_interface.start()

#start()