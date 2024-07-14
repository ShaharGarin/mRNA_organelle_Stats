#Calc % for localizations: NC, ER total and nER cER
#Calc avarage ER coverage

import xl_calcs_fun as xf
from tkinter import filedialog
import os
import pandas as pd
# import ast
# import numpy as np
from scipy import stats

total_mrna = "Total mRNA per Cell"
col_ner_title = "Total Colocolized With Organelle Near"
col_cer_title = "Total Colocolized With Organelle Far"
not_col_title = "Total Not Colocolized with Organelle"
org_cov_title = "Organelle Signal Coverage Of Cell List"
new_folder_string = "/Calc Tables/"
tot_col_rat = "Total Colocolized Ratio"
ner_col_rat = "nER Colocalization Ratio"
cer_col_rat = "cER Colocalization Ration"
not_col_rat = "Not Colocalized Ratio"
ava_org_cov = "Average Organelle Coverage"
title_order = [total_mrna, tot_col_rat, not_col_rat, ner_col_rat, cer_col_rat]


def main():
    tables_folder_path = filedialog.askdirectory(initialdir = '', title = "Where are your files?", mustexist = True)
    my_strain_dic = calc_tables(tables_folder_path)
    #statistics_table(tables_folder_path)
    statistics_table(tables_folder_path + new_folder_string, my_strain_dic)
    
    return f"Tables saved in {tables_folder_path + new_folder_string}"
    

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
    print(strain_dic.keys()) 
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


main()