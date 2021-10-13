from threading import Thread
from tabulate import tabulate
from database import Database
from time import sleep
import os


class Selector():
    def __init__(self, curr_folder_path: str, database: Database):
        self.curr_folder_path = curr_folder_path
        self.entity_names = os.listdir(self.curr_folder_path)
        self.database = database
        self.selection = 0

        thread = Thread(target=self.start)
        thread.start()
    
    def start(self):
        while True:
            sleep(1)
            self.refresh()
        
    def refresh(self):
        os.system("cls")
        table = [['( )', 'Name', 'Type', 'Size']]
        table.append([
            f'({"*" if self.selection == 0 else " "})',
            '^^ Parent Directory',
            'Folder',
            '-'
        ])
        for i, entity_name in enumerate(self.entity_names):
            entity_path = f'{self.curr_folder_path}/{entity_name}'
            table.append([
                f'({"*" if self.selection == (i + 1) else " "})',
                entity_name,
                'File' if os.path.isfile(entity_path) else 'Folder',
                self.database.get_entity_size(entity_path)
            ])
        print(tabulate(table, headers='firstrow', tablefmt='grid'))
    
    def change_folder(self, curr_folder_path: str):
        self.curr_folder_path = curr_folder_path
        self.entity_names = os.listdir(self.curr_folder_path)
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