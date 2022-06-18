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
    #kwargs = {"column's name":"data type"}
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


lmht_db = Data_base()
table_column={'name':"varchar(255)", 'age':"INTEGER", 'score':"REAL"}
lmht_db.create_table("TEST_TABLE", table_column)
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Maxime', 'age':'10', 'score':'18.0'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Esteban', 'age':'19', 'score':'19.5'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Leo', 'age':'30', 'score':'20.1'})
# lmht_db.insert_data_with_columns_names("TEST_TABLE", {'name':'Cong Khai', 'age':'21', 'score':'19.99'})
# lmht_db.insert_data_without_column_name("TEST_TABLE", ['Phuong','35','19.999999'])
# lmht_db.delete_row("TEST_TABLE","name = 'Cong Khai'")
# lmht_db.select_all_data("TEST_TABLE")
print(lmht_db.select_data_with_condition("TEST_TABLE", " age = 19 ", ("name","age")))