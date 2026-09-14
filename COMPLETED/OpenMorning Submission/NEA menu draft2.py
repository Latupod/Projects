import tkinter as tk
from tkinter import ttk,messagebox
import Data
import navigator2
import freeviewnavigation
import selectlogins
import registerlogin

CorridorContent = Data.CorridorContent
rooms = [room[1:] for key in CorridorContent for room in CorridorContent[key]]

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
        self.spacing = 0.25 #spacing that determines space between buttons for quality of life changes
        self.root = root
        self.text = text
        self.position = position
        #self.button = tk.Button(self.root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14))
        #self.place_button()

    def place_button(self):
        self.button.place(anchor="n",relx=(0.5+((self.position-1)*self.spacing)),rely=0.4)

class CommandButton(BaseButton):
    def __init__(self, text, position, root,command):
        super().__init__(text, position, root)
        self.button = tk.Button(self.root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=command)
        self.place_button()

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
    def __init__(self, text, position, root,startpoint,endpoint):
        super().__init__(text, position, root)
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.button = tk.Button(root,text=self.text,height=4,width=15,foreground="white",background="light blue",font=("Arial",14),command=self.validation)
        self.place_button()
    
    def validation(self):
        self.startroom = self.startpoint.get_content()
        self.endroom = self.endpoint.get_content()
        print(self.startroom,self.endroom)
        print(type(self.startroom),type(self.endroom))
        if self.startroom != self.endroom:
            self.start()

    def start(self):
        return navigator2.start(self.startroom,self.endroom)

class BackButton(BaseButton):
    def __init__(self, text, position, root, prevwindow,fontsize,width,height):
        super().__init__(text, position, root)
        self.prevwindow = prevwindow
        self.button = tk.Button(root,text=self.text,height=height,width=width,foreground="white",background="light blue",font=("Arial",fontsize),command=self.goback)
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
 
class BasePage():
    def __init__(self,root,nroot):
        self.root = root
        self.nroot = nroot
        self.root.geometry("500x300")
        self.frame = tk.Frame(root,background="light grey") #control the background colour
        self.frame.place(relwidth=1,relheight=1)
        self.logins = []

    def makepage(self,text,command):
        username_label = tk.Label(self.frame,text="UserID",height=2,width=8,foreground="white",background="light blue",font=("Arial",10))
        username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()
        self.password_label = tk.Label(self.frame,text="Password",height=2,width=8,foreground="white",background="light blue",font=("Arial",10))
        self.password_label.pack()
        if text == "Login":
            self.password_entry = tk.Entry(self.frame, show="*")  
        else:
            self.password_entry = tk.Entry(self.frame)  

        self.password_entry.pack()
        login_button = tk.Button(self.frame,text=text,height=2,width=8,foreground="white",background="light blue",font=("Arial",10),command=command)
        login_button.pack()

class Login(BasePage):
    def __init__(self, root, nroot):
        super().__init__(root, nroot)
        self.makepage("Login",self.validate_login)

    def validate_login(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()
        #user_pass = selectlogins.selectlogins()
        #if (userid,password) in user_pass:
        if True:
            messagebox.showinfo("Login Successful", "Welcome, user")
            self.root.withdraw
            self.nroot.deiconify()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password") 

class Register(BasePage):
    def __init__(self, root, nroot):
        super().__init__(root, nroot)
        self.makepage("Register",self.confirmchoice)
    
    def confirmchoice(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()
        registerlogin.register(userid,password)
        self.root.withdraw
        self.nroot.deiconify()

root = tk.Tk() #intialise "screen"
win = MainWindow(root, "Navigation App")

navmenu = tk.Toplevel(root)
menufornav = SubWindow(root,"NavMenu",navmenu)

login_register_page = tk.Toplevel(root)
menuforlogin_register = SubWindow(root,"Login/Register",login_register_page)

loginpage = tk.Toplevel()
menuforlogin = SubWindow(root,"Login",loginpage)

registerpage = tk.Toplevel()
menuforregister = SubWindow(root,"Register",registerpage)

timetable = tk.Toplevel()
menufortimetable = SubWindow(root,"Timetable",timetable)

freeviewnav = freeviewnavigation.start
CommandButton("FreeView",0,root,freeviewnav)
UserOptionButtons("Navigation",1,root,navmenu)
UserOptionButtons("Login/Register",2,root,login_register_page)

UserOptionButtons("Login",0,login_register_page,loginpage)
UserOptionButtons("Register",1,login_register_page,registerpage)

Login(loginpage,timetable)
Register(registerpage,timetable)


BackButton("Back",0,login_register_page,root,14,15,4)
BackButton("Back",0,loginpage,login_register_page,8,10,4)
BackButton("Back",0,registerpage,login_register_page,8,10,4)

frameNav = tk.Frame(navmenu,bg="light grey")
frameNav.pack(anchor="nw",padx=5,pady=5)

StartPoint = DropDown(frameNav,rooms,"Start Point",0,0)
EndPoint = DropDown(frameNav,rooms,"End Point",0,1)

StartButton("Start",1.5,navmenu,StartPoint,EndPoint)
BackButton("Back",0,navmenu,root,14,15,4)

navmenu.withdraw() #remove excess screens like the navmenu
login_register_page.withdraw()
loginpage.withdraw()
registerpage.withdraw()
timetable.withdraw()
root.mainloop() #start screen

