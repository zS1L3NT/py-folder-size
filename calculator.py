from __future__ import annotations
from threading import Thread
from pprint import pprint
from time import sleep
import random
import json
import os

# path: "C:/Codes/py-folder-size/calculator.py"
# dir : ["C:", "Codes", "py-folder-size", "calculator.py"]
# name: "calculator.py"

class Database():
    def __init__(self):
        self.hash = str(random.getrandbits(100))
        self.data = {}
    
    def set_ref(self, file_dir: list[str], size: int):
        file_name = file_dir.pop()
        ref = self.data
        
        for folder_name in file_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
        ref[file_name] = size

    def add_size(self, folder_dir: list[str], size: int):
        ref = self.data
        
        for folder_name in folder_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]

        if self.hash in ref:
            ref[self.hash]["size"] += size
        else:
            ref[self.hash] = {
                "complete": False,
                "paused": None,
                "size": size
            }
    
    def pause(self, parent_folder_dir: list[str], folder_path: str):
        ref = self.data

        for parent_folder_name in parent_folder_dir:
            if parent_folder_name not in ref:
                ref[parent_folder_name] = {}
            ref = ref[parent_folder_name]
        
        if self.hash in ref:
            if ref[self.hash]["paused"] is None:
                ref[self.hash]["paused"] = folder_path
        else:
            ref[self.hash] = {
                "complete": False,
                "paused": folder_path,
                "size": 0
            }

    def update_status(self, folder_dir: list[str]):
        ref = self.data

        for folder_name in folder_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]

        ref[self.hash]["complete"] = True
        for key, value in ref.items():
            if type(ref[key]) is dict:
                if ref[key][self.hash]["complete"] == False:
                    ref[self.hash]["complete"] = False
                    return

class Calculator():
    def __init__(self, origin_path: str, database: Database):
        self.origin_path = origin_path
        self.database = database
        self.folders_done = []
        self.cancelled = False
        self.callback = None

        for entity_name in os.listdir(self.origin_path):
            entity_path = f'{self.origin_path}/{entity_name}'
            if os.path.isdir(entity_path):
                i = len(self.folders_done)
                self.folders_done.append(False)
                FolderThread(self, entity_path, i)

            if os.path.isfile(entity_path):
                self.set_file_size(entity_path, os.path.getsize(entity_path))

    def threads_done(self):
        self.database.update_status(self.origin_path.split("/"))

        if self.callback is not None:
            self.callback()

    def set_file_size(self, file_path: str, size: int) -> None:
        file_dir = file_path.split('/')

        self.database.set_ref(file_dir, size)
        file_dir.pop()
        self.database.add_size(file_dir, size)
        
        if "/".join(file_path.split("/")[:-1]) == self.origin_path:
            return
    
        origin_dir = self.origin_path.split("/")
        self.database.add_size(origin_dir, size)

    def set_folder_size(self, folder_path: str, size: int):
        folder_dir = folder_path.split('/')
        self.database.add_size(folder_dir, size)

    def set_pause_position(self, folder_path: str):
        folder_dir = folder_path.split('/')
        folder_dir.pop()

        self.database.pause(folder_dir, folder_path)

class FolderThread():
    def __init__(self, parent: Calculator, folder_path: str, i: int):
        self.parent = parent
        self.folder_path = folder_path
        self.i = i
        self.callback_ran = False

        thread = Thread(target=self.read_folder, args=(folder_path,))
        thread.start()

    def read_folder(self, folder_path: str) -> int:
        folder_size = 0
        
        for entity_name in os.listdir(folder_path):
            entity_path = f'{folder_path}/{entity_name}'
            entity_size = 0

            if self.parent.cancelled:
                self.parent.set_pause_position(entity_path)
                self.callback()
                return 0

            if os.path.isdir(entity_path):
                entity_size = self.read_folder(entity_path)

            if os.path.isfile(entity_path):
                entity_size = os.path.getsize(entity_path)
                self.parent.set_file_size(entity_path, entity_size)
            
            folder_size += entity_size
        
        self.parent.set_folder_size(folder_path, folder_size)
        if self.folder_path != folder_path:
            return folder_size
        
        self.callback()
        
    def callback(self):
        if self.callback_ran:
            return

        self.parent.folders_done[self.i] = True
        if all(self.parent.folders_done):
            self.parent.threads_done()


database = Database()
calculator = Calculator(os.getcwd().replace("\\", "/").replace("/py-folder-size", ""), database)

def callback():
    with open("data.json", "w") as outfile:
        json.dump(calculator.database.data, outfile)
calculator.callback = callback

sleep(1)
calculator.cancelled = True