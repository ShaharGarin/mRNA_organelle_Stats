#Calc % for localizations: NC, ER total and nER cER
#Calc avarage ER coverage

import mRNA_organelle_colo_fun as xf
from tkinter import filedialog
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import ast


total_mrna = "Total mRNA per Cell"
col_ner_title = "Total Colocolized With Organelle Near"
col_cer_title = "Total Colocolized With Organelle Far"
not_col_title = "Total Not Colocolized with Organelle"
org_cov_title = "Organelle Signal Coverage Of Cell List"
colo_dict = {'nc':not_col_title, 'organelle_far':col_cer_title, 'organelle_near':col_ner_title}
mrna_z_title = "mRNAs z coords"
mrna_int_title = "mRNAs intensities"
mrna_colo_title = "mRNAs status"
new_folder_string = "/Calc Tables/"
tot_col_rat = "Total Colocolized Ratio"
ner_col_rat = "nER Colocalization Ratio"
cer_col_rat = "cER Colocalization Ration"
not_col_rat = "Not Colocalized Ratio"
ava_org_cov = "Average Organelle Coverage"
title_order = [total_mrna, tot_col_rat, not_col_rat, ner_col_rat, cer_col_rat]
sample_dict = {}



#Create gui window
gui = ThemedTk(theme = 'yaru')
tables_folder_path = tk.StringVar()
sam_num = tk.IntVar()
error_lbl = ttk.Label(gui, text = "")
error_lbl.grid(row = 11, column = 0)

#Browse folder command function. Also checks folder and number of csv files in it.
def get_dir():
    sel_dir = filedialog.askdirectory(initialdir = '', title = "Where are your files?", mustexist = True)
    tables_folder_path.set(sel_dir)
    if tables_folder_path.get() == '':
        error_lbl.config(text = "No folder selected", foreground = 'indigo')
    elif len(csv_files_list(tables_folder_path.get())) == 0:
        error_lbl.config(text = "The folder has no csv files", foreground = 'indigo') 
    else:
        error_lbl.config(text = '')
        sam_num.set(os.listdir(tables_folder_path.get()))

def check_ids():
    ident_list = list(file_names.get().split(' '))
    if ident_list == ['']:
        error_lbl.config(text = "No identifiers entered", foreground = 'indigo')
    else:
        error_lbl.config(text = '')
        file_ids.config(text = f"You have {len(ident_list)} sample(s): \n {ident_list}", justify = 'center')
        #Check each id given has an associated file
        check_ids_exist(ident_list)

def check_ids_exist(id_list):
    folder_files = csv_files_list(folder_entry.get())
    missing_id = []
    mult_files = []
    #check if all ids are found in folder
    for id in id_list:
        appear = 0
        appear = sum(1 for x in folder_files if id in x)
        if appear == 0:
            missing_id.append(id)
        #check if all id appear only once
        if appear > 1:
            mult_files.append(id)
    if missing_id != []:
         error_lbl.config(text = f"The following ids given don't match any file: {missing_id}.\nCan't continue.", foreground = 'indigo', justify = 'center')
    if mult_files != []:
        error_lbl.config(text = f"The following ids given appear more than once: {mult_files}.\nCan't continue.", foreground = 'indigo', justify = 'center')
    

def check_names():
    name_list = list(sample_names.get().split(' '))
    ident_list = list(file_names.get().split(' '))
    if ident_list == ['']:
        error_lbl.config(text = "No identifiers entered", foreground = 'indigo')
    elif name_list == ['']:
        error_lbl.config(text = "No names entered", foreground = 'indigo')
    elif len(name_list) != len(ident_list):
        error_lbl.config(text = "Number of ids and names don't match.\nCan't Continue", foreground = 'indigo', justify = 'center')
    else:
        for sample in range(len(name_list)):
            strain_name = name_list[sample]
            strain_ident = ident_list[sample]
            sample_dict[strain_name] = strain_ident
        error_lbl.config(text = '')
        sample_names_lbl.config(text = f"Your sample(s): {sample_dict} \nMake sure the order is right.", justify = 'center')

