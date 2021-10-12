from __future__ import annotations
from threading import Thread
from pprint import pprint
from time import sleep
import random
import os


class Calculator():
    def __init__(self, origin_path: str):
        self.origin_path = origin_path
        self.size_hash = str(random.getrandbits(100))
        self.sizes = {}

        for entity_name in os.listdir(self.origin_path):
            entity_path = f'{self.origin_path}/{entity_name}'
            if os.path.isdir(entity_name):
                FolderReader(self, self.origin_path, entity_name)

            if os.path.isfile(entity_path):
                self.set_file_size(entity_path, os.path.getsize(entity_path))

    def set_file_size(self, file_path: str, size: int) -> None:
        file_dir = file_path.split('/')
        file_name = file_dir.pop()
        ref = self.sizes

        for folder_name in file_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
        if self.size_hash not in ref:
            ref[self.size_hash] = 0

        # Set the filesizes in the ref
        ref[file_name] = size
        ref[self.size_hash] += size
        
        if "/".join(file_path.split("/")[:-1]) == self.origin_path:
            return
            
        # Set the folder size
        # Do this every time we set a file size in the folder
        ref = self.sizes
        for folder_name in self.origin_path.split("/"):
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
        if self.size_hash not in ref:
            ref[self.size_hash] = 0
        ref[self.size_hash] += size

    def set_folder_size(self, folder_path: str, size: int):
        folder_dir = folder_path.split('/')
        ref = self.sizes

        for folder_name in folder_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
        
        ref[self.size_hash] = size

    def get_file_size(self, file_dir: list[str]) -> int | None:
        file_name = file_dir.pop()
        ref = self.sizes

        for folder_name in file_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
        
        if file_name not in ref:
            return None
        return ref[file_name]

class FolderReader():
    def __init__(self, parent: Calculator, origin_path: str, folder_name: str):
        self.parent = parent
        self.origin_path = origin_path
        self.folder_name = folder_name

        thread = Thread(target=self.read_folder, args=(f'{origin_path}/{folder_name}',))
        thread.start()
        thread.join()

    def read_folder(self, folder_path: str) -> int:
        folder_size = 0

        if self.parent.origin_path == self.origin_path:
            for entity_name in os.listdir(folder_path):
                entity_path = f'{folder_path}/{entity_name}'
                entity_size = 0

                if os.path.isdir(entity_path):
                    entity_size = self.read_folder(entity_path)

                if os.path.isfile(entity_path):
                    entity_size = os.path.getsize(entity_path)
                    self.parent.set_file_size(entity_path, entity_size)
                
                folder_size += entity_size
        
        self.parent.set_folder_size(folder_path, folder_size)
        return folder_size

        
Calculator = Calculator(os.getcwd().replace("\\", "/"))

def run():
    pprint(Calculator.sizes, indent=4, sort_dicts=True)


thread = Thread(target=run)
thread.start()
thread.join()
