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
        terminal_size = (0, 0)
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
            if metadata["completed"]:
                if complete and terminal_size == (os.get_terminal_size().lines, os.get_terminal_size().columns):
                    continue
                complete = True
            
            self.refresh()
            terminal_size = (os.get_terminal_size().lines, os.get_terminal_size().columns)
        
    def refresh(self):
        os.system("cls")
        table = [['( )', 'Name', 'Type', 'Size', 'Reading']]
        table.append([
            f'({"*" if self.selection == 0 else " "})',
            '^^ Parent Directory ' + (os.get_terminal_size().columns - 65) * ".",
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
                Status = "✅\u200B" if entity_name in ref else "⌛\u200B"
            if os.path.isdir(entity_path):
                entity_dir = entity_path.split("/")
                Status = "✅\u200B" if self.database.get_metadata__dir(entity_dir)["completed"] else "⌛\u200B"

            Size = self.database.get_entity_size(entity_path)

            table.append([ Checkbox, entity_name, Type, Size, Status ])

        print(tabulate(table, headers='firstrow', tablefmt='grid'))
    
    def paginate_entity_names(self) -> list[tuple[int, str]]:
        empty_entity = [(-1, "...")]
        selected_i = self.selection - 1
        entity_names = list(enumerate(self.entity_names))
        entity_count = len(entity_names)

        # maximum number of entities that can be shown on the screen
        # make the number odd
        max_entity_count = max(5, (os.get_terminal_size().lines - 8) // 2)
        max_entity_count = (max_entity_count + 1) if max_entity_count // 2 else max_entity_count
        half_max_entity_count = max_entity_count // 2

        if entity_count <= max_entity_count:
            return entity_names
        
        if selected_i <= half_max_entity_count:
            return entity_names[:max_entity_count - 1] + empty_entity
        
        if selected_i >= entity_count - half_max_entity_count - 1:
            return empty_entity + entity_names[entity_count - max_entity_count + 1:]

        return empty_entity + entity_names[selected_i - half_max_entity_count + 1:selected_i + half_max_entity_count] + empty_entity
    
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