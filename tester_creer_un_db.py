from matplotlib.pyplot import table
from interact_with_db import Data_base



pseudo = ["maxuka", "EsayPotato","Swipe"]
liste_col = ["ID","Kill","Death","Assist"]
liste_final_max = [[10,1,2,3],[11,10,0,1],[12,8,7,5],[13,1,15,9],[14,4,4,7]]
liste_final_EP = [[20,1,1,3],[21,0,4,4],[23,10,0,1],[24,11,11,13],[25,1,0,19]]
liste_final_sw = [[30,1,1,1,],[31,2,2,2],[32,1,18,19],[33,9,0,17],[34,1,1,17],[33,0,0,0]]
liste_final = [liste_final_max,liste_final_EP,liste_final_sw]

def main():
    lmht_database = Data_base("test_database.db")
    for o in range(len(pseudo)):
        lmht_database.create_table(pseudo[o],liste_col, "ID") 
        for ele in liste_final[o]:
            lmht_database.insert_data_without_column_name(pseudo[o], ele)
    tables = lmht_database.list_all_table()
    print(tables)
    for i in tables:
        # lmht_database.select_all_data(i[0])
        # print(f'\n================================={pseudo[tables.index(i)]}=========================================\n\n')
        lmht_database.print_table_form_get_dict(i[0])



if __name__ == "__main__":
    main()