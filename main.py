from pynput.keyboard import Listener
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

def on_press(k):
    global origin_path
    global selector
    
    try:
        key = k.char
    except:
        key = k.name

    if key == "enter":
        exit()

    if key == "esc":
        return False
    
    if key == "up":
        selector.up_select()

    if key == "down":
        selector.down_select()
    
    if key == "space":
        entity_name = selector.get_selected()

        if entity_name is None:
            if origin_path.endswith(":"):
                return
            entity_dir = origin_path.split("/")
            entity_dir.pop()
            new_path = "/".join(entity_dir)

            selector.cancelled = True
            listener.stop()
            os.execl(sys.executable, "python", __file__, f'"{new_path}"')
        else:
            new_path = f'{origin_path}/{entity_name}'
            if os.path.isfile(new_path):
                return

            selector.cancelled = True
            listener.stop()
            os.execl(sys.executable, "python", __file__, f'"{new_path}"')

try:
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()
except:
    print("Stopped listening to keypress")