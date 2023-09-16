############################################################
# Tips:
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
# print_hi('PyCharm')
#
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
############################################################
# myGUI: Plot-tool for LCS_Mon Data (v0.5)
# Art Brown 8/31/2023
#
#
############################################################
# Import libraries
############################################################
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfd
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


############################################################
# declare variables
############################################################
file_Flag = 0
plot_Flag = 0
select_Flag = 0
# fig = 0
i = 0
my_Index = 0
Elapsed_Sec = []
columns = []
my_Array = []
my_Array_of_Arrays = []
my_Vars_Name_Array = ['']
my_Vars_Index_Array = []
my_Vars_Index_len = 0
my_Var_Name = "my_Var_Name"
file_path = "file_path"
read_file = "read_file"
file_Name = "file_Name"

############################################################
# frames and widgets
############################################################
root = Tk()
root.title('myGUI: Plot-tool for LCS_Mon Data (v0.6)')  # TODO: update version number after revision
root.geometry("560x750")
root.minsize(width=560, height=750)

# dialog box
text_box_frame = Frame(root, width=560, height=1)
text_box_frame.grid(row=0, column=0, columnspan=2)

text_box = Text(text_box_frame, height=2, width=70)
text_box.grid(row=0, column=0, columnspan=5, sticky='we')
text_box.config(state=DISABLED)
root.grid_rowconfigure(0, weight=2)

# frame for buttons
btn_frame = Frame(root, width=560, height=1)
btn_frame.grid(row=1, column=0, columnspan=2)

# frame for selections and search
selection_box_frame = Frame(root, width=280, height=1)
selection_box_frame.grid(row=2, column=0)

# frame for variables
variable_box_frame = Frame(root, width=280, height=1)
variable_box_frame.grid(row=2, column=1)

# search box
search_box_label = tk.Label(selection_box_frame, text='search')
search_box_label.grid(row=2, column=1, sticky='ne')
search_box = Text(selection_box_frame, height=1, width=30)
search_box.grid(row=3, column=1, sticky='ne')
search_box.config(state=NORMAL)
search_box.insert('end', 'WIP')

# search results
search_results_box_label = tk.Label(selection_box_frame, text='search results')
search_results_box_label.grid(row=4, column=1, sticky='ne')
search_results_box = Text(selection_box_frame, height=5, width=30)
search_results_box.grid(row=5, column=1, sticky='n')
search_results_box.insert('end', 'WIP')
search_results_box.config(state=DISABLED)

# text box containing name of selected variables Y1
variable_box_label = tk.Label(selection_box_frame, text='Y-axis 1')
variable_box_label.grid(row=6, column=1, sticky='se')
variable_box = Text(selection_box_frame, height=10, width=30)
variable_box.grid(row=7, column=1, sticky='se')
variable_box.config(state=DISABLED)

# text box containing name of selected variables Y2
variable_box_label2 = tk.Label(selection_box_frame, text='Y-axis 2')
variable_box_label2.grid(row=8, column=1, sticky='se')
variable_box2 = Text(selection_box_frame, height=10, width=30)
variable_box2.grid(row=9, column=1, sticky='se')
variable_box2.config(state=DISABLED)

# table placeholder to prevent dancing widgets
variable_box_label = tk.Label(variable_box_frame, text='All Variables')
variable_box_label.grid(row=2, column=2, sticky='ne')
table = ttk.Treeview(variable_box_frame, columns="columns", height=30)
table.grid(row=3, column=2)
table.column("#0", anchor='c', stretch=NO, width=40)
table.column("#1", anchor='c', stretch=YES, width=200)
table.heading("#0", text="#")
table.heading("#1", text="Variable")


