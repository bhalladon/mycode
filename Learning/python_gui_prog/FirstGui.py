import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title("Python GUI")
#win.resizable(0, 0)
ttk.Label(win, text="A label").grid(column=1,row=1)
win.mainloop()
