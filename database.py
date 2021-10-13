from __future__ import annotations
import random

def format(size: int) -> str:
    if size < 100:
        return str(size) + " B"

    if size < 1_000:
        return str(size) + " B"
    
    if size < 10_000:
        return str(round(size / 1_000, 3)) + " kB"

    if size < 100_000:
        return str(round(size / 1_000, 2)) + " kB"

    if size < 1_000_000:
        return str(round(size / 1_000, 1)) + " kB"
    
    if size < 10_000_000:
        return str(round(size / 1_000_000, 3)) + " MB"
    
    if size < 100_000_000:
        return str(round(size / 1_000_000, 2)) + " MB"
    
    if size < 1_000_000_000:
        return str(round(size / 1_000_000, 1)) + " MB"
    
    if size < 10_000_000_000:
        return str(round(size / 1_000_000_000, 3)) + " GB"
    
    if size < 100_000_000_000:
        return str(round(size / 1_000_000_000, 2)) + " GB"
    
    if size < 1_000_000_000_000:
        return str(round(size / 1_000_000_000, 1)) + " GB"
    
    if size < 10_000_000_000_000:
        return str(round(size / 1_000_000_000_000, 3)) + " TB"
    
    return "?"

class Database():
    def __init__(self):
        self.hash = "00000" + str(random.getrandbits(100))
        self.data = {}
    
    def get_ref(self, dir: list[str]):
        ref = self.data

        for entity in dir:
            if entity not in ref:
                ref[entity] = {}
            ref = ref[entity]
        return ref
    
    def get_metadata(self, ref) -> dict:
        if self.hash not in ref:
            ref[self.hash] = {
                "completed": False,
                "paused": None,
                "size": 0
            }
        return ref[self.hash]

    def get_dir_metadata(self, dir: list[str]) -> dict:
        return self.get_metadata(self.get_ref(dir))

    def set_ref(self, file_dir: list[str], size: int):
        file_name = file_dir.pop()
        self.get_ref(file_dir)[file_name] = size

    def add_size(self, folder_dir: list[str], size: int):
        metadata = self.get_dir_metadata(folder_dir)
        metadata["size"] += size
    
    def pause(self, parent_folder_dir: list[str], folder_path: str):
        metadata = self.get_dir_metadata(parent_folder_dir)
        
        if metadata["paused"] is None:
            metadata["completed"] = False
            metadata["paused"] = folder_path

    def set_completed(self, folder_dir: list[str]):
        metadata = self.get_dir_metadata(folder_dir)
        metadata["completed"] = True
        metadata["paused"] = None

    def update_completed(self, folder_dir: list[str]):
        ref = self.get_ref(folder_dir)
        metadata = self.get_metadata(ref)

        metadata["completed"] = True
        for value in ref.values():
            if type(value) is dict:
                metadata_ = self.get_metadata(value)
                if metadata_["completed"] == False:
                    metadata["completed"] = False
                    return

    def read_clearance(self, folder_dir: list[str]) -> tuple[True, None] | tuple[False, str]:
        ref = self.get_ref(folder_dir)
    
        if self.hash in ref:
            if ref[self.hash]["completed"]:
                return (True, None)
            return (False, ref[self.hash]["paused"])
        else:
            return (True, None)
    
    def get_entity_size(self, entity_path: str) -> str:
        ref = self.get_ref(entity_path.split("/"))

        if type(ref) is int:
            return format(ref)
        
        if type(ref) is dict:
            metadata = self.get_metadata(ref)
            return format(metadata["size"])
        
        print(entity_path)
        raise TypeError("What is that file type???")

    def is_complete(self, folder_path: str) -> bool:
        folder_dir = folder_path.split("/")
        ref = self.data

        for folder_name in folder_dir:
            if folder_name not in ref:
                return False
            ref = ref[folder_name]

        if self.hash not in ref:
            return False
        return ref[self.hash]["completed"]