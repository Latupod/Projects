# Importing the required libraries
from tkinter import * #Used to run GUI
from PIL import Image, ImageTk #Used to load images into GUI
import MainProgram #Used to perform shortest path algorithm


class navUI():
    def __init__(self,startroom,endroom):
        #Won't both explaining some of the below as theyre explained in Data.py
        self.NodeConnections = MainProgram.NodeConnections
        self.CorridorFloorMapper = MainProgram.CorridorFloorMapper 
        self.NodeCoords = MainProgram.NodeCoords 
        self.Nodes,self.Corridors,startnodepair,endnodepair,startroomplace,endroomplace,self.floors = MainProgram.maincode(startroom,endroom)
        #each nodecoordmapper produces a dictionary mapping each node to its coordinates for each individual floor
        self.nodecoordmapperground = {self.NodeCoords["Ground Floor"][node]:node for node in self.NodeCoords["Ground Floor"]} 
        self.nodecoordmapperfirst = {self.NodeCoords["First Floor"][node]:node for node in self.NodeCoords["First Floor"]}
        self.nodecoordmappersecond = {self.NodeCoords["Second Floor"][node]:node for node in self.NodeCoords["Second Floor"]}
        self.startroomplace = self.getnodepos(self.floors[0],startroomplace,startnodepair) #returns the coordinates of the start room
        self.endroomplace = self.getnodepos(self.floors[-1],endroomplace,endnodepair) #returns the coordinates of the end room
        self.linkfloors = self.checkfloors() #sets the linkfloors list to the result of the checkfloors function (below), 
                                            #linkfloors stores any corridors involved in linking floors together in navigations
    
    def checkfloors(self,linkfloors = []): #checks what floors are involved in the navigation e.g. ground to first or first to second or both (so ground to second)
        for corridor in self.Corridors: #for each corridor in the corridors involved in the path 
            if corridor in self.CorridorFloorMapper["Ground-First Floor"]: #if the corridor is in the ground-first floor section, 
                linkfloors.append([corridor,"Ground-First"]) #recongise that ground and first floors are involved, and note which corridor is causing this
            elif corridor in self.CorridorFloorMapper["First-Second Floor"]: #if the corridor is in the first-second floor section, 
                linkfloors.append([corridor,"First-Second"]) #recongise that first and second floors are involved, and note which corridor is causing this
        if len(linkfloors) == 2: #if the length of the list linkfloors is 2, i.e. both Ground-First and First-Ground connectors are involved then all 3 floors must be involved
            self.floors = ["Ground Floor","First Floor","Second Floor"] #so set the floors list to contain all 3 floors
        return linkfloors #return the linkfloors list, if empty then all navigation occurs on one floor

    def getnodepos(self,floor,roomplace,nodepair): #function to obtain the coordinates of a room with respect to their node pairs (for the start and end node pairs)
        nodepair = (self.NodeCoords[floor][nodepair[0]],self.NodeCoords[floor][nodepair[1]]) #convert the node pair to their coordinates
        nodediff = (abs(nodepair[1][0] - nodepair[0][0]),abs(nodepair[1][1] - nodepair[0][1])) #find the magnitudinal difference between the x,y coordinates of the pair values
        nodesections = int(nodediff[1]/7) if nodediff[0] == 0 else int(nodediff[0]/7) #split this difference into sections of length 7 (the amount the navigation animates at)
        return self.findroomcoord(nodediff,nodepair,roomplace[0],nodesections) #return the above data to a function that will calculate the room coordinates between its node pairs

    def findroomcoord(self,nodediff,nodepair,changescale,sections,displacement = 0): #using maths to work out the position of a room in a corridor
        #I won't comment this all as it's too complex to explain each individual lines purpose without being extremely messy
        #But this process is all described in the Design process of the document under Design/Path Finding Algorithm:Encoding the Map (Graphing)
        sections = int(sections)
        remainder = sections % 10
        try:
            addcoord = 10 // remainder
        except ZeroDivisionError: #if remainder is zero, then except a zero division error and just consider addcord as 0
            addcoord = 0
        jump = sections // 10
        scalefactors = []
        for pos in range(1,11):
            try:
                if (pos % addcoord) == 0:
                    if displacement < remainder:
                        displacement += 1
            except ZeroDivisionError:
                pass
            scalefactors.append(jump*pos + displacement)
        if nodediff[0] == 0: #if no change in x
            return (nodepair[0][0] , min(nodepair[0][1],nodepair[1][1]) + (scalefactors[int(changescale)])*7 ) #then change y, min() applied to select the bottom most node
        elif nodediff[1] == 0: #if no change in y
            return (max(nodepair[0][0],nodepair[1][0]) - (scalefactors[int(changescale)])*7 , nodepair[0][1] ) #then change x, max() applied to select the left most node

