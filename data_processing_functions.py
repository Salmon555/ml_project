def txt_to_dictionary(name) -> dict:
    dic={}
    file = open(name+'.txt','r')


    for line in file.readlines():
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        list_ = v.split(",") 
        dic[k] = list_

    file.close()
    return dic


def get_intersection(listA: list,listB: list):
	Rlist = []
	for i in listA:
		if i in listB:
			Rlist.append(i)
	return Rlist

def list_to_string(listA: list) -> str:
	output="("
	for i in listA:
		output += i+","
	return output[:-1]+")"

def machine_sequence_to_machine_name(string: str, cd1:int, cd2:int) -> str:
	size_dic = txt_to_dictionary("machine_type_dic")
	machine_sizename_list = []
	if cd1 == 1:
		machine_sizename_list += size_dic["mac1_low"]
	elif cd1 == 2:
		machine_sizename_list += size_dic["mac1_medium"]
	elif cd1 == 3:
		machine_sizename_list += size_dic["mac1_high"]
	if cd2 == 1:
		machine_sizename_list += size_dic["mac2_low"]
	elif cd2 == 2:
		machine_sizename_list += size_dic["mac2_medium"]
	elif cd2 == 3:
		machine_sizename_list += size_dic["mac2_high"]


	dic = txt_to_dictionary("machine_usage_type_dic_")
	output = ""
	list_= string.split("-")
	for i in list_:
		machine_list = []
		num = i.split("(")[0]
		if num[0] == " ":
			num = num[1:]
		if num == "8or10":
			machine_list = dic["8"] + dic ["10"]
		else:
			machine_list = dic[num]
		intersection = get_intersection(machine_list,machine_sizename_list)
		if intersection == []:
			intersection = machine_list
		output += list_to_string(intersection) + "-"

	return output[:-1]

def status_to_usefulstatus(string: str) -> str:
	output = ""
	list_ = string.split("-")
	for i in list_:
		if i in ["3","5","200","202","204","444", "366", "488", "424","502", "506", "344", "372", "478","430", "490", "480", "310", "12"]:
			output += i+"-"
	return output[:-1]