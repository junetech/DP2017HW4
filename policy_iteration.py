"""
Loads parameters for transition probability and reward of 3-state problem,
and calculates optimal policy by policy iteration.

Requires:

- xlsx file(probability_and_reward.xlsx) on the same location as this .py file
- Pandas package(with dependency satisfied)

Dec. 21. 2017 by JuneTech
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

def list_of_md_policy(posb_action_dict):
    """
    Returns all combination of markovian deterministic policies
    """
    state_list = []
    action_list = []
    for key, value in posb_action_dict.items():
        state_list.append(key)
        action_list.append(value)

    policy_ea = 1
    for state_list in action_list:
        policy_ea = policy_ea * len(state_list)

    policy_list = [{} for i in range(policy_ea)]

    policy_list = [{'s': 'slow', 'm': 'slow', 'f': 'slow'}, {'s': 'slow', 'm': 'fast', 'f': 'slow'}, {'s': 'fast', 'm': 'slow', 'f': 'slow'}, {'s': 'fast', 'm': 'fast', 'f': 'slow'}]
    return policy_list

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

def I_delta_P_inverse(param_mat):
    """
    calculates inverse of (identity - delta*probability matrix)
    """
    num_states = len(param_mat)
    IdP = np.identity(num_states) - DELTA * param_mat
    return IdP.getI()

def reward_vector(prob_mat, reward_mat):
    """
    returns reward vector for given policy
    """
    state_num = len(prob_mat)
    reward = [0 for i in range(state_num)]
    for i in range(state_num):
        for j in range(state_num):
            reward[i] += prob_mat[i, j] * reward_mat[i, j]
    reward = np.matrix(reward).transpose()
    return reward

def arg_max_policy(current_value):
    """
    returns policy that has the arg max supremum norm of value matrix
    """
    max_value = -256
    max_policy = None
    for policy in POLICY_LIST:
        prob_df = make_param_df(PROB_PARAM_DF_DICT, policy)
        reward_df = make_param_df(REWARD_PARAM_DF_DICT, policy)
        prob_mat = df_into_npm(prob_df)
        reward_mat = df_into_npm(reward_df)
        policy_value = reward_vector(prob_mat, reward_mat) + DELTA * np.matmul(prob_mat, current_value)
        # supremum norm
        if policy_value.max() > max_value:
            max_value = policy_value.max()
            max_policy = policy
    return max_policy

def policy_iterate(current_policy, iterate_num):
    """
    policy iteration with initial policy as the 1st policy among list
    """
    iterate_num += 1

    prob_df = make_param_df(PROB_PARAM_DF_DICT, current_policy)
    reward_df = make_param_df(REWARD_PARAM_DF_DICT, current_policy)
    prob_mat = df_into_npm(prob_df)
    reward_mat = df_into_npm(reward_df)
    current_value = np.matmul(I_delta_P_inverse(prob_mat), reward_vector(prob_mat, reward_mat))

    next_policy = arg_max_policy(current_value)

    print(current_value)
    if next_policy == current_policy: 
        return current_policy, iterate_num
    return policy_iterate(next_policy, iterate_num)

PROB_PARAM_DF_DICT = read_xlsx_file("probability_param.xlsx")
REWARD_PARAM_DF_DICT = read_xlsx_file("reward_param.xlsx")
DELTA = 0.7
POLICY_LIST = list_of_md_policy(posb_action_state())
ITERATE_NUM = 0

print(policy_iterate(POLICY_LIST[0], ITERATE_NUM))
