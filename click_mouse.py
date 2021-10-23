import time
import random
import threading
import numpy as np
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

class AutoClicker(threading.Thread): 

    __mouse: Controller
    key: str

    def __init__(self, key: str = 's'): 
        super().__init__()
        self.__mouse = Controller()
        self.key = key

        with Listener(on_press=self.__key_press_event) as key_press:
                key_press.join()


    def __key_press_event(self, key): 
        delay_range = np.linspace(start=0.001, stop=0.1, num=50)
        random_delay = random.choice(delay_range)

        if(key == KeyCode(char=self.key)):
            time.sleep(random_delay)
            self.__mouse.click(Button.left, 1)
    
    


c = AutoClicker()
c.start()