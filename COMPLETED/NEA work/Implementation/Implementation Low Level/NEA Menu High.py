import tkinter as tk
from tkinter import ttk,messagebox
import Data
import MainProgram
import Navigation
import FreeViewNavigation

CorridorContent = Data.CorridorContent
rooms = [room[1:] for key in CorridorContent for room in CorridorContent[key]]

###MAKING FUNCTIONS AND CLASSES###
class Window():
    def __init__(self,root,title): 
        self.root = root #the screen/window being used
        self.title = title #title of the screen/window
        self.root.title(self.title) #setting up the screen/window name
        self.width = "1200" #defining the screen/window width
        self.height = "550" #defining the screen/window height
        self.root.geometry(f"{self.width}x{self.height}") #setting up the screen/window size
        
    def setbackground(self,window):
        self.frame = tk.Frame(window,background="light grey") #control the background colour
        self.frame.place(relwidth=1,relheight=1) #Place the frame (background) onto the screen
    
class MainWindow(Window):#inherit from the Window Class, this class is exclusively for the main starting window
    def __init__(self, root, title):
        super().__init__(root, title)
        self.setbackground(self.root) #set up background on the screen/window
        self.settitle()
        
    def settitle(self): #sets up the title of the screen/window using a label  
        title_label = ttk.Label(self.root,text=self.title,font=("Comic Sans MS",50,"bold"),borderwidth=5,relief="solid",foreground="red") #intialising the title label
        title_label.place(relx=0.5,rely=0.05,anchor="n") #placing the title label
    
class SubWindow(Window): #inherit from the Window class, used to produce every other window other than the main starting window
    def __init__(self, root, title,menu):
        super().__init__(root,title)
        self.menu = menu #screen/window that is now being enacted on, root now refers to the original window
        self.menu.title(title) #title of the screen/window\
        self.menu.geometry(f"{self.width}x{self.height}")
        self.setbackground(self.menu) #setting up the screen/window size

class BaseButton():
    def __init__(self,text,position,root):
        self.spacing = 0.25 #spacing that determines space between buttons for quality of life changes
        self.root = root # screen/window the button will be placed on
        self.text = text # text of button
        self.position = position #position of button

    def place_button(self):
        self.button.place(anchor="n",relx=(0.5+((self.position-1)*self.spacing)),rely=0.4) #placing button on screen with relevant position

class CommandButton(BaseButton): #inherit from BaseButton, this class will be used to directly execute functions from a menu if an intermediate menu is not required
    def __init__(self, text, position, root,command):
        super().__init__(text, position, root)
        self.button = tk.Button(self.root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=command)
        self.place_button()

class UserOptionButtons(BaseButton):#inherit from BaseButton, this class will be the building block to navigate beteen screens/windows
    def __init__(self, text, position,root,nroot):
        super().__init__(text, position,root)
        self.nroot = nroot #the newwindow that the button will navigate to
        self.button = tk.Button(root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=self.select) #setup button 
        self.place_button() #run button placing procedure

    def select(self): 
        self.root.withdraw() #remove the original screen/window
        self.nroot.deiconify() #show the new screen/window

    def getstate(self):
        return self.text
    
class StartButton(BaseButton):#inherit from BaseButton, used exclusively to start the navigation
    def __init__(self, text, position, root,startpoint,endpoint):
        super().__init__(text, position, root)
        self.startpoint = startpoint #dropdownbox contatining the startpoint room
        self.endpoint = endpoint #dropdownbox contatining the endpoint room
        self.button = tk.Button(root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=self.validation) #setup button
        self.place_button() #run button placing procedure
    
    def validation(self): #checking if the rooms are valid to be navigated
        self.startroom = self.startpoint.get_content() #Get the startpoint room choice
        self.endroom = self.endpoint.get_content() #Get the endpoint room choice
        info = [] #initialise info list, to hold information about rooms
        try:
            mapper = list(Data.CorridorContent.items()) #convert Corridor content dictionary into a list
            info.append(MainProgram.findroomtocorridor(self.startroom,mapper)) #adding room information 
            info.append(MainProgram.findroomtocorridor(self.endroom,mapper))
        except IndexError: #If the no inputs are given then index error will occur, so we know inputs are just invalid
            messagebox.showerror("Python Error","Invalid Inputs") #raise an error messagebox if inputs are not valid
        if info[0][1] == info[1][1]: #if corridor of rooms are the same
            messagebox.showerror("Python Error","Rooms in same corridor") #raises an error message box
        elif (self.startroom != self.endroom) and ((self.startroom != "Select a point") and (self.endroom != "Select a point")): #If the startroom and endroom are not the same 
                                                                                                                            # and are actually rooms (not the default option)
            self.start() #If so start procedure
        else:
            messagebox.showerror("Python Error","Invalid Inputs") #raise an error messagebox if inputs are not valid

    def start(self):
        return Navigation.start(self.startroom,self.endroom) #Start navigation code

