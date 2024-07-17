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
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


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
cer_col_rat = "cER Colocalization Ratio"
not_col_rat = "Not Colocalized Ratio"
ava_org_cov = "Average Organelle Coverage"
title_order = [total_mrna, tot_col_rat, not_col_rat, ner_col_rat, cer_col_rat, ava_org_cov]
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
        ident_list = [id for id in ident_list if id != '']
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
        sample_name_lbl.config(text = '')
    else:
        ident_list = [id for id in ident_list if id != '']
        name_list = [name for name in name_list if name != '']
        for sample in range(len(name_list)):
            strain_name = name_list[sample]
            strain_ident = ident_list[sample]
            sample_dict[strain_name] = strain_ident
        error_lbl.config(text = '')
        sample_names_lbl.config(text = f"Your sample(s): {sample_dict} \nMake sure the order is right.", justify = 'center')

def filter_main():
    if len(folder_entry.get()) == 0 or len(file_names.get()) == 0 or len(sample_names.get()) == 0 or error_lbl.cget('text') != '':
        filter_lbl.config(text = "One or more of the needed inputs is missing or wrong.", foreground = 'indigo')
    elif file_ids.cget('text') == '' or sample_name_lbl.cget('text') == '':
        filter_lbl.config(text = "Enter sample names/ids", foreground = 'indigo')
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
                for name in list(sample_names.get().split(' ')):
                    if name in file:
                        file_df = pd.read_csv(file)
                        #filter by mRNA intensity
                        filtered_mrna = mrna_filter(file_df)
                        #filter by organelle coverage
                        file_df = filtered_mrna.loc[file_df[total_mrna] != 0]
                        filtered_org = org_filter(file_df)
                        file_df = filtered_org.loc[file_df[total_mrna] != 0]
                        file_df.to_csv(f"{folder_entry.get()}{new_folder_string}{name} filtered.csv", index = False)
                        calc_tables(f"{folder_entry.get()}{new_folder_string}")        
            #statistical comparisons table
            statistics_table(f'{folder_entry.get()}{new_folder_string}')
            filter_done_lbl.config(text = f'Tables saved in {folder_entry.get()}{new_folder_string}')

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
                    file_df.to_csv(f"{folder_path}{new_folder_string}{key} no zero.csv", index = False)

def mrna_filter(file_df):
    for i, row in file_df.iterrows():
        int_list = ast.literal_eval(row[mrna_int_title])
        colo_list = ast.literal_eval(row[mrna_colo_title])
        z_list = ast.literal_eval(row[mrna_z_title])
        filter_list = []
        curr_tot = int(file_df.loc[i, total_mrna])
        for j in range(len(int_list)):
            curr_colo = int(file_df.loc[i, colo_dict[colo_list[j]]])
            if float(int_list[j]) > float(mrna_max.get()) or float(int_list[j]) < float(mrna_min.get()):
                curr_tot -= 1
                curr_colo -= 1
                filter_list.append(j)
                file_df.loc[i, colo_dict[colo_list[j]]] = curr_colo
            file_df.loc[i, total_mrna] = curr_tot
        for j in sorted(filter_list, reverse = True):
            del int_list[j]
            del colo_list[j]
            del z_list[j]
        file_df.at[i, mrna_int_title] = int_list
        file_df.at[i, mrna_colo_title] = colo_list
        file_df.at[i, mrna_z_title] = z_list
    return file_df
    

def org_filter(file_df):
    for i, row in file_df.iterrows():
        org_list = ast.literal_eval(row[org_cov_title])
        z_list = row[mrna_z_title]
        colo_list = row[mrna_colo_title]
        int_list = row[mrna_int_title]
        spot_del = []
        
        for cov in range(len(org_list)):
            if org_list[cov] < float(org_min.get()) or org_list[cov] > float(org_max.get()):
                for z in range(len(z_list)):
                    if z_list[z] == cov:
                        spot_del.append(z)
        curr_tot = int(file_df.loc[i, total_mrna])
        for spot in sorted(spot_del, reverse = True):
            curr_colo = int(file_df.loc[i, colo_dict[colo_list[spot]]])
            curr_tot -= 1
            curr_colo -= 1
            file_df.loc[i, colo_dict[colo_list[spot]]] = curr_colo
            del z_list[spot]
            del colo_list[spot]
            del int_list[spot]
        file_df.loc[i, total_mrna] = curr_tot
    return file_df

#Calc ratios and averages and add to csv
def calc_tables(folder_path):
    csv_files = csv_files_list(folder_path)
    csv_files = [f for f in csv_files if 'filtered' in f]
    for key in sample_dict:
            for file in csv_files:
                if key in file:
                    file_df = pd.read_csv(file)
                    file_df[ner_col_rat] = xf.calc_loc_ratio(file_df[total_mrna].tolist(), file_df[col_ner_title].tolist())
                    file_df[cer_col_rat] = xf.calc_loc_ratio(file_df[total_mrna].tolist(), file_df[col_cer_title].tolist())
                    file_df[not_col_rat] = xf.calc_loc_ratio(file_df[total_mrna].tolist(), file_df[not_col_title].tolist())
                    file_df[tot_col_rat] = xf.calc_comp_ratio(file_df[not_col_rat].tolist())
                    file_df[ava_org_cov] = xf.calc_ave_cov(file_df[org_cov_title].tolist(), float(org_min.get()), float(org_max.get()))
                    file_df.to_csv(f"{folder_path}{key} Calculation Table.csv", index = False)