def filter_main():
    if len(folder_entry.get()) == 0 or len(file_names.get()) == 0 or len(sample_names.get()) == 0 or error_lbl.cget('text') != '':
        filter_lbl.config(text = "One or more of the needed inputs is missing or wrong.", foreground = 'indigo')
    else:
        filter_vals_list = [mrna_max.get(), mrna_min.get(), org_max.get(), org_min.get()]
        for val in filter_vals_list:
            try: val = float(val) 
            except: ValueError
        if type(val) != float:
            filter_lbl.config(text = "Filter value not a number.", foreground = 'indigo')
        else:
            filter_lbl.config(text = '')
            zero_filter(folder_entry.get())
            file_list = csv_files_list(f"{folder_entry.get()}{new_folder_string}")
            for file in file_list:
                for id in list(file_names.get().split(' ')):
                    if id not in file:
                        print(1)
                        continue
                    else:
                        file_df = pd.read_csv(file)
                        for i, row in file_df.iterrows():
                            int_list = ast.literal_eval(row[mrna_int_title])
                            colo_list = ast.literal_eval(row[mrna_colo_title])
                            #filter by mRNA intensity
                            filter_list = []
                            for i in range(len(int_list)):
                                if float(int_list[i]) > float(mrna_max.get()) or float(int_list[i]) < float(mrna_min.get()):
                                    print(1)
                                    row[total_mrna] = int(row[total_mrna]) - 1
                                    row[colo_dict[colo_list[i]]] = int(row[colo_dict[colo_list[i]]]) - 1
                                    filter_list.append(i)
                            for i in sorted(filter_list, reverse = True):
                                del int_list[i]
                                row[mrna_int_title] = int_list
                                del colo_list[i]
                                row[mrna_colo_title] = colo_list
                        file_df = file_df.loc[file_df[total_mrna] != 0]
                        file_df.to_csv(f"{file} filtered.csv")
                        #filter by organelle coverage
        filter_done_lbl.config(text = f'Filtered and unfiltered tables saved in {folder_entry.get()}{new_folder_string}')

def mrna_filter():
    return

def org_filter():
    return

def plot_data():
    return

#Design gui window
gui.title("mRNA-Organelle Colocalization Tool")
gui.geometry('')
title_lbl = ttk.Label(gui, text = "mRNA-Organelle Colocalization Tool", font = ('Calibri', 32, 'bold underline'), justify = 'center')
title_lbl.grid(row = 0, column = 0, columnspan = 4, pady = 10)

#get folder
folder_entry = ttk.Entry(gui, textvariable = tables_folder_path, width = 100, justify = 'center')
folder_entry.grid(row = 1, column = 0)
folder_lbl = ttk.Button(gui, text = "Enter Folder", command = get_dir)
folder_lbl.grid(row = 2, column = 0)

#get file/sample ids
file_names_lbl = ttk.Label(gui, text = 'Enter file indentifiers (case sensetive with spaces seperating each):')
file_names_lbl.grid(row = 3, column = 0)
file_names = ttk.Entry(gui, width = 50, justify = 'center')
file_names.grid(row  = 4, column = 0)
file_names_but = ttk.Button(gui, text = 'Enter', command = check_ids)
file_names_but.grid(row = 5, column = 0)
file_ids = ttk.Label(gui, text = '')
file_ids.grid(row = 6, column = 0)

#get sample names
sample_name_lbl = ttk.Label(gui, text = 'Enter sample names (will appear in tables and plots. Same order as ids):')
sample_name_lbl.grid(row = 7, column = 0)
sample_names = ttk.Entry(gui, width = 50, justify = 'center')
sample_names.grid(row = 8, column = 0)
sample_names_but = ttk.Button(gui, text = 'Enter', command = check_names)
sample_names_but.grid(row = 9, column = 0)
sample_names_lbl = ttk.Label(gui, text = '')
sample_names_lbl.grid(row = 10, column = 0)

#Filter values seperator
sep1 = ttk.Separator(gui, orient = 'vertical')
sep1.grid(row = 1, column = 1, rowspan = 11, columnspan = 1, sticky = 'ns', padx = 2, pady = 2)

#get mRNA intesities min/max
mrna_int_lbl = ttk.Label(gui, text = 'Enter mRNA Intensity values:', justify = 'center')
mrna_int_lbl.grid(row = 1, column = 2, columnspan = 2)
mrna_min_lbl = ttk.Label(gui, text = "min:")
mrna_min_lbl.grid(row = 2, column = 2)
mrna_min = ttk.Entry(gui, width = 10, justify = 'center')
mrna_min.insert(0, '0.1')
mrna_min.grid(row = 3, column = 2)
mrna_max_lbl = ttk.Label(gui, text = "max:")
mrna_max_lbl.grid(row = 2, column = 3)
mrna_max = ttk.Entry(gui, width = 10, justify = 'center')
mrna_max.insert(0, '65535')
mrna_max.grid(row = 3, column = 3)

#get organelle coverages min/max
org_int = ttk.Label(gui, text = 'Enter Organelle Coverage values:', justify = 'center')
org_int.grid(row = 4, column = 2, columnspan = 2)
org_min_lbl = ttk.Label(gui, text = "min:")
org_min_lbl.grid(row = 5, column = 2)
org_min = ttk.Entry(gui, width = 10, justify = 'center')
org_min.insert(0, '0.01')
org_min.grid(row = 6, column = 2)
org_max_lbl = ttk.Label(gui, text = "max:")
org_max_lbl.grid(row = 5, column = 3)
org_max = ttk.Entry(gui, width = 10, justify = 'center')
org_max.insert(0, '100')
org_max.grid(row = 6, column = 3)

