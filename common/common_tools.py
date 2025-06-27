#%%
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import os
import pandas as pd
import tkinter.simpledialog as sd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
import yaml
import json


root = tk.Tk()
root.withdraw()


def select_excel_file():
    """Prompt the user to select an Excel file and return its path."""
    file_path = fd.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls;*.xlsm")])

    if not file_path:
        mb.showerror('Error', 'No file selected.')
        return None
    return file_path    


def select_sheet(xls):
    """Prompt the user to select a sheet from the Excel file."""
    sheet_names = xls.sheet_names
    while True:   # loop to allow retrying
        sheet_name = sd.askstring('Select Sheet', f'Available Sheets:\n{sheet_names}\n\nEnter the sheet name that you want to analyze:')
        if sheet_name in sheet_names:
            return sheet_name
    
        retry = mb.askretrycancel('Error', 'Invalid sheet name. Do you want to try again?')
        if not retry:
            return None
            

def process_excel_file(allow_sheet_selection: bool=True, sheet_name: str=None) -> Dict[str, str]:
    """This function is a wrapper for the select_excel_file and select_sheet functions.
    It prompts the user to select an Excel file and, if allowed, a sheet within that file.
    min function to handle Excel file selection and processing."""    
    file_path = select_excel_file()
    if not file_path:
        return [None, None, None, None]
    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        mb.showerror('Error', f'Failed to open the Excel file: {e}')
        return [None, None, None, None]
    
    # based on the given file_path, store the directory_path and filename in variables
    directory = os.path.dirname(file_path)
    xlsx_file_path = os.path.basename(file_path)
    file_name = os.path.splitext(xlsx_file_path)[0] # get the file name without extention

    # Optional sheet selection
    if allow_sheet_selection and not sheet_name:
        sheet_name = select_sheet(xls)
        if not sheet_name:
            return [None, None, None, None]
    elif sheet_name and sheet_name not in xls.sheet_names:
        mb.showerror('Error', f'Sheet "{sheet_name}" not found in the Excel file.')
        return [None, None, None, None]
        
    return {'file_path': file_path, 
            'directory': directory, 
            'file_name': file_name, 
            'sheet_name': sheet_name}



def savefig_and_show(file_info: dict, show_message: bool = True):
    png_file_name = os.path.join(file_info['directory'], f'{file_info["file_name"]}_{file_info["sheet_name"]}.png')
    plt.savefig(png_file_name, transparent=True, dpi = 200)
    if show_message:
        mb.showinfo('message', f'Program executed.\n\n The image file "{os.path.basename(png_file_name)}" has been saved in the folder where the Excel file is located.')
        os.startfile(png_file_name)     # show the figure by os default photo viewer


def load_config(file_path: str) -> Dict[str, str]:
    """Load configuration from a YAML or JSON file."""
    with open(file_path, 'r', encoding = 'utf-8') as file:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(file)
        elif filep_path.endswith('.json'):
            return json.load(file)
        else:
            raise ValueError("Unsupported file format. Please provide a YAML or JSON file.")

# %%
