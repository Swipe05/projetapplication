from multiprocessing import Condition
import sqlite3


class Data_base:
    def __init__(self, name = 'LMHT.db') -> None:
        
        try:
            print('===================================================================================')
            # Connect to DB and create a cursor
            self.sqliteConnection = sqlite3.connect(name)
            self.cursor = self.sqliteConnection.cursor()
            print('DB Init')

            # Write a query and execute it with cursor
            query = 'select sqlite_version();'
            self.cursor.execute(query)

            # Fetch and output result
            result = self.cursor.fetchall()
            print('SQLite Version is {}'.format(result))

            # Close the cursor
            #self.cursor.close()

            print('===================================================================================')

        # Handle errors
        except sqlite3.Error as error:
            print('Error occured - ', error)


    #create table
    # if data type is text ===> "VARCHAR(255)" 
    def create_table(self,table_name,  table_columns):
        #check if table exists
        listOfTable = self.cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; """).fetchall()
        if listOfTable: #if listOfTable == []: 
            print('Table existes')
            return False
        query = f""" CREATE TABLE {table_name} ( """
        count = 1
        for element in table_columns.items():
            if count < len(table_columns):
                query += f""" {element[0]}   {element[1]} ,"""
                count += 1
            else:
                query += f""" {element[0]}   {element[1]} """

        query += ''');'''
        self.cursor.execute(query)
    # insert values into the table by reordering the names of the columns 
    # ex: insert_data_with_columns_names("TEST_TABLE", {'name':'Maxime', 'age':'10', 'score':'18.5'})
    def insert_data_with_columns_names(self,table_name, dict_data):
        query = f'''INSERT INTO {table_name} ('''
        list_key = []
        list_value = []
        for ele in dict_data.items():
            list_key.append(ele[0])
            list_value.append('"'+ele[1]+'"')
        query = query + ",".join(list_key) + ') VALUES ('  + ",".join(list_value) + ");"
        print(query)
        self.cursor.execute(query)
        self.sqliteConnection.commit()
    #ex: insert_data_without_column_name("TEST_TABLE", ['Phuong','35','19.999999'])
    def insert_data_without_column_name(self, table_name, list_data):
        query = f'''INSERT INTO {table_name} VALUES ('''
        list_donne = [f'"{x}"' for x in list_data]
        query = query  + ','.join(list_donne) + ');'
        print(query)
        self.cursor.execute(query)
        self.sqliteConnection.commit()
    #ex:  delete_row("TEST_TABLE","name = 'Cong Khai'")
    def delete_row(self, table_name,condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        print(query)
        self.cursor.execute(query)
        self.sqliteConnection.commit()
    #ex: select_all_data("TEST_TABLE")
    def select_all_data(self, table_name):
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
    #ex: args = columns to display
    def select_data_with_condition(self, table_name,condition ,*args):
        data = []
        query = "SELECT "
        if len(args) == 0:
            query += "*"
        else:
            query += ','.join(*args)
        query = query + f" FROM {table_name} WHERE" + condition  + ';'
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
        #check if table exists
        listOfTable = self.cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; """).fetchall()
        if listOfTable: #if listOfTable == []: 
            print('Table existes')
            return
        query = f"DROP TABLE {table_name}"
        self.cursor.execute(query)
    # dict_change = {"column":"new_val"}
    # Following is an example, which will update ADDRESS for a customer whose ID is 6.
    # UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
    def update_data(self,tabel_name, condition, dict_change):
        query = f"UPDATE {tabel_name} SET "
        con = [f"{x}={y}" for x,y in dict_change.items()]
        query += ','.join(con)
        query += f" WHERE {condition} ;"
        print(query)
    '''
    UPDATE table_name
SET column1 = value1, column2 = value2...., columnN = valueN
WHERE [condition];
    '''  

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

lmht_db = Data_base()
## table_column={'name':"varchar(255)", 'age':"INTEGER", 'score':"REAL"}
## lmht_db.create_table("TEST_TABLE", table_column)
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Maxime', 'age':'10', 'score':'18.0'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Esteban', 'age':'19', 'score':'19.5'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Leo', 'age':'30', 'score':'20.1'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Cong Khai', 'age':'21', 'score':'19.99'})
# lmht_db.insert_data_without_column_name("TEST_TABLE", ['Phuong','35','19.999999'])
# lmht_db.delete_row("TEST_TABLE","name = 'Cong Khai'")
# lmht_db.select_all_data("TEST_TABLE")
# print(lmht_db.select_data_with_condition("TEST_TABLE", " age = 19 ", ("name","age")))
## table2_column = {'name':'varchar(255)', 'game':'varchar(255)', 'champ':'varchar(255)'}
# lmht_db.create_table("TEST_TABLE2", table2_column)
# lmht_db.insert_data_with_columns_names("TEST_TABLE2", {'name':'Maxime', 'game':'LOL', 'champ':'Camille'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE2", {'name':'Leo', 'game':'Valorant', 'champ':'Raze'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE2", {'name':'Esteban', 'game':'Valorant', 'champ':'Yoru'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE2", {'name':'Cong Khai', 'game':'LOL', 'champ':'Garen'})
# print(lmht_db.join('TEST_TABLE','TEST_TABLE2','TEST_TABLE.name=TEST_TABLE2.name',('TEST_TABLE.name','age','game')))
lmht_db.update_data("123","id>6" ,{"ADDRESS":'texas'})