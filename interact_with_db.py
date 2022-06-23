import sqlite3



class Data_base:
    def __init__(self, name='LMHT.db') -> None:

        try:
            print('===================================================================================')
            # Connect to DB and create a cursor
            self.sqliteConnection = sqlite3.connect(name,check_same_thread=False)
            self.cursor = self.sqliteConnection.cursor()
            print('DB Init')

            # Write a query and execute it with cursor
            query = 'select sqlite_version();'
            self.cursor.execute(query)

            # Fetch and output result
            result = self.cursor.fetchall()
            print('SQLite Version is {}'.format(result))

            # Close the cursor
            # self.cursor.close()

            print('===================================================================================')

        # Handle errors
        except sqlite3.Error as error:
            print('Error occured - ', error)

    # create table
    # if data type is text ===> "VARCHAR(255)"
    def name_with_espace(self, name):
        return name.replace(" ","_es_")
    def create_table(self, table_name, table_columns, primary_key=""):
        table_name = self.name_with_espace(table_name)
        # check if table exists
        listOfTable = self.cursor.execute(
            f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; """).fetchall()
        if listOfTable:  # if listOfTable == []:
            print('Table existes')
            return False
        query = f""" CREATE TABLE {table_name} ( """
        count = 1
        if type(table_columns) == list:
            for ele in table_columns:
                if count < len(table_columns):
                    query += f''' [{ele}]  VARCHAR(255) , '''
                    count += 1
                else:
                    query += f'''[{ele}] VARCHAR(255)'''
        elif type(table_columns) == dict:
            for element in table_columns.items():
                if count < len(table_columns):
                    query += f""" [{element[0]}]   {element[1]} ,"""
                    count += 1
                else:
                    query += f""" [{element[0]}]   {element[1]} """
        if primary_key != "":
            if type(primary_key) == list or type(primary_key) == tuple:
                query += ", PRIMARY KEY ( "
                for key in primary_key:
                    if primary_key.index(key) == len(primary_key) - 1:
                        query += f" [{key}] )  "
                    else:
                        query += f" [{key}], "
            if type(primary_key) == str:
                query += f" , PRIMARY KEY ({primary_key})  "

        query += ''');'''
        print(query)
        self.cursor.execute(query)

    # insert values into the table by reordering the names of the columns
    # ex: insert_data_with_columns_names("TEST_TABLE", {'name':'Maxime', 'age':'10', 'score':'18.5'})
    def insert_data_with_columns_names(self, table_name, dict_data):
        table_name = self.name_with_espace(table_name)
        try:
            query = f'''INSERT INTO {table_name} ('''
            list_key = []
            list_value = []
            for ele in dict_data.items():
                list_key.append("[" + ele[0] + "]")
                list_value.append('"' + ele[1] + '"')
                # print("ele is ", ele)
            query = query + ",".join(list_key) + ') VALUES (' + ",".join(list_value) + ");"
            print(query)
            self.cursor.execute(query)
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print("error is  ",error)
            pass

    # insert data to table
    def insert_multi_row_with_column_name(self, table_name, dict_data):
        table_name = self.name_with_espace(table_name)
        try:
            ele_dict = {}
            list_columns = list(dict_data.keys())
            list_value = list(dict_data.values())
            if type(list_value[0]) != int:
                # print("list value = ", list_value)
                # print("list columns = ", list_columns)
                ele_dict[list_columns[0]] = list_value[0]
                for i in range(1,len(list_value[1])):
                    for j in range(1,len(list_columns)):
                        try:
                            ele_dict[list_columns[j]] = str(list_value[j][i])
                        except Exception as e:
                            print(f" {i}  {j} ")
                            print(list_value)
                            print(list_columns)
                            print(e)
                    self.insert_data_with_columns_names(table_name, ele_dict)
            else:
                for j in range(len(list_columns)):
                    ele_dict[list_columns[j]] = str(list_value[j])
                self.insert_data_with_columns_names(table_name, ele_dict)

        except sqlite3.Error as error:
            # print(error)
            pass

    # ex: insert_data_without_column_name("TEST_TABLE", ['Phuong','35','19.999999'])
    def insert_data_without_column_name(self, table_name, list_data):
        table_name = self.name_with_espace(table_name)
        try:
            query = f'''INSERT INTO {table_name} VALUES ('''
            list_donne = [f'"{x}"' for x in list_data]
            query = query + ','.join(list_donne) + ');'
            print(query)
            self.cursor.execute(query)
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            # print("error  is   ", error)
            pass

    # ex:  delete_row("TEST_TABLE","name = 'Cong Khai'")
    def delete_row(self, table_name, condition):
        table_name = self.name_with_espace(table_name)
        query = f"DELETE FROM {table_name} WHERE {condition}"
        print(query)
        self.cursor.execute(query)
        self.sqliteConnection.commit()

    # ex: select_all_data("TEST_TABLE")
    def select_all_data(self, table_name):
        table_name = self.name_with_espace(table_name)
        data = []
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        print(f"-------------------------------all data of {table_name}-------------------------------------")
        output = self.cursor.fetchall()
        for row in output:
            data.append(row)
            print(row)
        self.sqliteConnection.commit()
        print("---------------------------------------------------------------------------------------------")
        return data

    def print_table_form_get_dict(self, table_name):
        table_name = self.name_with_espace(table_name)
        tab = {}
        data = self.cursor.execute(f'''SELECT * FROM {table_name}''')
        cols = []
        for col in data.description:
            tab[col[0]] = []
            cols.append(col[0])
        for row in data:
            for i in range(len(row)):
                tab[cols[i]].append(row[i])
        # print(tab)
        print(f_string_table(tab))
        return tab

    # ex: args = columns to display
    def select_data_with_condition(self, table_name, condition, *args):
        table_name = self.name_with_espace(table_name)
        data = []
        query = "SELECT "
        if len(args) == 0:
            query += "*"
        else:
            query += ','.join(*args)
        query = query + f" FROM {table_name} WHERE" + condition + ';'
        print(query)
        self.cursor.execute(query)
        output = self.cursor.fetchall()
        print(f"-----------------------{args} of {table_name} WHERE {condition}------------------------------")
        for row in output:
            data.append(row)
            print(row)
        print("----------------------------------------------------------------------------------------------")
        return data

    # args = selected columns
    # on_clase example: ON TEST_TABLE.name=TEST_TABLE2.name
    # ex: join('TEST_TABLE','TEST_TABLE2','TEST_TABLE.name=TEST_TABLE2.name',('TEST_TABLE.name','age','game'))
    def join(self, table1, table2, on_clause, *args):
        data = []
        query = "SELECT " + ','.join(*args) + f" FROM {table1} INNER JOIN {table2} ON {on_clause};"
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            data.append(row)
            print(row)
        return data

    def drop_table(self, table_name):
        table_name = self.name_with_espace(table_name)
        # check if table exists
        listOfTable = self.cursor.execute(
            f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; """).fetchall()
        if listOfTable:  # if listOfTable == []:
            print('Table existes')
            query = f"DROP TABLE {table_name}"
            self.cursor.execute(query)
            return


    # dict_change = {"column":"new_val"}
    # Following is an example, which will update ADDRESS for a customer whose ID is 6.
    # UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
    def update_data(self, tabel_name, condition, dict_change):
        query = f"UPDATE {tabel_name} SET "
        con = [f"{x}='{y}'" for x, y in dict_change.items()]
        query += ','.join(con)
        query += f" WHERE {condition} ;"
        print(query)
        self.cursor.execute(query)

    def list_all_table(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        lsi_t = self.cursor.fetchall()
        return lsi_t

    # create and add data to a table
    def read_data_from_a_dict(self, dictionary, name="partie", primary_key="timestamp", table_all_name = "all_summoner"):
        list_keys = list(dictionary.keys())
        list_values = list(dictionary.values())
        print("list key = ", list_keys)
        print("lsit values = ", list_values)
        self.create_table(name, list_keys, primary_key)
        self.create_table(table_all_name,["summonerName"] ,primary_key = "summonerName")
        self.insert_data_with_columns_names(table_all_name,{"summonerName":dictionary.get("summonerName")})
        self.insert_multi_row_with_column_name(name, dictionary)
        # self.insert_data_with_columns_names(dictionary.get(name),dictionary)
        # print(f'{list_keys} \n {list_values}')

    '''
    UPDATE table_name
    SET column1 = value1, column2 = value2...., columnN = valueN
    WHERE [condition];
    '''

    def list_columns(self,table_name):
        table_name = self.name_with_espace(table_name)
        cols = []
        self.cursor.execute(f"SELECT * FROM {table_name}")
        for col in self.cursor.description:
            cols.append(col[0])
        return cols
    def add_column(self, table_name, column_name):
        table_name = self.name_with_espace(table_name)
        col_name = str(column_name)
        query = f"ALTER TABLE {table_name} ADD COLUMN {col_name} varchar(255);"
        self.cursor.execute(query)


#######################################################################################################################
'''
PREDEFINED FUNCTIONS
create_table(self,table_name,  table_columns)
dinsert_data_with_columns_names(self,table_name, dict_data)
insert_data_without_column_name(self, table_name, list_data)
delete_row(self, table_name,condition)
select_all_data(self, table_name)
select_data_with_condition(self, table_name,condition ,*args)
join(self, table1, table2, on_clause, *args)
'''


#######################################################################################################################


##########################################################################################################################


###Table printing functions###

def f_table_length(d):
    if d == {}:
        return 0
    myIter = (iter(d))
    n = len(d[next(myIter)])
    for att in myIter:
        assert n == len(d[att]), f"Table with inconsistent lengths! {att} is {len(d[att])} instead of {n}"
    return n


def f_string_val(x, lim=20):
    s = f"{x}"
    if len(s) > lim:
        return s[:7] + "..."
    else:
        return f"{s: >{lim}}"


def f_string_line(d, i, ord=None, lim=20):
    if ord is None:
        ord = d
    s = "|"
    for att in ord:
        s = s + f_string_val(d[att][i], lim) + "|"
    return s


def f_string_title(d, ord=None, lim=20):
    if ord is None:
        ord = d
    s = "|"
    for att in ord:
        s = s + f_string_val(att, lim) + "|"
    s = s + "\n" + "+"
    for att in ord:
        s = s + "-" * (lim) + "+"
    return s


def f_string_table(d, ord=None, lim=20):
    if ord is None:
        ord = d
    s = f_string_title(d, ord, lim) + "\n"
    n = f_table_length(d)
    for i in range(n):
        s = s + f_string_line(d, i, ord, lim) + "\n"
    return s