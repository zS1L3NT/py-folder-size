# py-folder-sizes
Script to recursively calculate the total size of a folder. Only tested in Windows OS. Made a simple console GUI with pagination to navigate the current working directory you are in. Use space key to view contents of a sub-folder.
![GUI](https://i.ibb.co/3ztbqNQ/sizes.png)
## Installation
Install the two dependencies for this project like this
```bash
pip install ./requirements.txt
```
## Usage
Run the script with python in the folder you would like to scan.
```bash
python main.py
```
If you pass an arguement for the folder directory as the first arguement of the script, it will scan that directory instead
```bash
python main.py "C:/Users"
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
