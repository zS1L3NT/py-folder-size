from pynput import keyboard
from calculator import Calculator
from database import Database
from selector import Selector
import os

curr_folder_path = os.getcwd().replace("\\", "/")
database = Database()
selector = Selector(curr_folder_path, database)
calculator = Calculator(curr_folder_path, database)

def callback():
    global calculator
    calculator = Calculator(curr_folder_path, database)

def on_press(key):
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
        global curr_folder_path
        entity_name = selector.get_selected()
        if entity_name is None:
            curr_folder_dir = curr_folder_path.split("/")
            curr_folder_dir.pop()
            curr_folder_path = "/".join(curr_folder_dir)

            selector.change_folder(curr_folder_path)
            calculator.cancel(callback)
            return

        entity_path = f'{curr_folder_path}/{entity_name}'
        if os.path.isfile(entity_path): return
        
        curr_folder_path = entity_path
        selector.change_folder(curr_folder_path)
        calculator.cancel(callback)

try:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
except:
    print("Stopped listening to keypress")