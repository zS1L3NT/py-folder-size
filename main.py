from pynput import keyboard
from calculator import Calculator
from database import Database
from selector import Selector
import sys
import os

try:
    curr_folder_path = sys.argv[1]
except:
    curr_folder_path = os.getcwd().replace("\\", "/")

database = Database()
selector = Selector(curr_folder_path, database)
calculator = Calculator(curr_folder_path, database)

def callback():
    global calculator
    del calculator
    calculator = Calculator(curr_folder_path, database)

def on_press(key):
    global curr_folder_path
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
            entity_dir = curr_folder_path.split("/")
            entity_dir.pop()

            argv = []
            argv.append("python")
            argv.append(sys.argv[0])
            argv.append('/'.join(entity_dir))
            selector.cancelled = True
            os.system("cls")
            os.execv(sys.executable, argv)
        else:
            entity_path = f'{curr_folder_path}/{entity_name}'
            if os.path.isfile(entity_path):
                return

            argv = []
            argv.append("python")
            argv.append(sys.argv[0])
            argv.append(entity_path)
            selector.cancelled = True
            os.system("cls")
            os.execv(sys.executable, argv)

try:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
except:
    print("Stopped listening to keypress")