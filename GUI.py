import tkinter as tk
from tkinter import *
from tkinter import filedialog
import Model
import Structure
import os

root = Tk()
root.title("Naive Bayes Classifier")


def validate_directory(directory):
    if directory:
        return check_if_all_needed_files_exists() == True
    return False


def validate_bins(bins):
    if bins:
        try:
            bins_num = int(bins)
            return bins_num > 0
        except ValueError:
            return False
    return False


def enable_disable_build_button(*args):
    directory = directory_path_var.get()
    bins = discretization_bins_var.get()
    if validate_directory(directory) and validate_bins(bins):
        buildBtn.config(state='normal')
    else:
        buildBtn.config(state='disabled')


directory_path_var = tk.StringVar(root)
directory_path_var.trace("w", enable_disable_build_button)

directoryPathTxt = Label(root, text="Directory Path:\t")
directoryPathTxt.grid(row = 4, column = 0, sticky=W)
directoryPathInput = Entry(root, width=40, bg="white", textvariable=directory_path_var, state="disabled")
directoryPathInput.grid(row = 4, column = 1, sticky = W)


def check_if_all_needed_files_exists():
    global directory_path
    global structure_file_name
    global train_file_name
    global test_file_name

    print 'checking'
    if directory_path:
        if os.path.isdir(directory_path):
            # check if the directory contains Structure.txt, train.csv, test.csv
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            if structure_file_name not in files:
                return 'The "' + structure_file_name + '" file is not in the given directory'
            if train_file_name not in files:
                return 'The "' + train_file_name + '" file is not in the given directory'
            if test_file_name not in files:
                return 'The "' + test_file_name + '" file is not in the given directory'
            return True
        else:
            return 'The chosen file is not a directory'
    else:
        return 'You must pick the wanted directory'


def browse_directory_path():
    global directory_path
    directory_path = filedialog.askdirectory()
    result = check_if_all_needed_files_exists()
    if result == True:
        directoryPathInput.config(state="normal")
        directoryPathInput.delete(0, END)
        directoryPathInput.insert(END, directory_path)
        directoryPathInput.config(state="disabled")
    else:
        print result


directoryPathBtn = Button(root, text="Browse", width = 6, command = browse_directory_path)
directoryPathBtn.grid(row = 4, column = 2, sticky = W)

discretization_bins_var = tk.StringVar(root)
discretization_bins_var.trace("w", enable_disable_build_button)

discretizationBinsTxt = Label(root, text="Discretization Bins:\t")
discretizationBinsTxt.grid(row = 5, column = 0, sticky=W)
discretizationBinsInput = Entry(root, width=40, bg="white", textvariable=discretization_bins_var)
discretizationBinsInput.grid(row = 5, column = 1, sticky = W)


def build():
    # build the model
    global model
    global structure
    print 'building'
    classifyBtn.config(state="disabled")
    try:
        structure = Structure.Structure('structure_path')
        model = Model.Model('train.csv', structure=structure, binsNum=binsNum)

        print 'done building the model'
        classifyBtn.config(state="normal")
    except Exception as err:
        print err


def classify():
    # classify the test file
    global model
    print 'classifying'
    output_path = pick_output_path()
    model.classify('test_file.csv', output_path)


model = None
structure = None
directory_path = None

structure_file_name = 'Structure.txt'
train_file_name = 'train.csv'
test_file_name = 'test.csv'

buildBtn = Button(root, text="Build", width = 6, command = build, state="disabled")
buildBtn.grid(row = 7, column = 1, sticky = W)

classifyBtn = Button(root, text="Classify", width = 6, command = classify, state="disabled")
classifyBtn.grid(row = 9, column = 1, sticky = W)

root.mainloop()
