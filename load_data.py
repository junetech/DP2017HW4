"""
Loads parameters for transition probability and reward of 3-state problem.

Requires:

- xlsx file(probability_and_reward.xlsx) on the same location as this .py file
- Pandas package(with dependency satisfied)

Dec. 21. 2017 by JuneTech
"""

import pandas as pd

def read_xlsx_file(file_name):
    """
    Reads xlsx file and returns a dictionary containing four dataframes
    """
    return pd.read_excel(file_name, sheetname=None)

'''
for key, value in read_xlsx_file("probability_and_reward.xlsx"):
    print(value)
'''

param_df_dict = read_xlsx_file("probability_and_reward.xlsx")

print(param_df_dict)
print(param_df_dict['slow_prob'])