############################################################
# callback function
# this is main function that is triggered by select file button.
# opens file prompt, updates dialog box, and pulls variable names into a table
############################################################
def callback():
    global file_Flag
    global file_path
    global file_Name
    global read_file
    global i
    global table
    global columns
    # file prompt
    file_path = tkfd.askopenfilename()
    file_Name = os.path.basename(file_path)
    # insert file name in dialog box
    text_box.config(state='normal')
    text_box.delete('1.0', 'end')  # clear the box of current contents
    text_box.insert('end', file_Name)
    if not file_path:
        text_box.delete("1.0", "end")
        text_box.insert('end', 'dialog was cancelled')
        return
    # check file type
    if file_Name.endswith(".txt") and file_Name.startswith("Data - "):
        text_box.insert('end', ': valid text file\n')
        file_Flag = 1
    else:
        text_box.insert('end', ': invalid file type\n')
        file_Flag = 0

    if file_Flag == 1:
        # format dataframe
        read_file = pd.read_csv(file_path, skiprows=3, sep="\t", low_memory=False)
        columns = list(read_file.columns)  # adding column header list
        # print(columns)
        read_file.head()
        read_file.set_index('Elapsed Sec', inplace=True)
        # Add table of variables with scrollbar
        table = ttk.Treeview(variable_box_frame, columns="columns", height=30)
        table.grid(row=3, column=2)
        table.column("#1", anchor='c', stretch=NO, width=40)
        table.column("#0", anchor='c', stretch=YES, width=200)
        table.heading("#1", text="#")
        table.heading("#0", text="Variable")
        for i in range(len(columns)):
            print(columns[i])
            table.insert(parent="", index=i, iid=i, text=columns[i], values=i+1)  # TODO: fix this, throws warning
        scrollbar = ttk.Scrollbar(variable_box_frame, orient="vertical", command=table.yview)
        scrollbar.grid(row=3, column=3, sticky='ns')
        table.config(yscrollcommand=scrollbar.set)
        table.bind('<ButtonRelease-1>', select_item)
        table.bind('<ButtonRelease-3>', select_item2)
    # disable dialog box
    text_box.config(state='disabled')


############################################################
# select item function
############################################################
def select_item(a):
    global select_Flag
    global file_Flag
    global table
    global my_Var_Name
    global columns
    global my_Index
    global my_Vars_Name_Array
    global my_Vars_Index_Array
    global my_Vars_Index_len
    # turn on boxes
    variable_box.config(state='normal')
    text_box.config(state='normal')
    # check the file flag is good
    if file_Flag == 1:
        # get the highlighted selection
        my_Index = table.selection()[0]
        # store the name, and it's index in arrays and get the length of array
        my_Vars_Name_Array.append(columns[int(my_Index)])
        my_Vars_Index_Array.append(int(my_Index))
        my_Vars_Index_len = (int(len(my_Vars_Index_Array)))
        # check for duplicates
        if my_Vars_Index_len > 0:
            my_Vars_Name_Array = list(set(my_Vars_Name_Array))
            my_Vars_Index_Array = list(set(my_Vars_Index_Array))
            # add the variable names to the list of selections
            variable_box.delete('1.0', 'end')
            i = 0
            while i < my_Vars_Index_len:
                variable_box.insert('end', my_Vars_Name_Array[i])
                variable_box.insert('end', '\n')
                i = i + 1
    else:
        text_box.delete('1.0', 'end')
        text_box.insert('end', 'no file selected')

    # turn off boxes
    variable_box.config(state='disabled')
    text_box.config(state='disabled')
    # set the flag high once complete
    select_Flag = 1
    # todo: cleanup variable list dupe handling, little buggy

def select_item2(a):
    global select_Flag
    global file_Flag
    global table
    global my_Var_Name
    global columns
    global my_Index
    global my_Vars_Name_Array
    global my_Vars_Index_Array
    global my_Vars_Index_len
    # turn on boxes
    variable_box2.config(state='normal')
    text_box.config(state='normal')
    # check the file flag is good
    if file_Flag == 1:
        # get the highlighted selection
        my_Index = table.selection()[0]
        # store the name, and it's index in arrays and get the length of array
        my_Vars_Name_Array.append(columns[int(my_Index)])
        my_Vars_Index_Array.append(int(my_Index))
        my_Vars_Index_len = (int(len(my_Vars_Index_Array)))
        # check for duplicates
        if my_Vars_Index_len > 0:
            my_Vars_Name_Array = list(set(my_Vars_Name_Array))
            my_Vars_Index_Array = list(set(my_Vars_Index_Array))
            # add the variable names to the list of selections
            variable_box2.delete('1.0', 'end')
            i = 0
            while i < my_Vars_Index_len:
                variable_box2.insert('end', my_Vars_Name_Array[i])
                variable_box2.insert('end', '\n')
                i = i + 1
    else:
        text_box.delete('1.0', 'end')
        text_box.insert('end', 'no file selected')

