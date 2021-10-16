import json
from datetime import datetime
from pynput import keyboard
from calculator import Calculator
from database import Database
from selector import Selector
import os

curr_folder_path = "/".join(os.getcwd().split("\\")[:-1])
database = Database()
selector = Selector(curr_folder_path, database)
calculator = Calculator(curr_folder_path, database)

def callback():
    global calculator
    del calculator
    calculator = Calculator(curr_folder_path, database)

def on_press(key):
    global curr_folder_path
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
    
    if k == "p":
        with open(f"{round(datetime.now().timestamp())}.json", "w") as f:
            json.dump(database.get_ref(curr_folder_path.split("/")), f)
    
    if k == "enter":
        entity_name = selector.get_selected()
        if entity_name is None:
            curr_folder_dir = curr_folder_path.split("/")
            curr_folder_dir.pop()
            curr_folder_path = "/".join(curr_folder_dir)

            selector.change_folder(curr_folder_path)
            calculator.set_callback(callback)
            calculator.cancelled = True
            return

        entity_path = f'{curr_folder_path}/{entity_name}'
        if os.path.isfile(entity_path): return
        
        curr_folder_path = entity_path
        selector.change_folder(curr_folder_path)
        calculator.set_callback(callback)
        calculator.cancelled = True

try:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
except:
    print("Stopped listening to keypress")