#Calc ttests between all files and avarages of each column and create statistics table in csv file
def statistics_table(folder_path):
    file_list = csv_files_list(folder_path)
    file_list = [f for f in file_list if 'Calculation Table' in f]
    tot_mrna_ave = ["Total Signals per Cell Average", "Total Signals per Cell SEM"]
    tot_col_ave = ["Total Colocolized Average", "Total Colocolized SEM"]
    ner_col_ave = ["Total Not Colocolized Average", "Total nER SEM"]
    cer_col_ave = ["Total nER Average", "Total cER SEM"]
    not_col_ave = ["Total cER Average", "Total Not Colocolized SEM"]
    org_cov_ave = ["Organelle Coverage Average", "Organelle Coverage SEM"]
    col_list = [tot_mrna_ave[0], tot_mrna_ave[1], tot_col_ave[0], tot_col_ave[1], not_col_ave[0], not_col_ave[1], ner_col_ave[0], ner_col_ave[1], cer_col_ave[0], cer_col_ave[1], org_cov_ave[0], org_cov_ave[1]]
    stat_df = pd.DataFrame(index = col_list, columns = list(sample_dict.keys()))
    for key in sample_dict:
        for file in file_list:
            if key in file:
                file_df = pd.read_csv(file)
                col = 0
                for title in range(len(title_order)):
                    mean_err = xf.calc_col_ava(file_df[title_order[title]].tolist())
                    stat_df.loc[col_list[col], key] = mean_err[0]
                    col += 1
                    stat_df.loc[col_list[col], key] = mean_err[1]
                    col += 1
    anova_list = []
    anova_list = anova_comp(folder_path)
    #Statistcal comparison via anova and Tuckey
    if anova_list != []:
        stat_df.loc['Anova Statistic', 0] = anova_list[0][0]
        stat_df.loc['Anova p-value', 0] = anova_list[0][1]
        for res in range(len(anova_list[1])):
                for key in range(len(sample_dict.keys())):
                    stat_df.loc[f'Tukey HSD Test pvalues {list(sample_dict.keys())[res]}', list(sample_dict.keys())[key]] = anova_list[1][res][key]
            
    stat_df.to_csv(f"{folder_path}Stats Table.csv")

#Calc anove nad tuckey between all samples
def anova_comp(folder):
    file_list = csv_files_list(folder)
    file_list = [file for file in file_list if 'Calculation Table' in file]
    loc_anova = make_dic(file_list)
    if len(loc_anova.values()) == 1:
        filter_lbl.config(text = "Only one sample. Nothing to compare", foreground = 'indigo')
        return []
    else:
        anova_res = stats.f_oneway(*loc_anova.values())
        tukey_res = stats.tukey_hsd(*loc_anova.values()).pvalue
        return [anova_res, tukey_res]

#create df for anova
def make_dic(files):
    anova_dict = {}
    for key in sample_dict.keys():
        for file in files:
            if key in file:
                file_df = pd.read_csv(file)
                anova_dict[key] = file_df[tot_col_rat].to_list()
    return anova_dict

def make_scatter_dic(files):
    scatter_dict = {}
    for key in sample_dict.keys():
        for file in files:
            if key in file:
                file_df = pd.read_csv(file)
                scatter_dict[key] = [file_df[tot_col_rat].to_list(), file_df[ava_org_cov].tolist()]

    return scatter_dict

#Create a list of csv path files from a folder that may contain other files/folders
def csv_files_list(folder):
    csv_list = []
    for file in os.listdir(folder):
        if str(file).endswith("csv", -3):
            csv_list.append(os.path.abspath(os.path.join(folder, file)))
    return csv_list              

def plot_data():
    plot_files = csv_files_list(f"{folder_entry.get()}{new_folder_string}")
    plot_files = [file for file in plot_files if 'Calculation Table' in file]
    plot_dic = make_dic(plot_files)
    #Get data from plot_dic
    categories = list(plot_dic.keys())
    data_values = list(plot_dic.values())
    #Plot violin plot
    sns.violinplot(data = data_values, inner = 'point')
    plt.xticks(ticks=range(len(categories)), labels=categories)  # Set x-axis tick labels
    plt.xlabel('Samples')
    plt.ylabel('mRNA-Organelle Colocalization Ratio')
    plt.title('mRNA-Organelle Colocalization')
    plot_path = fr'{folder_entry.get()}{new_folder_string}Total Colocalization Plot.png'
    if os.path.isfile(plot_path):
        os.remove(plot_path)
    plt.savefig(plot_path, format = 'png', dpi = 500)
    plt.show()
    plt.close()

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
#Plot image
plot_img = ttk.Label(gui, image = '')
plot_img.grid(row = 14, column = 0, columnspan = 2)


gui.mainloop()