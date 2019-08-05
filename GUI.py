from tkinter import *
from tkinter import filedialog
import os

root = Tk()
root.title("Naive Bayes Classifier")

directoryPathTxt = Label(root, text="Directory Path:\t")
directoryPathTxt.grid(row = 4, column = 0, sticky=W)
directoryPathInput = Entry(root, width=40, bg="white")
directoryPathInput.grid(row = 4, column = 1, sticky = W)


def browse_directory_path():
    global directory_path
    directory_path = filedialog.askdirectory()
    directoryPathInput.delete(0, END)
    directoryPathInput.insert(END, directory_path)


directoryPathBtn = Button(root, text="Browse", width = 6, command = browse_directory_path)
directoryPathBtn.grid(row = 4, column = 2, sticky = W)

discretizationBinsTxt = Label(root, text="Discretization Bins:\t")
discretizationBinsTxt.grid(row = 5, column = 0, sticky=W)
discretizationBinsInput = Entry(root, width=40, bg="white")
discretizationBinsInput.grid(row = 5, column = 1, sticky = W)


def build():
    # build the model
    a = 1


buildBtn = Button(root, text="Build", width = 6, command = build)
buildBtn.grid(row = 7, column = 1, sticky = W)

classifyBtn = Button(root, text="Classify", width = 6, command = build)
classifyBtn.grid(row = 9, column = 1, sticky = W)

root.mainloop()
