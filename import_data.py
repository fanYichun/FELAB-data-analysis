import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from scipy.io import savemat
from scipy.io import loadmat
import numpy as np
import csv


def select_files(filetypes):
    ''' open a GUI window, select the files

    input:
    filetypes - types of file to select

    output:
    tuple of file names
    '''
    root = tk.Tk()
    filename = askopenfilename(filetypes=[filetypes],
                               title="Select files...", multiple=1)
    root.destroy()
    print('User selected ' + str(len(filename)) + ' files')
    return filename


def read_csv(file_name, dtype=int):
    '''
    read .csv data files, only the first colomn

    input:
    file_name - the csv file to read
    dtype - type for numpy array

    output:
    data, numpy array
    '''
    matfile_path = Path(file_name[: -3] + 'mat')
    if matfile_path.is_file():
        table = loadmat(matfile_path)['points'].flatten()
    else:
        table = []
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                table.append(dtype(row[0]))
        table = np.array(table, dtype=dtype)
        savemat(matfile_path, {'points': table})
    return table


def read_dat(file_name, dtype=int):
    '''
    read .dat data files

    input:
    file_name - the dat file to read
    dtype - type for numpy array

    output:
    data, numpy array
    '''
    table = np.fromfile(file_name, dtype=dtype)
    return table
