import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog


gui = ThemedTk(theme = 'yaru')


tables_folder_path = tk.StringVar()

#Browse folder command funciton
def get_dir():
    sel_dir = filedialog.askdirectory(initialdir = '', title = "Where are your files?", mustexist = True)
    tables_folder_path.set(sel_dir)

#create gui window

gui.title("mRNA-Organelle Colocalization Tool")
gui.geometry('1280x720')
folder_lbl = ttk.Button(gui, text = "Browse Folder", command = get_dir)
folder_lbl.grid(row = 1, column = 0)
folder_entry = ttk.Entry(gui, textvariable = tables_folder_path)
folder_entry.grid(row = 2, column = 0)
#get mRNA intesities min/max
mrna_int = ttk.Label(gui, text = 'Enter mRNA Intesity values:')
mrna_int.grid(row = 3, column = 0)
mrna_min_lbl = ttk.Label(gui, text = "min:")
mrna_min_lbl.grid(row = 4, column = 0)
mrna_min = ttk.Entry(gui)
mrna_min.grid(row = 4, column = 1)
mrna_max_lbl = ttk.Label(gui, text = "max:")
mrna_max_lbl.grid(row = 5, column = 0)
mrna_max = ttk.Entry(gui)
mrna_max.grid(row = 5, column = 1)
#get organelle coverages min/max
org_int = ttk.Label(gui, text = 'Enter Organelle Coverage values:')
org_int.grid(row = 6, column = 0)
org_min_lbl = ttk.Label(gui, text = "min:")
org_min_lbl.grid(row = 7, column = 0)
org_min = ttk.Entry(gui)
org_min.grid(row = 7, column = 1)
org_max_lbl = ttk.Label(gui, text = "max:")
org_max_lbl.grid(row = 8, column = 0)
org_max = ttk.Entry(gui)
org_max.grid(row = 8, column = 1)
#Run filtering and analysis

#Plot filtered data



gui.mainloop()