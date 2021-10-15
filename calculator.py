from threading import Thread
from database import Database
import os

# path: "C:/Codes/py-folder-size/calculator.py"
# dir : ["C:", "Codes", "py-folder-size", "calculator.py"]
# name: "calculator.py"

class Calculator():
    def __init__(self, origin_path: str, database: Database):
        self.origin_path = origin_path
        self.database = database
        self.folders_done: list[bool] = []

        self.callback = None
        self.cancelled = False
        self.callback_ran = False

        threads: list[FolderThread] = []

        for entity_name in os.listdir(self.origin_path):
            entity_path = f'{self.origin_path}/{entity_name}'
            if os.path.isdir(entity_path):
                i = len(self.folders_done)
                self.folders_done.append(False)
                threads.append(FolderThread(self, entity_path, i))

            if os.path.isfile(entity_path):
                self.add_file_size(entity_path, os.path.getsize(entity_path))

        for thread in threads: thread.start()

    def on_threads_done(self):
        self.database.update_completed(self.origin_path.split("/"))

        if self.callback is not None:
            self.callback_ran = True
            self.callback()

    def set_callback(self, callback):
        self.callback = callback
        if all(self.folders_done) and not self.callback_ran and self.callback is not None:
            self.callback_ran = True
            self.callback()

    def add_file_size(self, file_path: str, size: int) -> None:
        file_dir = file_path.split('/')
        file_name = file_dir.pop()
        ref = self.database.get_ref(file_dir)

        if file_name in ref:
            return
        
        ref[file_name] = size
        self.database.add_folder_size(file_dir, size)
        
        if "/".join(file_path.split("/")[:-1]) == self.origin_path:
            return
    
        origin_dir = self.origin_path.split("/")
        self.database.add_folder_size(origin_dir, size)

    def add_folder_size(self, folder_path: str, size: int):
        folder_dir = folder_path.split('/')
        self.database.add_folder_size(folder_dir, size)

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

    def start(self):
        thread = Thread(target=self.read_folder_size, args=(self.folder_path,))
        thread.start()

    def read_folder_size(self, folder_path: str) -> int:
        folder_size = 0

        if folder_path == "C:/Codes/wss":
            print()
            pass

        (allowed, paused_path) = self.parent.database.read_clearance(folder_path.split("/"))
        
        for entity_name in os.listdir(folder_path):
            entity_path = f'{folder_path}/{entity_name}'

            if not allowed:
                if entity_path == paused_path:
                    allowed = True
                else:
                    continue

            if self.parent.cancelled:
                self.parent.set_pause_position(entity_path)
                if self.folder_path == folder_path:
                    self.callback()
                return 0

            if os.path.isdir(entity_path):
                size = self.read_folder_size(entity_path)
                folder_size += size
                self.parent.add_folder_size(folder_path, size)

            if os.path.isfile(entity_path):
                size = os.path.getsize(entity_path)
                folder_size += size
                self.parent.add_file_size(entity_path, size)
        
        self.parent.database.set_completed(folder_path.split("/"))
        if self.folder_path != folder_path:
            return folder_size
        self.callback()

    def callback(self):
        if self.callback_ran: return
        self.callback_ran = True

        self.parent.folders_done[self.i] = True
        if all(self.parent.folders_done):
            self.parent.on_threads_done()