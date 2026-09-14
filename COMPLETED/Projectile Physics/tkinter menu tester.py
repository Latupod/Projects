import tkinter as tk
import draft5

root = tk.Tk()
root.title("Menu")

button = tk.Button(root,text = "Projectile Motion",command = draft5.start())

root.mainloop()