# def start_drag(self, event):
#     index = self.nearest(event.y)
#     value = self.get(index)
#     if value:
#         self.drag_data = (index, value)
#
#
# def do_drag(self, event):
#     if self.drag_data:
#         index, value = self.drag_data
#         self.delete(index)
#         self.selection_clear(0, tk.END)
#         self.selection_set(index)
#         self.activate(index)
#         self.insert(index, value)
#
#
# def end_drag(self, event):
#     if self.drag_data:
#         index, value = self.drag_data
#         self.selection_clear(0, tk.END)
#         self.insert(index, value)
#         self.drag_data = None

############################################################
# Plot data function (includes plot and table)
############################################################
def plotting():
    global file_Flag
    global select_Flag
    global file_path
    global read_file
    global file_Name
    global Elapsed_Sec
    global plot_Flag
    global columns
    global table
    global i
    # global fig
    global my_Index
    global my_Array
    global my_Array_of_Arrays
    global my_Var_Name
    global my_Vars_Name_Array
    global my_Vars_Index_len
    global my_Vars_Index_Array

    # if there already is a plot, and we are adding a variable, clear the existing plot
    if plot_Flag == 1 and select_Flag == 1:
        plt.clf()
        plt.close()
        plot_Flag = 0

    # Plot data
    if plot_Flag == 0 and select_Flag == 1:
        # get x axis
        Elapsed_Sec = np.loadtxt(file_path, skiprows=5, delimiter="\t", usecols=(1,))
        # if the array is not empty
        if len(my_Vars_Index_Array) > 0:
            i = 0
            while i < len(my_Vars_Index_Array):
                # pull selections into the plot
                my_Array = np.loadtxt(file_path, skiprows=5, delimiter="\t", usecols=(int(my_Vars_Index_Array[i]),))
                plt.rcParams['figure.figsize'] = [10, 8]  # sets the figure size without introducing new figures
                plt.plot(Elapsed_Sec, my_Array, label=(columns[int(my_Vars_Index_Array[i])]))  # get labels
                # legend location https://www.geeksforgeeks.org/how-to-place-legend-outside-of-the-plot-in-matplotlib/#
                # TODO: fix legend box
                # plt.legend(bbox_to_anchor=(1.2, 0.5), loc="center right")
                plt.legend(loc="upper right")
                i = i + 1
            plot_Flag = 1
            plt.title(file_Name)
            plt.xlabel('Elapsed Sec')
            plt.ylabel('Amplitude')
            plt.show()

    # fallback error message
    if plot_Flag == 0 and select_Flag == 0:
        text_box.config(state='normal')
        text_box.delete('1.0', 'end')
        text_box.insert('end', 'no file/variables selected')
        text_box.config(state='disabled')


############################################################
# Clear function
############################################################
def clear_all():
    global file_Flag
    global plot_Flag
    global select_Flag
    global read_file
    global text_box
    global variable_box
    global my_Index
    global my_Array
    global my_Var_Name
    global my_Vars_Index_len
    global my_Vars_Index_Array
    my_Index = 0
    my_Array = 0
    my_Var_Name = 0
    my_Vars_Index_len = 0
    file_Flag = 0
    plot_Flag = 0
    select_Flag = 0
    plt.clf()
    plt.close()
    my_Vars_Index_Array = []
    text_box.config(state='normal')
    variable_box.config(state='normal')
    text_box.delete("1.0", "end")
    variable_box.delete("1.0", "end")
    text_box.config(state='disabled')
    variable_box.config(state='disabled')


############################################################
# Buttons to call commands, need to be after definitions
############################################################
btn = Button(btn_frame, text="Select File", command=callback)
btn.grid(row=0, column=1, sticky='nw')

btn2 = Button(btn_frame, text="Plot File", command=plotting)
btn2.grid(row=0, column=2, sticky='nw')

btn3 = Button(btn_frame, text="Clear", command=clear_all)
btn3.grid(row=0, column=3, sticky='nw')


############################################################
# run instance
############################################################
root.bind('<Return>', lambda event: callback())
root.mainloop()

############################################################
# EOF
############################################################
