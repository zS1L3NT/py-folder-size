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
        self.hash = "__.metadata__" + str(random.getrandbits(100))
        self.data = {}
    
    def get_ref(self, dir: list[str]):
        ref = self.data

        for entity in dir:
            if entity not in ref:
                ref[entity] = {}
            ref = ref[entity]
        return ref
    
    def get_metadata__ref(self, ref) -> dict:
        if self.hash not in ref:
            ref[self.hash] = {
                "completed": False,
                "size": 0
            }
        return ref[self.hash]

    def get_metadata__dir(self, dir: list[str]) -> dict:
        return self.get_metadata__ref(self.get_ref(dir))

    def add_folder_size(self, folder_dir: list[str], size: int):
        metadata = self.get_metadata__dir(folder_dir)
        metadata["size"] += size

    def set_completed(self, folder_dir: list[str]):
        metadata = self.get_metadata__dir(folder_dir)
        metadata["completed"] = True

    def update_completed(self, folder_dir: list[str]):
        ref = self.get_ref(folder_dir)
        metadata = self.get_metadata__ref(ref)

        metadata["completed"] = True
        for key, value in ref.items():
            if type(value) is dict and key != self.hash:
                metadata_ = self.get_metadata__ref(value)
                if metadata_["completed"] == False:
                    metadata["completed"] = False
                    return
    
    def get_entity_size(self, entity_path: str) -> str:
        ref = self.get_ref(entity_path.split("/"))

        if type(ref) is int:
            return format(ref)
        
        if type(ref) is dict:
            metadata = self.get_metadata__ref(ref)
            return format(metadata["size"])
    
    def wipe(self):
        self.data = {}
        return self