from __future__ import annotations
from threading import Thread
from pprint import pprint
from time import sleep
import random
import os


class Calculator():
    def __init__(self, origin: str):
        self.origin = origin
        self.size_hash = str(random.getrandbits(100))
        self.sizes = {}

        for entity in os.listdir(self.origin):
            path = f'{self.origin}/{entity}'
            if os.path.isdir(entity):
                FolderReader(self, self.origin, entity)

            if os.path.isfile(path):
                self.set_file_size(path, os.path.getsize(entity))

    def set_file_size(self, path: str, size: int) -> None:
        dir = path.split('/')
        filename = dir.pop()
        ref = self.sizes

        for folder in dir:
            if folder not in ref:
                ref[folder] = {}
            ref = ref[folder]
        if self.size_hash not in ref:
            ref[self.size_hash] = 0

        # Set the filesizes in the ref
        ref[filename] = size
        ref[self.size_hash] += size
        
        if "/".join(path.split("/")[:-1]) == self.origin:
            return
            
        # Set the folder size
        # Do this every time we set a file size in the folder
        ref = self.sizes
        for folder in self.origin.split("/"):
            if folder not in ref:
                ref[folder] = {}
            ref = ref[folder]
        ref[self.size_hash] += size

    def set_folder_size(self, path: str, size: int):
        dir = path.split('/')
        ref = self.sizes

        for folder in dir:
            if folder not in ref:
                ref[folder] = {}
            ref = ref[folder]
        
        ref[self.size_hash] = size

    def get_file_size(self, dir: list[str]) -> int | None:
        filename = dir.pop()
        ref = self.sizes

        for folder in dir:
            if folder not in ref:
                ref[folder] = {}
            ref = ref[folder]
        
        if filename not in ref:
            return None
        return ref[filename]

class FolderReader():
    def __init__(self, parent: Calculator, origin: str, folder: str):
        self.parent = parent
        self.origin = origin
        self.folder = folder

        thread = Thread(target=self.read_folder, args=(f'{origin}/{folder}',))
        thread.start()
        thread.join()

    def read_folder(self, path: str) -> int:
        folder_size = 0

        if self.parent.origin == self.origin:
            for entity in os.listdir(path):
                entity = f'{path}/{entity}'
                entity_size = 0

                if os.path.isdir(entity):
                    entity_size = self.read_folder(entity)

                if os.path.isfile(entity):
                    entity_size = os.path.getsize(entity)
                    self.parent.set_file_size(entity, entity_size)
                
                folder_size += entity_size
        
        self.parent.set_folder_size(path, folder_size)
        return folder_size

        
Calculator = Calculator(os.getcwd().replace("\\", "/"))

def run():
    pprint(Calculator.sizes, indent=4, sort_dicts=True)


thread = Thread(target=run)
thread.start()
thread.join()
