from mariaDB import *


pseudo = ["maxuka", "EsayPotato","Swipe"]
liste_col = ["ID","0Kill","123Death","Assist"]
liste_final_max = [[10,1,2,3],[11,10,0,1],[12,8,7,5],[13,1,15,9],[14,4,4,7]]
liste_final_EP = [[20,1,1,3],[21,0,4,4],[23,10,0,1],[24,11,11,13],[25,1,0,19]]
liste_final_sw = [[30,1,1,1,],[31,2,2,2],[32,1,18,19],[33,9,0,17],[34,1,1,17],[33,0,0,0]]
liste_final = [liste_final_max,liste_final_EP,liste_final_sw]

dict_data_max = {"summonerName":"max lz","123ID":[10,11,12,13,14],"Kill":[1,10,8,1,4],"Death":[2,0,7,15,4],"Assist":[3,1,5,9,7]}

dict_data_max_update = {"summonerName":"max","123ID":[15,16,17,18,19],"Kill":[11,1,6,0,0],"Death":[0,0,0,1,4],"Assist":[3,6,5,9,7]}

dict_data_max_update1 = {"summonerName":"max","123ID":[20,21,22,23,24],"Kill":[11,1,6,0,0],"Death":[0,0,0,1,4],"Assist":[3,6,5,9,7]}

dict_data_max_update2 = {"summonerName":"max","123ID":[25,26,27,28,29],"Kill":[11,1,6,0,0],"Death":[0,0,0,1,4],"Assist":[3,6,5,9,7]}

dict_data_max_update3 = {"summonerName":"max","123ID":[30,31,32,33,34],"Kill":[11,1,6,0,0],"Death":[0,0,0,1,4],"Assist":[3,6,5,9,7]}
dict_data_EP = {"summonerName":"EasyPotato","123ID":[35,36,37,38,39],"Kill":[1,0,10,11,1],"Death":[1,4,0,11,0],"Assist":[3,4,1,13,19]}
dict_data_sw = {"summonerName":"Swipe","123ID":[304,314,324,334,344],"Kill":[1,2,1,9,1],"Death":[1,2,18,0,1],"Assist":[1,2,19,17,17]}
def main():
    lmht = Data_base()
    # for o in range(len(pseudo)):
    #     lmht.create_table(pseudo[o],liste_col, "ID") 
    #     for ele in liste_final[o]:
    #         lmht.insert_data_without_column_name(pseudo[o], ele)
    # tables = lmht.list_all_table()
    # print(tables)
    # for i in tables:
    #     # lmht.select_all_data(i[0])
    #     # print(f'\n================================={pseudo[tables.index(i)]}=========================================\n\n')
    #     lmht.print_table_form_get_dict(i[0])
    lmht.read_data_from_a_dict(dict_data_max,primary_key="col_123ID")
    lmht.read_data_from_a_dict(dict_data_max_update, primary_key="col_123ID")

    lmht.read_data_from_a_dict(dict_data_max_update1, primary_key="col_123ID")

    lmht.read_data_from_a_dict(dict_data_max_update2, primary_key="col_123ID")

    lmht.read_data_from_a_dict(dict_data_max_update3, primary_key="col_123ID")
    lmht.read_data_from_a_dict(dict_data_EP, primary_key="col_123ID")
    lmht.read_data_from_a_dict(dict_data_sw, primary_key="col_132ID")
    



if __name__ == "__main__":
    main()