from threading import Thread
from database import Database
import os

# path: "C:/Codes/py-folder-size/calculator.py"
# dir : ["C:", "Codes", "py-folder-size", "calculator.py"]
# name: "calculator.py"

class Calculator():
    def __init__(self, origin_path: str, database: Database):
        self.origin_path = origin_path
        if self.origin_path.endswith(":"):
            self.origin_path += "/"

        self.database = database
        self.folders_done: list[bool] = []

        threads: list[FolderThread] = []

        try:
            entity_names = sorted(os.listdir(self.origin_path))
        except:
            entity_names = []

        for entity_name in entity_names:
            entity_path = f'{self.origin_path}/{entity_name}'

            if os.path.isdir(entity_path):
                i = len(self.folders_done)
                self.folders_done.append(False)
                threads.append(FolderThread(self, entity_path, i))

            if os.path.isfile(entity_path):
                self.add_file_size(entity_path, os.path.getsize(entity_path))

        for thread in threads:
            thread.start()

    def on_threads_done(self):
        self.database.update_completed(self.origin_path.split("/"))

    def add_file_size(self, file_path: str, size: int) -> None:
        file_dir = file_path.split('/')
        file_name = file_dir.pop()
        ref = self.database.get_ref(file_dir)

        if file_name in ref:
            return
        ref[file_name] = size

        ref_dir = []
        for folder_name in file_dir:
            ref_dir.append(folder_name)
            self.database.add_folder_size(ref_dir, size)

    def add_folder_size(self, folder_path: str, size: int):
        folder_dir = folder_path.split('/')
        self.database.add_folder_size(folder_dir, size)

class FolderThread():
    def __init__(self, parent: Calculator, folder_path: str, i: int):
        self.parent = parent
        self.folder_path = folder_path
        self.i = i
        self.callback_ran = False

    def start(self):
        thread = Thread(target=self.read_folder, args=(self.folder_path,))
        thread.start()

    def read_folder(self, folder_path: str):
        try:
            entity_names = sorted(os.listdir(folder_path))
        except:
            entity_names = []

        for entity_name in entity_names:
            entity_path = f'{folder_path}/{entity_name}'

            if os.path.isdir(entity_path):
                self.read_folder(entity_path)

            if os.path.isfile(entity_path):
                self.parent.add_file_size(entity_path, os.path.getsize(entity_path))
        
        self.parent.database.set_completed(folder_path.split("/"))    
        if self.folder_path == folder_path:
            self.callback()

    def callback(self):
        if self.callback_ran: return
        self.callback_ran = True

        self.parent.folders_done[self.i] = True
        if all(self.parent.folders_done):
            self.parent.on_threads_done()