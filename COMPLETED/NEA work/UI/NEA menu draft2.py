import tkinter as tk
from tkinter import ttk

#Testing to find an optimal screen size (redundant)
'''
def print_size():
    print("window width is: " , root.winfo_width())
    print("window height is: ", root.winfo_height())
button = tk.Button(frm,text="get dimensions", command = print_size).pack()
'''
####

###MAKING FUNCTIONS AND CLASSES###
class Window():
    def __init__(self,root,title):
        self.root = root
        self.title = title
        self.root.title(self.title) #screen name
        self.width = "1200"
        self.height = "550"  
        self.root.geometry(f"{self.width}x{self.height}") #screen size
        
    def setbackground(self,window):
        self.frame = tk.Frame(window,background="light grey") #control the background colour
        self.frame.place(relwidth=1,relheight=1)
    
class MainWindow(Window):
    def __init__(self, root, title):
        super().__init__(root, title)
        self.setbackground(self.root)
        self.settitle()
        
    def settitle(self):
        title_label = ttk.Label(self.root,text=self.title,font=("Comic Sans MS",50,"bold"),borderwidth=5,relief="solid",foreground="red") #intialising the title label
        title_label.place(relx=0.5,rely=0.05,anchor="n") #placing the title label
    
class SubWindow(Window): ##check this is alright
    def __init__(self, root, title,menu):
        super().__init__(root,title)
        self.menu = menu
        self.menu.title(title)
        self.menu.geometry(f"{self.width}x{self.height}")
        self.setbackground(self.menu)
    

class BaseButton():
    def __init__(self,text,position,root):
        self.root = root
        self.text = text
        self.position = position
        #self.button = tk.Button(self.root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14))
        #self.place_button()

    def place_button(self):
        self.button.place(anchor="n",relx=(0.5+((self.position-1)*spacing)),rely=0.4)

class UserOptionButtons(BaseButton):
    def __init__(self, text, position,root,nroot):
        super().__init__(text, position,root)
        self.nroot = nroot
        self.button = tk.Button(root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=self.select)
        self.place_button()

    def select(self):
        global usertype
        usertype = self.text #set the usertype to be whatever is selected from text
        self.root.withdraw() #remove the initial user type option menu
        self.nroot.deiconify() #show the navmenu
        print(usertype)

    def getstate(self):
        return self.text
    
class StartButton(BaseButton):
    def __init__(self, text, position, root):
        super().__init__(text, position, root)
        self.button = tk.Button(root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=self.validation)
        self.place_button()
    
    def validation(self):
        pass
        #bind this function to start button
        #insert some sort of check on drop boxes to see whether something is selected and what is selected in each isnt the same
        #then execute self.start() to start navigation

    def start(self):
        pass

class BackButton(BaseButton):
    def __init__(self, text, position, root, prevwindow):
        super().__init__(text, position, root)
        self.prevwindow = prevwindow
        self.button = tk.Button(root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=self.goback)
        self.place_button()

    def place_button(self):
        self.button.place(anchor="se",relx=1,rely=1)

    def goback(self):
        self.root.withdraw()
        self.prevwindow.deiconify()

class DropDown():
    def __init__(self,root,list,text,row,column):
        self.root = root
        self.list = list
        self.text = text
        self.row = row
        self.column = column
        self.setup()

    def setup(self):
        self.dropdownbox = ttk.Combobox(self.root,values=self.list,width=16,font=("Arial",15),foreground="dark blue")
        self.dropdownbox.set("Select a point")
        self.label = ttk.Label(self.root,text=(f'Select a {self.text}:'),font=("Arial",15,"bold"))
        self.label.grid(row=self.row,column=self.column)
        self.dropdownbox.grid(row=self.row+1,column=self.column)
        
    def get_content(self):
        return self.dropdownbox.get()
#####

 

spacing = 0.25 #spacing that determines space between buttons for quality of life changes
usertype = "" #currently the selected usertype is being obtained by assignemnt on a global variable but consider finding a way to change this later using get methods

root = tk.Tk() #intialise "screen"
win = MainWindow(root, "Navigation App")
navmenu = tk.Toplevel(root)
menufornav = SubWindow(root,"NavMenu",navmenu)

UserOptionButtons("Lower School \nStudents",0,root,navmenu) #setting up differnt user option buttons
UserOptionButtons("Sixth Form \nStudents",1,root,navmenu)
UserOptionButtons("Teachers",2,root,navmenu)

StartButton("Start",1.5,navmenu)
BackButton("Back",0,navmenu,root)

frameNav = tk.Frame(navmenu,bg="light grey")
frameNav.pack(anchor="nw",padx=5,pady=5)

#insert the actual map or import it here for group
group = ["TestA","TestB","TestC","TestD"]

StartPoint = DropDown(frameNav,group,"Start Point",0,0)
EndPoint = DropDown(frameNav,group,"End Point",0,1)

navmenu.withdraw() #remove excess screens like the navmenu
root.mainloop() #start screen

