import numpy as np
import pandas as pd

def read_xlsx_file(file_name):
    """
    Reads xlsx file and returns a dictionary containing four dataframes
    """
    ord_dict_df = pd.read_excel(file_name, sheetname=None)
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
    current_state_list = list(param_df_dict['slow'])
    param_df = pd.DataFrame(columns = current_state_list)
    for key, value in policy.items():
        param_df[key] = param_df_dict[value][key]
    print(param_df)
    return param_df


PROB_PARAM_DF_DICT = read_xlsx_file("probability_param.xlsx")
REWARD_PARAM_DF_DICT = read_xlsx_file("reward_param.xlsx")

POLICY_LIST = list_of_md_policy(posb_action_state())

prob_df = make_param_df(PROB_PARAM_DF_DICT, POLICY_LIST[0])
reward_df = make_param_df(REWARD_PARAM_DF_DICT, POLICY_LIST[0])
