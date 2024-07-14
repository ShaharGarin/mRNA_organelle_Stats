import numpy as np
from scipy import stats
import ast

#Calc localization precentages from two columns
def calc_loc_ratio(column1, column2):
    ratio_list = []
    for cell in range(len(column1)):
        if column1[cell] == 0:
            ratio_list.append(0)
        else:
            ratio_list.append(column2[cell]/column1[cell])
    return ratio_list

#Calc complementary ratio
def calc_comp_ratio(column):
    diff_list = []
    for cell in range(len(column)):
        diff_list.append(1 - column[cell])
    return diff_list


#Calc avarage of lists in column
def calc_ave_cov(column):
    cov_list = []
    for cell in column:
        list_cell = ast.literal_eval(cell)
        cov_list.append(sum(list_cell)/len(list_cell))
    
    return cov_list

#Calc avarages and standard error of whole column
def calc_col_ava(column):
    return [np.mean(column), stats.sem(column)]