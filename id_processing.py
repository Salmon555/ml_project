import pandas as pd
import os


def sort_str(string: str):  # sorting the string like "10-11-204-205-39-40"
    lis = string.split("-")
    lis = sorted(lis)
    output = ""
    for i in lis:
        output += i + "-"
    return output[:-1]


def id_processing(id):
    output = "10-11-39-40-"  # "10-11-39-40" exist in every row
    id_list = id.split("-")
    prefix = id_list[0]
    if "FAK" in prefix:
        output += "502-503-"
    id_list = id_list[1:]
    if "WSC" in id and "X" in id:
        output += "490-491-"
    if "RS" == prefix[0:2]:
        output += "32-33-"
    for index, string in enumerate(id_list):
        if "NSC" in string:
            output += "202-203-"
        else:
            if "SC" in string and "WSC" not in string:
                output += "430-431-"
        if "SX" in string:
            output += "444-445-"
        if "LFC" in string:
            output += "366-367-"
        if "Y" in string:
            output += "488-489-"
        if "RC" in string:
            output += "424-425-"
        if "KC" in string:
            output += "344-345-"
        if "MF" in string:
            output += "372-373-"
        if "WF" in string:
            output += "478-479-"
        if "A" in string:
            if index == len(id_list) - 1:
                output += "310-311-"
            else:
                if "E" in id_list[index + 1]:
                    output += "480-481-"
                else:
                    output += "310-311-"
        if "H" in string and "H" in prefix:
            output += "506-507-"
    return output


def time_order(input: list):  # Transforming the status into a status_time_sequence
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(cur_dir, 'time_order.csv')

    output = ""
    for i in input:
        output += i + "-"
    output = sort_str(output[:-1])  # Making it a sorted_str

    time = pd.read_csv(file_path)
    temp_list = list(time["pro_status_cd"])
    temp_dic = {}
    for i in temp_list:
        temp_dic[i] = temp_dic.get(i, 0) + 1

    final_dic = {}  # The key is the sorted string, the values is a list, the first element is the most popular status chronologically
    # The second element is the number of its apperance.
    for key, values in temp_dic.items():
        # Preserving two biggest number
        final_dic[sort_str(key)] = [["", 0], ["", 0]]
    for key, values in temp_dic.items():
        if final_dic[sort_str(key)][0][1] <= final_dic[sort_str(key)][1][1]:
            if final_dic[sort_str(key)][0][1] <= values:
                final_dic[sort_str(key)][0] = [key, values]
        else:
            if final_dic[sort_str(key)][1][1] <= values:
                final_dic[sort_str(key)][1] = [key, values]
    if output in final_dic.keys():
        output = [final_dic[output][0][0], final_dic[output][1][0]]
    return output

    # output is a list of str


def machine_type(string: str):  # Output the machine-type in time order
    list_of_status = string.split("-")
    output = ""
    machine_type8_list = ["444", "366", "488", "424"]
    machine_type10_list = ["502", "506", "344", "372", "478"]
    machine_type8and10_list = ["430", "490", "480", "310", "12"]
    for status in list_of_status:
        if status == "3":
            output += "1- "
        elif status == "5":
            output += "2- "
        elif status == "200":
            output += "3- "
        elif status == "202":
            output += "4- "
        elif status == "204":
            output += "5- "
        elif status in machine_type8_list:
            output += "8- "
        elif status in machine_type10_list:
            output += "10- "
        elif status in machine_type8and10_list:
            output += "8or10- "
    return output[:-1]


def product_id_to_size(input_: str):
    list_ = input_.split("-")
    d_size, l_size = "", ""
    for word in list_:
        if d_size == "":
            for char in word:
                if char.isdigit() == True:
                    d_size += char
        else:
            if l_size == "":
                for char in word:
                    if char.isdigit() == True:
                        l_size += char
            else:
                break
    d_size = int(d_size)
    l_size = int(l_size)
    return [d_size, l_size]
