from pynput import keyboard
from calculator import Calculator
from database import Database
from selector import Selector
import sys
import os

try:
    origin_path = sys.argv[1]
except:
    origin_path = os.getcwd().replace("\\", "/")

database = Database()
selector = Selector(origin_path, database)
calculator = Calculator(origin_path, database)

def callback():
    global calculator
    del calculator
    calculator = Calculator(origin_path, database)

def on_press(key):
    global origin_path
    global selector
    if key == keyboard.Key.esc:
        return False
    
    try:
        k = key.char
    except:
        k = key.name
    
    if k == "up":
        selector.up_select()

    if k == "down":
        selector.down_select()
    
    if k == "enter":
        entity_name = selector.get_selected()

        if entity_name is None:
            if origin_path.endswith(":"):
                return
            entity_dir = origin_path.split("/")
            entity_dir.pop()
            new_path = "/".join(entity_dir)

            selector.cancelled = True
            listener.stop()
            os.execl(sys.executable, "python", __file__, new_path)
        else:
            new_path = f'{origin_path}/{entity_name}'
            if os.path.isfile(new_path):
                return

            selector.cancelled = True
            listener.stop()
            os.execl(sys.executable, "python", __file__, new_path)

try:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
except:
    print("Stopped listening to keypress")