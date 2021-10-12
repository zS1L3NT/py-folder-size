from formatter import format
from tabulate import tabulate
import os

class selector():
    def __init__(self, options: list[str]):
        self.options = options
        self.sizes = [0 for _ in options]
        self.selection = 0

        self.refresh()
        
    def refresh(self):
        os.system("cls")
        table = [['( )', 'Filename', 'Size']]
        table.append([
            f'({"*" if self.selection == 0 else " "})',
            'Pause/Resume Calculations',
            '-'
        ])
        for i, option in enumerate(self.options):
            table.append([
                f'({"*" if self.selection == (i + 1) else " "})',
                option,
                format(self.sizes[i])
            ])
        print(tabulate(table, headers='firstrow', tablefmt='grid'))

    def update_sizes(self, sizes: list[int]):
        self.sizes = sizes

        self.refresh()

    def up_select(self):
        if self.selection != 0:
            self.selection -= 1
            self.refresh()
    
    def down_select(self):
        if self.selection != len(self.options):
            self.selection += 1
            self.refresh()