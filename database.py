from __future__ import annotations
import random

def format(size: int) -> str:
    if size < 0:
        return "?"

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
                "completed": False,
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
                ref[self.hash]["completed"] = False
                ref[self.hash]["paused"] = folder_path
        else:
            ref[self.hash] = {
                "completed": False,
                "paused": folder_path,
                "size": 0
            }

    def set_completed(self, folder_dir: list[str]):
        ref = self.data
        
        for folder_name in folder_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
        
        if self.hash in ref:
            ref[self.hash]["completed"] = True
            ref[self.hash]["paused"] = None
        else:
            ref[self.hash] = {
                "completed": True,
                "paused": None,
                "size": 0
            }

    def update_completed(self, folder_dir: list[str]):
        ref = self.data

        for folder_name in folder_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]

        ref[self.hash]["completed"] = True
        for key, value in ref.items():
            if type(ref[key]) is dict:
                if self.hash in ref[key]:
                    if ref[key][self.hash]["completed"] == False:
                        ref[self.hash]["completed"] = False
                        return
                else:
                    ref[key][self.hash] = {
                        "completed": False,
                        "pause": None,
                        "size": 0
                    }
                    ref[self.hash]["completed"] = False
                    return

    def read_clearance(self, folder_dir: list[str]) -> tuple[True, None] | tuple[False, str]:
        ref = self.data

        for folder_name in folder_dir:
            if folder_name not in ref:
                ref[folder_name] = {}
            ref = ref[folder_name]
    
        if self.hash in ref:
            if ref[self.hash]["completed"]:
                return (True, None)
            return (False, ref[self.hash]["paused"])
        else:
            return (True, None)
    
    def get_entity_size(self, entity_path: str) -> str:
        entity_dir = entity_path.split("/")
        ref = self.data

        for entity_name in entity_dir:
            if entity_name not in ref:
                return format(-1)
            ref = ref[entity_name]

        if type(ref) is int:
            return format(ref)
        
        if type(ref) is dict:
            if self.hash not in ref:
                ref[self.hash] = {
                    "completed": False,
                    "pause": None,
                    "size": 0
                }
            return format(ref[self.hash]["size"])
        
        return "?"
        