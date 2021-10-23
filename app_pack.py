from operator import truediv
import tkinter as tk
from tkinter import ttk
import time
import random
import numpy as np
import threading
from numpy.lib.function_base import delete
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# reference: https://www.youtube.com/watch?v=eamTeszpeZ4
class AutoClicker(): 
    program_running: bool
    # max_clicks: int
    __click_counter: int
    __display_remaining_counter_label: ttk.Label
    __key: str
    __mouse: Controller
    __event_listener: Listener

    def __init__(self, key: str = 's'): 
        super().__init__()
        self.__mouse = Controller()
        self.__key = key
        self.program_running = False

    def setKey(self, key): 
        self.__key = key
    
    def updateCounter(self): 
        self.__click_counter

    def enable(self, init_click_counter: str, display_label: ttk.Label=None): 
        init_counter = int(init_click_counter)
        if(display_label is not None): 
                self.__display_remaining_counter_label = display_label

        if(init_counter == 0): 
            init_counter = -1
            if(self.__display_remaining_counter_label):
                self.__display_remaining_counter_label.config(text=f'Clicks remaining: Infinit')

        if(not self.program_running): 
            self.__click_counter = init_counter
            self.program_running = True
            self.__event_listener = None
            self.__event_listener = Listener(on_press=self.__key_press_event)
            self.__event_listener.start()

    def reset_counter(self, reset_clicks: str): 
        init_counter = int(reset_clicks)
        if(init_counter == 0): 
            init_counter = -1
            if(self.__display_remaining_counter_label):
                self.__display_remaining_counter_label.config(text=f'Clicks remaining: Infinit')
        self.__click_counter = init_counter
    
    def disable(self):
        self.program_running = False
        self.__event_listener.stop()
        # if(display_label is not None): 
            # self.__display_remaining_counter_label = display_label

    def __key_press_event(self, key): 
        delay_range = np.linspace(start=0.001, stop=0.1, num=50)
        random_delay = random.choice(delay_range)

        if(key == KeyCode(char=self.__key) and self.program_running and ((self.__click_counter > 0) or (self.__click_counter == -1))):
            time.sleep(random_delay)
            self.__mouse.click(Button.left, 1)

            if(self.__click_counter < 0): 
                self.__display_remaining_counter_label.config(text=f'Clicks remaining: Infinit')
            else: 
                self.__click_counter -= 1
                self.__display_remaining_counter_label.config(text=f'Clicks remaining: {self.__click_counter}')
        return self.program_running


if(__name__ == '__main__'): 

    auto_clicker = AutoClicker()

    root = tk.Tk()
    root.title("Amy's auto-clicker")
    # root.geometry('500x200')


    # =======================================================  GUI frame
    gui_frame = ttk.Frame(root, padding=(30,30))
    gui_frame.pack(side='top', fill='both', expand=True)

    instructions = ttk.Label(gui_frame, text='To get program to auto-click, hold your key down.')
    instructions.pack(ipadx=5, ipady=20)

    instructions.config(font=("Verdana", 20))


    # =======================================================  key input frame
    def showOnlyOneKey(string: tk.StringVar): 
        text_val = string.get()
        string.set(text_val[-1:])
        key = string.get()
        global auto_clicker
        if(key != ''): 
            auto_clicker.setKey(string.get())
    
    text_input_frame = ttk.Frame(gui_frame)
    text_input_frame.pack(fill='both')

    auto_click_key = tk.StringVar(value='s')
    auto_click_key.trace("w", lambda name, index, mode, sv=auto_click_key: showOnlyOneKey(sv))

    input_label = ttk.Label(text_input_frame, text='Hold key for cursor to auto click:')
    input_label.pack(side='left', fill='x', ipadx=5)

    input_key = ttk.Entry(text_input_frame, width=2, textvariable=auto_click_key)
    input_key.pack(side='left', fill='x')


    # =======================================================  click counter frame
    click_counter_display_frame = ttk.Frame(gui_frame)
    # click_counter_display_frame.pack(fill='both')
    remaining_clicks_label = ttk.Label(click_counter_display_frame, text='Clicks remaining: Infinit')

    # =======================================================  max click input frame
    def intOnly(string: tk.StringVar): 
        global remaining_clicks_label
        global auto_clicker
        value = ''
        for char in string.get(): 
            if(char in '1234567890'): 
                value += char
        if(not auto_clicker.program_running): 
            remaining_clicks_label.config(text=f'Clicks remaining: {value}')
        string.set(str(int(value)))

    counter_input_frame = ttk.Frame(gui_frame)
    counter_input_frame.pack(fill='both')

    max_click_counter = tk.StringVar(value='0')
    max_click_counter.trace("w", lambda name, index, mode, sv=max_click_counter: intOnly(sv))

    counter_label = ttk.Label(counter_input_frame, text='Max Clicks ( 0 = infinit ):')
    counter_label.pack(side='left', ipadx=5)

    input_counter = ttk.Entry(counter_input_frame, width=10, textvariable=max_click_counter)
    input_counter.pack(side='left')
    

    


    # =======================================================  buttons

    # show remaining clicks just above buttons
    click_counter_display_frame.pack(fill='both')
    remaining_clicks_label.pack(side='left', ipadx=5, pady=(10, 10))
    remaining_clicks_label.config(font=("Verdana", 18))



    def enable_auto_click(btn: ttk.Button): 
        global auto_click_key
        global auto_clicker
        enable_key = auto_click_key.get()
        print(btn)
        if((len(enable_key) > 0) and not auto_clicker.program_running): 
            auto_clicker.enable(max_click_counter.get(), remaining_clicks_label)
            btn.configure(text='Program Started. Just change the key above, if needed', state='disabled')
    
    def reset_click_counter(btn: ttk.Button): 
        global auto_clicker
        auto_clicker.reset_counter(max_click_counter.get())
        remaining_clicks_label.config(text=f'Clicks remaining: {max_click_counter.get()}')

    def disable_auto_click(enable_btn: ttk.Button): 
        global auto_clicker
        global auto_click_key
        if(auto_clicker.program_running):
            auto_clicker.disable()
            enable_btn.configure(text='Enable Auto Clicking', state='selected')
            remaining_clicks_label.config(text=f'Clicks remaining: {max_click_counter.get()}')


    enable_btn = ttk.Button(gui_frame,
        text='Enable Auto Clicking',
        command=lambda: enable_auto_click(enable_btn),
    )
    enable_btn.pack(pady=(20, 0))

    reset_btn = ttk.Button(gui_frame,
        text='Reset Counter',
        command=lambda: reset_click_counter(reset_btn),
    )
    reset_btn.pack()

    disable_btn = ttk.Button(gui_frame,
        text='Disable Auto Clicking',
        command=lambda: disable_auto_click(enable_btn)
    )
    disable_btn.pack()

    ttk.Button(gui_frame, text='Exit', command=root.destroy).pack()

    root.mainloop()