# Folder Sizes

![License](https://img.shields.io/github/license/zS1L3NT/py-folder-sizes?style=for-the-badge) ![Languages](https://img.shields.io/github/languages/count/zS1L3NT/py-folder-sizes?style=for-the-badge) ![Top Language](https://img.shields.io/github/languages/top/zS1L3NT/py-folder-sizes?style=for-the-badge) ![Commit Activity](https://img.shields.io/github/commit-activity/y/zS1L3NT/py-folder-sizes?style=for-the-badge) ![Last commit](https://img.shields.io/github/last-commit/zS1L3NT/py-folder-sizes?style=for-the-badge)

Script to recursively calculate the total size of a folder. Only tested in Windows OS. Made a simple console GUI with pagination to navigate the current working directory you are in. Use space key to view contents of a sub-folder.
![GUI](https://i.ibb.co/3ztbqNQ/sizes.png)

## Motivation

Windows File Explorer is annoying. I want to see the size of each folder in a directory but it just won't show. I have to click into each folder individually to see it's size. Using this script, I can calculate the size of each folder and display it for myself to see.

## Features

-   Calculates the size of folders recursively, with a dedicated for each folder displayed
-   Status of whether the thread is still reading files or has finished reading a folder
-   Special selection menu
    -   Selected item shows `(*)`
    -   Non-selected item shows `( )`
-   Press spacebar to enter a folder

## Usage

Install the two dependencies for this project like this

```
$ pip install ./requirements.txt
```

Run the script with python in the folder you would like to scan.

```
$ python main.py
```

If you pass an arguement for the folder directory as the first arguement of the script, it will scan that directory instead

```
$ python main.py "C:/Users"
```

## Built with

-   Python
    -   [![tabulate](https://img.shields.io/badge/tabulate-0.8.9-blue?style=flat-square)](https://pypi.org/project/tabulate/0.8.9)
    -   [![pynput](https://img.shields.io/badge/pynput-1.7.3-blue?style=flat-square)](https://pypi.org/project/pynput/1.7.3)
