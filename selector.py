from threading import Thread
from tabulate import tabulate
from database import Database
from time import sleep
import os


class Selector():
    def __init__(self, origin_path: str, database: Database):
        self.origin_path = origin_path
        if self.origin_path.endswith(":"):
            self.origin_path += "/"

        self.entity_names = self.get_sorted_entity_names()
        self.database = database
        self.selection = 0
        self.cancelled = False

        thread = Thread(target=self.start)
        thread.start()
    
    def start(self):
        complete = False
        origin_path = self.origin_path

        sleep(1)
        self.refresh()

        while True:
            if self.cancelled:
                break
            sleep(1)

            if origin_path != self.origin_path:
                origin_path = self.origin_path
                complete = False
                self.refresh()
            
            metadata = self.database.get_metadata__dir(origin_path.split("/"))
            if metadata["completed"] == True:
                if complete:
                    continue
                complete = True
            
            self.refresh()
        
    def refresh(self):
        os.system("cls")
        table = [['( )', 'Name', 'Type', 'Size', 'Reading']]
        table.append([
            f'({"*" if self.selection == 0 else " "})',
            '^^ Parent Directory',
            'Folder',
            '-',
            '-'
        ])

        for i, entity_name in self.paginate_entity_names():
            if entity_name == "...":
                table.append([ "...", "...", "...", "...", "..." ])
                continue

            entity_path = f'{self.origin_path}/{entity_name}'

            Checkbox = f'({"*" if self.selection == (i + 1) else " "})'

            Type = 'File' if os.path.isfile(entity_path) else 'Folder'

            Status = ""
            if os.path.isfile(entity_path):
                entity_dir = entity_path.split("/")
                entity_name = entity_dir.pop()
                ref = self.database.get_ref(entity_dir)
                Status = "✅\u200B\u200B" if entity_name in ref else "⌛\u200B"
            if os.path.isdir(entity_path):
                entity_dir = entity_path.split("/")
                Status = "✅\u200B\u200B" if self.database.get_metadata__dir(entity_dir)["completed"] else "⌛\u200B"

            Size = self.database.get_entity_size(entity_path)

            table.append([ Checkbox, entity_name, Type, Size, Status ])

        print(tabulate(table, headers='firstrow', tablefmt='grid'))
    
    def paginate_entity_names(self):
        empty_entity = "..."
        selected = self.selection - 1
        entity_count = len(self.entity_names)

        if entity_count <= 9:
            return enumerate(self.entity_names)

        entity_names = [(0, "") for _ in range(9)]
        entity_names[0] = (0, self.entity_names[0])
        entity_names[8] = (entity_count - 1, self.entity_names[-1])
        
        if selected <= 3:
            entity_names[1] = (1 ,self.entity_names[1])
            entity_names[2] = (2 ,self.entity_names[2])
            entity_names[3] = (3 ,self.entity_names[3])
            entity_names[4] = (4 ,self.entity_names[4])
            entity_names[5] = (5 ,self.entity_names[5])
            entity_names[6] = (6 ,self.entity_names[6])
            entity_names[7] = (-1, empty_entity)
            return entity_names
        
        if entity_count - selected <= 4:
            entity_names[1] = (-1, empty_entity)
            entity_names[2] = (entity_count - 7, self.entity_names[-7])
            entity_names[3] = (entity_count - 6, self.entity_names[-6])
            entity_names[4] = (entity_count - 5, self.entity_names[-5])
            entity_names[5] = (entity_count - 4, self.entity_names[-4])
            entity_names[6] = (entity_count - 3, self.entity_names[-3])
            entity_names[7] = (entity_count - 2, self.entity_names[-2])
            return entity_names
        
        entity_names[1] = (-1, empty_entity)
        entity_names[2] = (selected - 2, self.entity_names[selected - 2])
        entity_names[3] = (selected - 1, self.entity_names[selected - 1])
        entity_names[4] = (selected, self.entity_names[selected])
        entity_names[5] = (selected + 1, self.entity_names[selected + 1])
        entity_names[6] = (selected + 2, self.entity_names[selected + 2])
        entity_names[7] = (-1, empty_entity)
        return entity_names
    
    def get_sorted_entity_names(self):
        entity_names = os.listdir(self.origin_path)
        folders: list[str] = []
        files: list[str] = []

        for entity_name in entity_names:
            entity_path = f'{self.origin_path}/{entity_name}'

            if os.path.isfile(entity_path):
                files.append(entity_name)

            if os.path.isdir(entity_path):
                folders.append(entity_name)
        
        return folders + files
    
    def change_folder(self, curr_folder_path: str):
        self.origin_path = curr_folder_path
        self.entity_names = self.get_sorted_entity_names()
        self.selection = 0

    def up_select(self):
        if self.selection != 0:
            self.selection -= 1
            self.refresh()
    
    def down_select(self):
        if self.selection != len(self.entity_names):
            self.selection += 1
            self.refresh()
    
    def get_selected(self):
        if self.selection == 0:
            return None
        return self.entity_names[self.selection - 1]