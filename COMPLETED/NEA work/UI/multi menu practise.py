import tkinter as tk

root1 = tk.Tk()
root1.title("Menu 1")
root1.geometry("1250x500")

root2 = tk.Toplevel(root1)
root2.title("Menu 2")
root2.geometry("1250x500")

def goto_menu1():
    root2.withdraw()
    root1.deiconify()

def goto_menu2():
    #root1.withdraw()
    root2.deiconify()

magicnumber = 25
def getbig():
    global magicnumber
    magicnumber += 3
    buttonC.configure(font=("Arial",magicnumber)) #only works if the buttonC is an object not packed withing its assignment
    #buttonC = tk.Button(root2,text="A cool button",font=("Comic Sans MS",magicnumber),command=getbig).pack(padx=10,pady=10)

label = tk.Label(root1,text="MENU 1",font=("Arial",25)).pack(pady=10)
button = tk.Button(root1,text="Show menu 2",font=("Arial",10),command=goto_menu2).pack(pady=20)

label = tk.Label(root2,text="MENU 2",font=("Arial",25)).pack(pady=10)
button = tk.Button(root2,text="Show menu 1",font=("Arial",10),command=goto_menu1).pack(pady=20)
buttonC = tk.Button(root2,text="A cool button",font=("Comic Sans MS",25),command=(getbig),relief="solid")
buttonC.pack(padx=10,pady=10)

root2.withdraw()
root1.mainloop()


