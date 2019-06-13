import pandas as pd

status = pd.read_csv('D:\\summer_python\\0607\\6.01_withseq.csv')  # read files
status = status[["in_prod_name", "pro_status_cd"]]

status["status_list"] = status["pro_status_cd"].apply(lambda x: x.split("-"))
status["status_list"] = status["status_list"].astype(list)


def create_type(name: str):
    status[name] = status["status_list"].apply(lambda x: name in x)
    status[name] = status[name].astype(int)


new_category_name = ["3", "5", "12", "200", "202", "204"]

for name in new_category_name:
    create_type(name)

# creating new category

status["202"] = status["202"] * 2
status["204"] = status["204"] * 4

status["category"] = status["200"] + status["202"] + status["204"]

status = status.drop(["200", "202", "204"], axis=1)  # drop useless columns
status["no_numbers"] = status["in_prod_name"].apply(
    lambda x: re.sub('[0-9]', '', str(x)))
status["no_numbers"] = status["no_numbers"].apply(
    lambda x: re.sub('/.', '', str(x)))

status.to_csv("./data.csv")  # save data