class window(navUI):#inherits from navUI
    def __init__(self, startroom, endroom,win):
        super().__init__(startroom, endroom)
        self.win = win #the screen/window of interest
        self.winwidth = 400 # the screen/window height
        self.winheight = 800 # the screen/window width
        self.win.geometry(f"{self.winwidth}x{self.winheight}") # the screen/window size

        self.imagesizex = 4200 # the image x-dimension (width)
        self.imagesizey = 3138 # the image y-dimension (height)
        self.adjust_x = (self.winwidth)/2 # the adjustment in x-dimension to centre the image with the screen
        self.adjust_y = (self.winheight)/2 # the adjustment in y-dimension to centre the image with the screen

        self.center_box_size = 3 #the size of the centre box (the user that appears on the screen and shows where you are)
        self.size = self.center_box_size + 4 #the amount the box moves with each movement
        self.makecanvas() #run canvas making procedure

    def makecanvas(self):
        startcoordtempx = -2068-self.adjust_x # the values 2068 and 1608 just depict the start coordinates
        startcoordtempy = -1608-self.adjust_y
        x_coord = (startcoordtempx)+int(self.winwidth)/2 # the start coordinates of the image with accounting with the dimension adjustments of the screensize 
        y_coord = (startcoordtempy)+int(self.winheight)/2
        self.canvas = Canvas(self.win, width=self.imagesizex, height=self.imagesizey, bg="black") #initialising the cavnvas that the map and trail act on
        self.canvas.place(x=x_coord,y=y_coord) #place the canvas 
    
    def drawcanvas(self,file): #pass image as the file name
        self.canvas.delete("all") #remove all object on canvas (wipe it clean)
        self.image = ImageTk.PhotoImage(Image.open(file))#load the relevant image
        self.canvas.create_image(0,0,anchor=NW,image=self.image)#place the image onto the canvas
        self.win.update() #update screen/window

    def start(self):
        self.win.mainloop() #start navigation screen
        
