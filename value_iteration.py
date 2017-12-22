"""
Loads parameters for transition probability and reward of 3-state problem,
and calculates optimal policy by value iteration.

Requires:

- xlsx file(probability_and_reward.xlsx) on the same location as this .py file
- Pandas package(with dependency satisfied)

Dec. 23. 2017 by JuneTech
"""

import pandas as pd
import numpy as np

def read_xlsx_file(file_name):
    """
    Reads xlsx file and returns a dictionary containing four dataframes
    """
    ord_dict_df = pd.read_excel(file_name, sheet_name=None)
    return ord_dict_df

def posb_action_state():
    """
    Returns possible action choice for each state
    """
    return {'s': ['slow', 'fast'], 'm': ['slow', 'fast'], 'f': ['slow']}

def make_param_df(param_df_dict, policy):
    """
    make Dataframe of parameter(probability/reward) according to policy
    input: dictionary of parameter dataframe(key: policy, value: dataframe), policy
    """
    current_state_list = list(param_df_dict[policy['s']])
    param_df = pd.DataFrame(columns=current_state_list)
    for key, value in policy.items():
        param_df[key] = param_df_dict[value][key]
    return param_df

def df_into_npm(df_):
    """
    convert dataframe into matrix
    - omit headers
    - inverse
    """
    tp_matrix = []
    for param_list in df_:
        tp_matrix.append(df_[param_list])
    return np.asmatrix(tp_matrix)

def max_action_value(state, value_col):
    max_value = -256
    max_action = None
    for action in posb_action_state()[state]:
        compared_value = 0
        compared_prob = PROB_PARAM_DF_DICT[action][state]
        compared_reward = REWARD_PARAM_DF_DICT[action][state]
        for i in range(len(compared_prob)):
            compared_value += compared_prob[i]*compared_reward[i]
            compared_value += DELTA * compared_prob[i]*value_col[i, 0]
        #print(compared_prob, '\n', compared_reward, '\n', compared_value, action, '\n')
        if max_value < compared_value:
            max_value = compared_value
            max_action = action
    return max_action, max_value

def value_iterate(value_col, iterate_num):
    """
    value iteration with initial value as zero for all states
    """
    iterate_num += 1

    #print(iterate_num, value_col)

    next_value_list = []
    action_list = {}
    for state in STATE_LIST:
        that_action, next_value = max_action_value(state, value_col)
        next_value_list.append(next_value)
        action_list[state] = that_action
    next_value_col = np.asmatrix(next_value_list).transpose()

    #print(next_value_list, action_list)
    #print(next_value_col - value_col)
    ## termination condition
    if np.linalg.norm(next_value_col - value_col) < (EPSILON*(1-DELTA))/(2*DELTA):
        return next_value_col, action_list, iterate_num
    return value_iterate(next_value_col, iterate_num)

def initial_value():
    """
    makes matrix of initial value
    """
    value_list = []
    for i in range(len(STATE_LIST)):
        value_list.append(0)
    return np.asmatrix(value_list).transpose()

PROB_PARAM_DF_DICT = read_xlsx_file("probability_param.xlsx")
REWARD_PARAM_DF_DICT = read_xlsx_file("reward_param.xlsx")
DELTA = 0.7
EPSILON = 0.1
ITERATE_NUM = 0

STATE_LIST = [header for header in PROB_PARAM_DF_DICT['slow']]

opt_value_col, opt_policy, total_iterations = value_iterate(initial_value(), ITERATE_NUM)

print(opt_value_col, opt_policy, total_iterations)
