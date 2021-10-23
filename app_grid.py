import tkinter as tk
from tkinter import ttk

try: 
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass



root = tk.Tk()
root.title("Amy's auto-clicker")
root.geometry('500x200')
root.columnconfigure(0, weight=1)


gui_frame = ttk.Frame(root, padding=(10,10))
gui_frame.grid(row=0, column=0)



text_input_frame = ttk.Frame(gui_frame)
text_input_frame.grid(row=0, column=0)

input_label = ttk.Label(text_input_frame, text='Hold key for cursor to auto click:') \
    .grid(row=0, column=0)

auto_click_key = tk.StringVar()
input_key = ttk.Entry(text_input_frame, width=3, textvariable=auto_click_key) \
    .grid(row=0, column=1)


def btn_cb_demo(): 
    print('test')


ttk.Button(gui_frame,
    text='Test Button',
    command=btn_cb_demo
).grid()

ttk.Button(gui_frame, text='Exit', command=root.destroy).grid()

root.mainloop()