class Travel(window):#inherits from the Window class, the main class responsible for actual animation of the navigation on the GUI
    def __init__(self, startroom, endroom, win):
        super().__init__(startroom, endroom, win)
        self.count = 0 #used as a boolean flag to determine whether the map is in motion between nodes
        image_test = PhotoImage(width=1,height=1) #load a square box (to act as the user)
        testbtn1 = Label(self.win,image=image_test,width=self.center_box_size,height=self.center_box_size,bg="black") #intialise a black box as the user
        testbtn1.place(x=(int(self.winwidth)/2),y=(int(self.winheight)/2)) #place the user in the centre of the screen/window
        self.splitnav() #start splitnav function

    def getcoords(self,e): #function that returns the current coordinates
        print(f"coordinates: ({self.canvas.winfo_x()},{self.canvas.winfo_y()})")

    def move(self,dx,dy): #function to move the user (or actually the canvas but thats explained further in the Design of the document) dx,dy are either 0,1,-1
        dx = self.size * dx #set change in x as the produce of the movement constant (self.size) and the desired change in x  
        dy = self.size * dy #set change in y as the produce of the movement constant (self.size) and the desired change in y  
        newx = self.canvas.winfo_x() + dx #work out new coordinates of canvas
        newy = self.canvas.winfo_y() + dy
        self.canvas.place(x=newx,y=newy) #place the new canvas
        self.canvas.create_rectangle((-newx+self.adjust_x),(-newy+self.adjust_y),(-newx+self.adjust_x)+self.size,(-newy+self.adjust_y)+self.size,fill="red",width=0) 
        #create a rectangle at the previous position, such creating a trail of the path taken

    # as the next few function are almost identical, I will only comment travelup in detail and the following are self explanatory from such
    def travelup(self,dx=0,dy=1): #function to travel up until a node is reached, the significance of dx,dy are also exaplained in the document in detail so won't explain here
        nodecoordmapper = self.nodecoordmapper #setup the node coordinate mapping list 
        x = self.canvas.winfo_x() # get current canvas coordinates
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper: #if the coordinates are not a node
            self.count = 1 #set the count to 1 (set to be in motion)
            self.move(dx,dy) #move the canvas according to dx,dy
            self.win.after(1,self.travelup) #recursively call the travelup function 
        elif (x,y) in nodecoordmapper and self.count == 0: #if current coordinates are a node but the count is zero (i.e. we havent started moving yet)
            self.count = 1 #set the count to 1 (set to be in motion)
            self.move(dx,dy) #move the canvas according to dx,dy
            self.win.after(1,self.travelup) #recursively call the travelup function 
        elif (x,y) in nodecoordmapper and self.count != 0: #if the current coordinates are a node and count isnt zero (i.e. we are in motion)
            self.count = 0 #then set the count to be zero so we are not in motion and dont recursivly call any more

    def traveldown(self,dx=0,dy=-1):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.traveldown) 
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.traveldown)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0

    def travelleft(self,dx=1,dy=0):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelleft) 
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelleft)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0
    
    def travelright(self,dx=-1,dy=0):
        nodecoordmapper = self.nodecoordmapper
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        if (x,y) not in nodecoordmapper:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelright) 
        elif (x,y) in nodecoordmapper and self.count == 0:
            self.count = 1
            self.move(dx,dy)
            self.win.after(1,self.travelright)
        elif (x,y) in nodecoordmapper and self.count != 0:
            self.count = 0

    def navigate(self,floor,path,startroomplace,endroomplace): #function to start the navigation for a certain floor, passing the floor, path and start and end room coordinates
        if floor == "Ground Floor": #if the floor of interest is the ground floor
            self.nodecoordmapper = self.nodecoordmapperground #set the node to coordinate mapping list to be for the ground floor
            self.drawcanvas('HamptonMapMyVerGroundFloor.drawio.png') #load the ground floor map to the canvas
        elif floor == "First Floor": #same as above but for first floor
            self.nodecoordmapper = self.nodecoordmapperfirst
            self.drawcanvas('HamptonMapMyVerFirstFloor.drawio.png')
        elif floor == "Second Floor": #same as above but for second floor
            self.nodecoordmapper = self.nodecoordmappersecond
            self.drawcanvas('HamptonMapMyVerSecondFloor.drawio.png')
        
        CoordPath = [self.NodeCoords[floor][node]for node in path] #convert the path of nodes into coordinates
 
        if startroomplace == self.startroomplace: #if the start room is on the floor being navigated 
            CoordPath.insert(0,startroomplace) #add start room coordinates to the from coordinate path list
            self.nodecoordmapper[startroomplace] = "StartTempNode" #add the start room coordinates to the node coordinate mapping list
        if endroomplace == self.endroomplace: #the same idea for the endnode instead
            CoordPath.append(self.endroomplace) #the end room coordiantes added to end of the coordinate path list
            self.nodecoordmapper[self.endroomplace] = "EndTempNode"
        self.canvas.place(x=CoordPath[0][0],y=CoordPath[0][1]) #place the canvas at the start node of the path
        self.win.update() #update the screen/window
        self.win.after(500) #wait 5 seconds before starting the navigation
        self.lastchoice = "" #initialise the last navigation choice made (for the verbal descriptive process)
        position = 0 #initialist the position that navigation is in along the CoordPath to be 0
        while (self.canvas.winfo_x(),self.canvas.winfo_y()) != (CoordPath[-1]): #while the current coordinates are not the final coordinates in the list
            choice,current_x,current_y = self.autonav(CoordPath,position) #run the autonav function (returns values which are used for different higher level objective)
            position += 1 #increment the position by 1

    def autonav(self,CoordPath,position):#Function to perform the auto navigation
        current_x = CoordPath[position][0] #set current x as the node coordinate according to the position in navigation
        current_y = CoordPath[position][1] #set current y as the node coordinate according to the position in navigation
        next_x = CoordPath[position+1][0] #set next x as the node coordinate for the next position in navigation
        next_y = CoordPath[position+1][1] #set next y as the node coordinate for the next position in navigation
        if next_y > current_y: #if next y coordinate is greater than the current y 
            if self.lastchoice == "up": #if the lastchoice in the navigation was to go up,
                print("Continue down corridor") #then still going up so continue down corridor
            else:
                print("Go up corridor") #otherwise print instruction to go up corridor 
            self.travelup() #call the travelup function
            self.win.update() #update the screen/window
            self.lastchoice = "up" #set the lastchoice in the navigation as up
            self.win.after(75) #wait 0.75 seconds (delay to make the navigation easier to understand on GUI)
        #the below is the same code but for each other direction so won't bother commenting again
        if next_y < current_y:
            if self.lastchoice == "down":
                print("Continue down corridor")
            else:
                print("travel down")
            self.traveldown()
            self.win.update()
            self.lastchoice = "down"
            self.win.after(75)
        if next_x > current_x:
            if self.lastchoice == "left":
                print("Continue down corridor")
            else:
                print("travel left")
            self.travelleft()
            self.win.update()
            self.lastchoice = "left"
            self.win.after(75)
        if next_x < current_x:
            if self.lastchoice == "right":
                print("Continue down corridor")
            else:
                print("travel right")
            self.travelright()
            self.win.update()
            self.lastchoice = "right"
            self.win.after(75)
        return None,current_x,current_y #return statement not relevant here, user for a different high level objective
    
    
    def splitnav(self): #an intermediate to the navigation that ensure navigation is carried out one floor at a time 
        if self.linkfloors == []: #if the linkfloors list is empty, then all navigation must happen on the same floor
            self.navigate(self.floors[0],self.Nodes,self.startroomplace,self.endroomplace) #so simply run navigate straight away
        else: 
            path = {} #initialise the path dictionary to split the path into subpath for each floor
            toadd = [] #temporary list to add to the paths list
            nodeconnectionlist = [] #initialise list of nodes from corridors
            floornum = 0 #initialise the floor number index

            for corridor in self.linkfloors: #for each corridor in linkfloors list
                nodeconnectionlist.append(self.linkcorridortonode(corridor[0])) #add to the nodeconnections, the nodes connected to the corresponding corridor

            for node in self.Nodes: #for each node in the node path
                toadd.append(node) #add this node to the temporay list
                try:
                    if node == nodeconnectionlist[floornum][0]: #if the current node being looked at is used at somepoint in connecting floors
                        path[self.floors[floornum]] = toadd #add this to the path dictionary with the key of the current floor index
                        toadd = [] #reset the temporary variable
                        floornum += 1 #increment the floor number by 1
                except IndexError: 
                    pass

            try:
                path[self.floors[floornum]] = toadd #add remaining nodes in temporary list to the path under the key of the current floor index
            except IndexError:
                pass

            for part in path: #for each part of the path (as path has now been split into floor by floor navigation)
                self.navigate(part, path[part], self.startroomplace if part == self.floors[0] else None, self.endroomplace if part == self.floors[-1] else None) 
                #call the navigate function to navigate the current floor
                # if the floor is the start floor involved in navigation also pass the start room coordinates, 
                # likewise, if the floor is the end floor involved in navigation also pass the end room cooridnates 
                print("Take stairs") #print to take stairs as one part of navigation is now complete for a certain floor

    #may notice that function below is same as the one used in MainProgram.py, been copied here as I cannot directly call and reuse the one in MainProgram.py
    #as it acts on a different set of lists (e.g. here its specfically self.NodeConnections), so was simpler to copy the function rather rewrite it to pass these lists
    def linkcorridortonode(self,corridor): #self explanatory but returns the link between each corridor and its two connection nodes (as each corridor has a node either side)
        nodes = [] #initialise the nodes list
        for node in self.NodeConnections: #for each node that exists
            for neighbournode in self.NodeConnections[node]: #for each neighbouring node to that current node
                if self.NodeConnections[node][neighbournode] == corridor: #if the link (corridor) between these two nodes is the corridor of interest
                    nodes.append(node) #add the current node to the nodes list
                    nodes.append(neighbournode) #add the neighbouring node to the nodes list
            if len(nodes) == 2: #if the length of the nodes list is 2, then as any corridor can only have 2 node connections, then we know we are done
                break #so stop the for loop
        return nodes #return the nodes list

def start(startroom=None,endroom=None): 
    win = Toplevel() #initialise the window
    travel_interface = Travel(startroom,endroom,win)
    travel_interface.start() #start the navigation