#Run filtering and analysis
filter_but = ttk.Button(gui, text = 'Filter', command = filter_main)
filter_but.grid(row = 8, column = 2, columnspan = 2)
filter_lbl = ttk.Label(gui, text = '', justify = 'center', foreground = 'indigo')
filter_lbl.grid(row = 9, column = 2, columnspan = 2)
filter_done_lbl = ttk.Label(gui, text = '', justify = 'center', foreground = 'darkgreen')
filter_done_lbl.grid(row = 10, column = 2, columnspan = 2)

#Plots seperator
sep2 = ttk.Separator(gui, orient = 'horizontal')
sep2.grid(row = 12, column = 0, rowspan = 1, columnspan = 100, sticky = 'ew', padx = 2, pady = 2)

#Plot filtered data
plot_but = ttk.Button(gui, text = 'Plot', command = plot_data)
plot_but.grid(row = 13, column = 0, columnspan = 4)


# def main():
 
#     my_strain_dic = calc_tables(tables_folder_path)
#     #statistics_table(tables_folder_path)
#     statistics_table(tables_folder_path + new_folder_string, my_strain_dic)
    
#     return f"Tables saved in {tables_folder_path + new_folder_string}"

def zero_filter(folder_path):
    csv_files = csv_files_list(folder_path)
    my_strains = sample_dict
    try: os.makedirs(folder_path + new_folder_string)
    except: FileExistsError
    for key in my_strains:
            for file in csv_files:
                if my_strains[key] in file:
                    file_df = pd.read_csv(file)
                    file_df = file_df.loc[file_df[total_mrna] != 0]
                    file_df.to_csv(f"{folder_path}{new_folder_string}{key} no zero.csv")
    

#Calc ratios and averages and add to csv
def calc_tables(folder_path):
    if folder_path == '':
        print("You didn't select a folder. Quitting.")
        exit()
    csv_files = csv_files_list(folder_path)
    my_strains = get_sample_names()
    try: os.makedirs(folder_path + new_folder_string)
    except: FileExistsError
    for key in my_strains:
            for file in csv_files:
                if my_strains[key] in file:
                    file_df = pd.read_csv(file)
                    file_df = file_df.loc[file_df[total_mrna] != 0]
                    file_df[ner_col_rat] = xf.calc_loc_ratio(file_df[total_mrna].tolist(), file_df[col_ner_title].tolist())
                    file_df[cer_col_rat] = xf.calc_loc_ratio(file_df[total_mrna].tolist(), file_df[col_cer_title].tolist())
                    file_df[not_col_rat] = xf.calc_loc_ratio(file_df[total_mrna].tolist(), file_df[not_col_title].tolist())
                    file_df[tot_col_rat] = xf.calc_comp_ratio(file_df[not_col_rat].tolist())
                    file_df[ava_org_cov] = xf.calc_ave_cov(file_df[org_cov_title].tolist())
                    file_df.to_csv(f"{folder_path}{new_folder_string}{key} Calculation Table.csv")
                    print(f"file for {key} done")
    return my_strains

#Calc ttests between all files and avarages of each column and create statistics table in csv file
def statistics_table(folder_path, strain_dic):
    file_list = csv_files_list(folder_path)
    tot_mrna_ave = ["Total Signals per Cell Average", "Total Signals per Cell SEM"]
    tot_col_ave = ["Total Colocolized Average", "Total Colocolized SEM"]
    ner_col_ave = ["Total Not Colocolized Average", "Total nER SEM"]
    cer_col_ave = ["Total nER Average", "Total cER SEM"]
    not_col_ave = ["Total cER Average", "Total Not Colocolized SEM"]
    col_list = [tot_mrna_ave[0], tot_mrna_ave[1], tot_col_ave[0], tot_col_ave[1], not_col_ave[0], not_col_ave[1], ner_col_ave[0], ner_col_ave[1], cer_col_ave[0], cer_col_ave[1]]
    stat_df = pd.DataFrame(index = col_list, columns = list(strain_dic.keys()))
    for key in strain_dic:
        for file in file_list:
            if key in file:
                file_df = pd.read_csv(file)
                col = 0
                for title in range(len(title_order)):
                    stat = xf.calc_col_ava(file_df[title_order[title]].tolist())
                    stat_df.loc[col_list[col], key] = stat[0]
                    col += 1
                    stat_df.loc[col_list[col], key] = stat[1]
                    col += 1
    stat_df.to_csv(f"{folder_path}Stats Table.csv")
    print("Statistics table produced.")          

#Create a list of csv path files from a folder that may contain other files/folders
def csv_files_list(folder):
    csv_list = []
    for file in os.listdir(folder):
        if str(file).endswith("csv", -3):
            csv_list.append(os.path.abspath(os.path.join(folder, file)))
    return csv_list

#Get samples names from user and create list for each type
def get_sample_names():
    num_strains = int(input("How many sample types in your experiment? "))
    strains_dict = {}
    for sample in range(num_strains):
        strain_name = input(f"Name of sample type {sample + 1}: ")
        strain_ident = input(f"Specifict Identifier in sample {sample + 1} file names: ")
        strains_dict[strain_name] = strain_ident
    return strains_dict


gui.mainloop()
#main()