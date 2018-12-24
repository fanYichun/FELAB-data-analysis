import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from scipy.io import savemat
from scipy.io import loadmat
import numpy as np
import xlrd
import csv


def select_files(filetypes):
    ''' Open a GUI window, select the files

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


def read_csv(file_name, dtype=float):
    ''' Read .csv data files, only the first colomn

    input:
        file_name - the csv file to read
        dtype - type of numpy array

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


def read_dat(file_name, dtype=float):
    ''' Read .dat data files

    input:
        file_name - the dat file to read
        dtype - type of numpy array

    output:
        data, numpy array
    '''
    table = np.fromfile(file_name, dtype=dtype)
    return table


def read_oscilloscope_txt(file_name, skiprows=5, dtype=float):
    ''' Read .txt data files generated by oscilloscope

    input:
        file_name - the txt file to read
        skiprows - first several rows to ignore
        dtype - type of numpy array

    output:
        data, numpy array
    '''
    matfile_path = Path(file_name[: -3] + 'mat')
    if matfile_path.is_file:
        data = loadmat(matfile_path)

        time = data['time'].flatten()
        amp = data['amplitude'].flatten()
    else:
        txt_data = np.loadtxt(file_name, skiprows=skiprows, dtype=dtype)

        time = txt_data[:, 0] * 1e9  # ns
        amp = txt_data[:, 1] * 1e3  # mV
        peak_index = amp.argmin()
        time = time - time[peak_index]

        savemat(matfile_path, {'time': time, 'amplitude': amp})
    return time, amp


def read_xls(file_name, row_range, col):
    ''' Get a part from an xls file

    input:
        file_name - the xls file to read
        row_range - range of the rows
        col - number of the col
    output:
        data in the range, list
    '''
    def xl_get_sh(file_name):
        ''' Get the first sheet from the xls file
        
        input:
            file_name - the xls file to read
        output:
            the sheet defined in package xlrd
        '''
        book = xlrd.open_workbook(file_name)
        sh = book.sheet_by_index(0)
        return sh
    
    sh = xl_get_sh(file_name)
    data = list(row_range)
    ind = 0
    for row in row_range:
        data[ind] = sh.cell_value(row, col)
        ind += 1
    return data
