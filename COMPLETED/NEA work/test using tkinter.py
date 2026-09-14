# from tkinter import *
# 
# root = Tk()
# 
# root.geometry('300x400')
# 
# test1 = Button(root,text='Hello World', font=(("Inter",14)))
# 
# test1.place(relx = 0.5, rely = 2, anchor = CENTER)
# test2.place(relx = 0.5, rely = 2, anchor = CENTER)
# 
# root.mainloop()
# # from tkinter import *
# # from tkinter import ttk
# # root = Tk()
# # frm = ttk.Frame(root, padding=50)
# # frm.grid()
# # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# # ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# # root.mainloop()

# # # import tkinter as tk
# # # 
# # # root = tk.Tk()
# # # root.title("Test App")
# # # 
# # # def on_click():
# # #     lbl.config(text = "Button Clicked")
# # # 
# # # btn = tk.Button(root,text="Test Button", command = on_click)
# # # btn.grid(row = 0, column = 0)
# # # 
# # # lbl = tk.Label(root,text="Test Label")
# # # lbl.grid(row = 0, column = 1)
# # # 
# # # #print(lbl.config().keys()) #to see possible options of config for label
# # # 
# # # root.mainloop()

import tkinter as tk

root = tk.Tk()
root.title("Test app")

def add_to_list():
    text = entry.get()
    if text:
        text_list.insert(tk.END, text)
        entry.delete(0, tk.END)
    
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(1, weight=1)

frame = tk.Frame(root)
frame.grid(row = 0, column = 0, sticky="nsew",padx=5,pady=5)

frame.columnconfigure(0,weight=1)
frame.rowconfigure(1,weight=1)

entry = tk.Entry(frame)
entry.grid(row = 0, column = 0,sticky="ew")

entry.bind("<Return>",lambda event: add_to_list())

entry_btn = tk.Button(frame, text = "Add1",command = add_to_list)
entry_btn.grid(row = 0, column = 1)

text_list = tk.Listbox(frame)
text_list.grid(row = 1, column = 0, columnspan=2,sticky="nsew")


frame2 = tk.Frame(root)
frame2.grid(row = 0, column = 1, sticky="nsew",padx=5,pady=5)

frame2.columnconfigure(0,weight=1)
frame2.rowconfigure(1,weight=1)

entry = tk.Entry(frame2)
entry.grid(row = 0, column = 0,sticky="ew")

entry.bind("<Return>",lambda event: add_to_list())

entry_btn = tk.Button(frame2, text = "Add2",command = add_to_list)
entry_btn.grid(row = 0, column = 1)

text_list2 = tk.Listbox(frame2)
text_list2.grid(row = 1, column = 0, columnspan=2,sticky="nsew")


root.mainloop()
