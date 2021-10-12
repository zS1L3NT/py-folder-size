from pynput import keyboard
from Calculator import Calculator
from selector import selector
import os

selector = selector(os.listdir())
Calculator = Calculator(os.getcwd().replace("\\", "/").replace("/py-folder-size", ""))

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

try:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
except:
    print("Stopped listening to keypress")