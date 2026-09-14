import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("Test App Using Classes")
#root.geometry("300x300")
root.rowconfigure(0,weight=1)

class MakeTextBox():
    def __init__(self,Frow,Fcolumn): 
        root.columnconfigure(Fcolumn,weight=1)

        self.frame = ttk.Frame(root)
        self.frame.columnconfigure(Fcolumn,weight=1)
        self.frame.rowconfigure(Frow+1,weight=1) 
        self.frame.grid(row = Frow, column = Fcolumn, sticky="nsew",padx=10,pady=10)
        self.createstuff()    

    def createstuff(self):
        self.entry = ttk.Entry(self.frame)
        self.entry.grid(row=0,column=0,sticky="ew")
        self.entry.bind("<Return>",lambda x: self.add_to_list())
        self.text_list = tk.Listbox(self.frame)
        self.text_list.grid(row=1,column=0,columnspan=2,sticky="nsew")
        
    def add_to_list(self):
        text = self.entry.get()
        if text:
            self.text_list.insert(tk.END,text)
            self.entry.delete(0,tk.END)

box = MakeTextBox(0,0)
box2 = MakeTextBox(0,1)

root.mainloop()