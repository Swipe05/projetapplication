# abcd = {"xs":1,"ds":2,"dcs":3}
# for i in abcd.items():
#     print(i[0])
#     print(i[1])

def create_table(table_name,  **kwargs):
    query = f""" CREATE TABLE {table_name} ( """
    count = 1
    for element in kwargs.items():
        print("element  ", element)
        if count < len(kwargs):
            query += f""" {element[0]}   {element[1]} ,"""
            count += 1
        else:
            query += f""" {element[0]}   {element[1]} """

    query += ''');'''
    return query

print(create_table("TEST-Table",c1="123",c2="456",c3="789"))


def insert_data_with_columns_names(table_name, dict_data):
    query = f'''INSERT INTO {table_name} ( '''
    list_key = []
    list_value = []
    for ele in dict_data.items():
        list_key.append(ele[0])
        list_value.append(ele[1])
    query = query + ",".join(list_key) + ' ) VALUES ( ' + ",".join(list_value) + ");"
    return query

print(insert_data_with_columns_names("TEST-Table", {"STUDENT":"name","id":"113","hub":"bro"}))