class BackButton(BaseButton):#inherit from BaseButton, exclusive back button for navigating between screens/windows 
    def __init__(self, text, position, root, prevwindow,fontsize,width,height):# position inherited from BaseButton but not necessary here
                                                                                #root is the current screen/window
                                                                                #prevwindow is the previous screen/window that will go back to
                                                                                #the following: fontsize,width,height are self-explanatory 
        super().__init__(text, position, root)
        self.prevwindow = prevwindow #setup previous window
        self.button = tk.Button(root,text=self.text,height=height,width=width,foreground="white",background="light blue",font=("Arial",fontsize),command=self.goback) #setup button
        self.place_button() #run button placing procedure

    def place_button(self):
        self.button.place(anchor="se",relx=1,rely=1) #placing the button in the bottom right

    def goback(self): #procedure to swap screens/windows
        self.root.withdraw() #minimise current screen/window
        self.prevwindow.deiconify() #show previous screen/window

class DropDown():
    def __init__(self,root,list,text,row,column):
        self.root = root #screen/window that dropdown box will act on
        self.list = list #the content of the dropdown box
        self.text = text #the variable being selected (in this case it will be the rooms)
        self.row = row #the row the dropdown box should be (relevance explained better in the setup procedure)
        self.column = column #the column the dropdown box should be (relevance explained better in the setup procedure)
        self.setup() #run dropdown box setup procedure

    def setup(self):
        self.dropdownbox = ttk.Combobox(self.root,values=self.list,width=16,font=("Arial",15),foreground="dark blue") #setting up actualy dropdown box
        self.dropdownbox.set("Select a point") #Set the default option/prompt
        self.label = ttk.Label(self.root,text=(f'Select a {self.text}:'),font=("Arial",15,"bold")) #setup a label for the dropdown box to desribe what is being selected
        self.label.grid(row=self.row,column=self.column) #place the label in a "grid" format 
        self.dropdownbox.grid(row=self.row+1,column=self.column) #place the dropdown box in a "grid" format
        
    def get_content(self):
        return self.dropdownbox.get() #get the selection from the dropdown box

'''MAIN WINDOW'''
root = tk.Tk() #intialise main screen/window
win = MainWindow(root, "Navigation App") #Create the main window display

'''NAVIGATION MENU'''
navmenu = tk.Toplevel(root) #intialise screen/window for choosing rooms
menufornav = SubWindow(root,"NavMenu",navmenu) #Create subwindow for navmenu
UserOptionButtons("Navigation",1.5,root,navmenu) #Create a button on the mainwindow for navigating to the navmenu
frameNav = tk.Frame(navmenu,bg="light grey") #Create a frame on the navmenu
frameNav.pack(anchor="nw",padx=5,pady=5) #place frame on navmenu
StartPoint = DropDown(frameNav,rooms,"Start Point",0,0) #Create dropdownbox for startpoint
EndPoint = DropDown(frameNav,rooms,"End Point",0,1) #Create dropdownbox for endpoint
StartButton("Start",1.5,navmenu,StartPoint,EndPoint) #Create startbutton to start the navigation process 
BackButton("Back",0,navmenu,root,14,15,4) #Back button to go back to main screen/window from navmenu

'''FREEVIEW MENU'''
freeviewmenu = tk.Toplevel(root) #intialise screen/window for choosing floor to do the freeviewnavigation
menuforfreeview = SubWindow(root,"Freeview",freeviewmenu) #Create subwindow for freeviewmenu
freeviewnavground = FreeViewNavigation.startground #Setup method to call the freeviewnavigation code for ground floor
freeviewnavfirst = FreeViewNavigation.startfirst #Setup method to call the freeviewnavigation code for first floor
freeviewnavsecond = FreeViewNavigation.startsecond #Setup method to call the freeviewnavigation code for second floor
UserOptionButtons("FreeViewMenu",0.5,root,freeviewmenu) #Create a button on the mainwindow for navigating to the freeviewmenu
Ground = CommandButton("Ground Floor",0,freeviewmenu,freeviewnavground) #Bind this above method to the freeviewmenu for ground floor navigation
First = CommandButton("First Floor",1,freeviewmenu,freeviewnavfirst) #Bind this above method to the freeviewmenu for first floor navigation
Second = CommandButton("Second Floor",2,freeviewmenu,freeviewnavsecond) #Bind this above method to the freeviewmenu for second floor navigation
BackButton("Back",0,freeviewmenu,root,14,15,4) #Back button to go back to main screen/window from navmenu

#Minimises all windows except the mainwindow
freeviewmenu.withdraw()
navmenu.withdraw() 

root.mainloop() #start screen