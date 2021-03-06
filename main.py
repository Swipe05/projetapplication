import time

from riotwatcher import LolWatcher
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from requests.exceptions import HTTPError
from datetime import datetime
import os
import webbrowser
import random

import asyncio

from calendar_DB import *
from threading import Thread
from datetime import datetime
from mariaDB import *
from variable import every
import time
import matplotlib.pyplot as plt
import customtkinter as ctkp



dict_champions = {'Aatrox':0, 'Ahri':1 ,'Akali':1 , 'Akshan':0,'Alistar':0,'Amumu':0, 'Anivia':1, 'Annie':1, 'Aphelios':0, 'Ashe':1, 'AurelionSol':0, 'Azir':0 ,'Bard':0, 'Belveth':1,'Blitzcrank':0, 'Brand':0,'Braum':0,'Caitlyn':1,'Camille':1 ,'Cassiopeia':1 ,'Chogath':0, 'Corki':0, 'Darius':0,'Diana':1,'DrMundo':0,'Draven':0 ,'Ekko':0,'Elise':1, 'Evelynn':1,'Ezreal':0,'Fiddlesticks':0, 'Fiora':1, 'Fizz':0, 'Galio':0,'Gangplank':0,'Garen':0,'Gnar':0,'Gragas':0,'Graves':0,'Gwen':1,'Hecarim':0,'Heimerdinger':0,'Illaoi':0,'Irelia':1,'Ivern':0,'Janna':1,'JarvanIV':0 ,'Jax':0,'Jayce':0, 'Jhin':0,'Jinx':1,'Kaisa':1,'Kalista':1,'Karma':1,'Karthus':0,'Kassadin':0,'Katarina':1,'Kayle':1,'Kayn':0,'Kennen':0,'Khazix':0,'Kindred':0,'Kled':0,
                  'KogMaw':0,'Leblanc':1,'LeeSin':0,'Leona':1,'Lissandra':1,'Lillia':1,'Lucian':0,'Lulu':1,'Lux':1,'MasterYi':0,'Malphite':0,'Malzahar':0,'Maokai':0,'MissFortune':1,'Mordekaiser':0,'Morgana':1,'Nami':1,'Nasus':0,'Nautilus':0,'Nidalee':1,'Neeko':1,'Nocturne':0,'Nunu':0,'Olaf':0,'Orianna':1,'Ornn':0,'Pantheon':0,'Poppy':1,'Pyke':0,'Qiyana':1,
                  'Quinn':1,'Rakan':0,'Rammus':0,'RekSai':0,'Rell':1,'Renekton':0,'Renata':1,'Rengar':0,'Riven':1,'Rumble':0,'Ryze':0,'Samira':1,'Sejuani':1,'Senna':1,'Seraphine':1,'Sett':0,'Shaco':0,'Shen':0,'Shyvana':1,'Singed':0,'Sion':0,'Sivir':1,'Skarner':1,'Sona':1,'Soraka':1,'Swain':0,'Sylas':0,'Syndra':0,'TahmKench':0,'Taliyah':1,'Talon':0,'Taric':0,'Teemo':0,'Thresh':0 ,'Tristana':1,'Trundle':0,'Tryndamere':0,'TwistedFate':0,'Twitch':0,'Udyr':0,'Urgot':0,'Varus':0,'Vayne':1,'Veigar':0,'Velkoz':0,'Vex':1,'Vi':1,'Viego':0,'Viktor':0,'Vladimir':0,'Volibear':0,'Warwick':0,'MonkeyKing':0,'Xayah':1,'Xerath':0,'XinZhao':0,'Yasuo':0,'Yone':0,'Yorick':0,'Yuumi':1,'Zac':0,'Zed':0,'Zeri':1,'Ziggs':0,'Zilean':0,'Zoe':1,'Zyra':1}





class LoLInterface():
    """
    Interface that allows user to search for League of Legends Summoners info, ranked stats,
    matches...
    """

    def __init__(self):
        self.database = Data_base()
        # Api key needed to work with Riot Api
        self.api_key = 'RGAPI-08ee4765-7528-436c-946e-a7b7ba099a83'



        # LolWatcher instance creation
        self.watcher = LolWatcher(self.api_key)
        self.puuid = ""
        self.my_matches = 0
        self.window = Tk()
        self.my_region = ""
        self.liste_reseau_id = []
        self.liste_reseau_name = []
        self.rec = 0
        self.all_players = []
        self.all_players2 = []
        self.champ_dict = dict_champions

        # Treeview style
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview.Heading", font=('Helvetica Neue', 14, 'bold'), foreground='blue')
        self.style.configure("mystyle.Treeview", background="#b5c3f7", font=('Helvetica Neue', 11), rowheight=25,
                             foreground='black', fieldbackground='#3e61de', highlightthickness=0, bd=2, )
        self.style.map('Treeview',
                       background=[('selected', 'blue')])
        self.window.title("League of Legends Data Miner")
        self.window.resizable(True, True)
        self.window.config(pady=10, padx=10, background='#2F2F2F')

        # New window
        self.new_win = Toplevel(self.window)
        self.new_win.resizable(False, False)
        self.new_win.config(bg='#05061a')
        self.my_tree = ttk.Treeview(self.new_win, selectmode=BROWSE, style="mystyle.Treeview")
        self.new_win.withdraw()

        # New window
        self.new_win2 = Toplevel(self.window)
        self.new_win2.resizable(False, False)
        self.new_win2.config(bg='#378060')
        self.new_win2.withdraw()

        # New window
        self.new_win3 = Toplevel(self.window)
        self.new_win3.resizable(False, False)
        self.new_win3.config(bg='#378060')
        self.new_win3.withdraw()

        # New window
        self.new_win4 = Toplevel(self.window)
        self.new_win4.resizable(False, False)
        self.new_win4.config(bg='#378060')
        self.new_win4.withdraw()

        # Protocol when user press close window button
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing5)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.new_win2.protocol("WM_DELETE_WINDOW", self.on_closing2)
        self.new_win3.protocol("WM_DELETE_WINDOW", self.on_closing3)
        self.new_win4.protocol("WM_DELETE_WINDOW", self.on_closing4)

        # Listbox creation and configuration
        self.list = Listbox(justify=CENTER)
        self.list.config(width=10,height=4,borderwidth=2, activestyle=NONE, fg="white",
                         bg="#2F2F2F", font=("Arial", 15, "bold"), selectforeground="#03f8fc",
                         selectbackground="#03052e", selectborderwidth=0, selectmode=SINGLE,
                         highlightbackground='#313cf7', highlightcolor='#2029c7')
        self.list.grid(row=1, column=0, columnspan=2, pady=10, sticky=EW)

        # Scrollbar creation for Listbox
        self.list = Listbox(justify=CENTER)
        self.list.config(width=10,height=4,borderwidth=2, activestyle=NONE, fg="white",
                         bg="#464453", font=("Arial", 15, "bold"), selectforeground="#007956",
                         selectbackground="#2F2F2F", selectborderwidth=0, selectmode=SINGLE,
                         highlightbackground='#2F2F2F', highlightcolor='#005242')
        self.list.grid(row=1, column=0, columnspan=2, pady=10, sticky=EW)

        # Scrollbar creation for Listbox
        self.scroll = Scrollbar()
        self.scroll.grid(row=1, column=2, sticky=NS, pady=10)
        self.list.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.list.yview)

        # Labels, Entries and Buttons...
        self.label = ctkp.CTkLabel(text="Summoner name: ",
                                   text_font=('Helvetica Neue', 15, 'bold'), background='#05061a', foreground='#0f1adb',
                                   text_color='white')
        self.label.grid(row=2, column=0)
        self.text = ctkp.CTkEntry(justify=CENTER, text_font=('Helvetica Neue', 13, 'bold'), foreground='black',
                                  background='white', insertbackground='blue')
        self.text.grid(row=2, column=1)
        self.clear_entry = ctkp.CTkButton(width=50,
                                          height=10, text_font=('Helvetica Neue', 9, 'bold'), fg_color=("#2F2F2F"),
                                          border_width=3,
                                          corner_radius=8,
                                          text="Clear", command=self.clear,
                                          background='#BBF287', text_color='white', border_color='#005A34',
                                          hover_color='#005A34')
        self.clear_entry.grid(row=3, column=1)
        self.build_truc = ctkp.CTkButton(width=150,
                                         height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                         border_width=3,
                                         corner_radius=8,
                                         text="Creation network and data", command=self.run_db_scan,
                                         background='#BBF287', text_color='white', border_color='#005A34',
                                         hover_color='#005A34')
        self.build_truc.grid(row=6, column=0, sticky=EW, columnspan=3)
        self.build_truc2 = ctkp.CTkButton(width=150,
                                          height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                          border_width=3,
                                          corner_radius=8,
                                          text="delete Database", command=self.delete_alltables,
                                          background='#BBF287', text_color='white', border_color='#005A34',
                                          hover_color='#005A34')
        self.build_truc2.grid(row=13, column=0, sticky=EW, columnspan=3)

        self.addaperson = ctkp.CTkButton(width=150,
                                         height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                         border_width=3,
                                         corner_radius=8,
                                         text="Add one person to database", command=self.run_db_scan2,
                                         background='#BBF287', text_color='white', border_color='#005A34',
                                         hover_color='#005A34')
        self.addaperson.grid(row=7, column=0, sticky=EW, columnspan=3, pady=10)
        self.search_btn = ctkp.CTkButton(width=150,
                                         height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                         border_width=3,
                                         corner_radius=8,
                                         text="Show Last 100 Games", command=self.search_summoner,
                                         background='#BBF287', text_color='white', border_color='#005A34',
                                         hover_color='#005A34')
        self.search_btn.grid(row=11, column=0, sticky=EW, columnspan=3, pady=10)
        # self.search_btn_list = ctkp.CTkButton(width=150,
        #                                       height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
        #                                       border_width=3,
        #                                       corner_radius=8,
        #                                       text="Show stat for summoners in list",
        #                                       command=self.search_summoner_list,
        #                                       background='#BBF287', text_color='white', border_color='#005A34',
        #                                       hover_color='#005A34')
        # self.search_btn_list.grid(row=9, column=0, sticky=EW, columnspan=3, pady=10)
        self.view_ranked = ctkp.CTkButton(width=185,
                                          height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                          border_width=3,
                                          corner_radius=8,
                                          text="View ranked info", command=self.view_ranked_info, background='#858aed',
                                          text_color='white', border_color='#005A34', hover_color='#005A34')
        self.view_ranked.grid(row=8, column=0, sticky=W, columnspan=3)
        self.region_label = ctkp.CTkLabel(text="Player region: ", text_font=('Helvetica Neue', 15, 'bold'),
                                          background='#05061a', foreground='#0f1adb', text_color='white')
        self.player_list_label = ctkp.CTkLabel(text="Player list: ", text_font=('Helvetica Neue', 15, 'bold'),
                                               background='#05061a', foreground='#0f1adb', text_color='white')
        self.region_label.grid(row=4, column=0, sticky=E)
        self.player_list_label.grid(row=5, column=0, sticky=E)

        # Combobox to select the Summoner region
        self.combo = ttk.Combobox(self.window, state="readonly",
                                  values=['EUW1', 'BR1', 'EUN1', 'JP1', 'KR', 'LA1', 'LA2', 'NA1',
                                          'OC1', 'TR1', 'RU'], font=('Helvetica Neue', 10, 'bold'),
                                  justify=CENTER)
        with open('players_list.txt') as inFile:
            players = [line for line in inFile]
        self.combo_player = ttk.Combobox(self.window, state="readonly",
                                         values=tuple(players), font=('Helvetica Neue', 10, 'bold'),
                                         justify=CENTER, postcommand=self.updatecblist)

        self.combo_player.grid(row=5, column=1, pady=10, sticky=W)
        self.combo.grid(row=4, column=1, pady=10, sticky=W)

        self.last_20 = ctkp.CTkLabel(text="Last 20 games of", text_font=('Helvetica Neue', 14, 'bold'),
                                     background='#05061a',
                                     foreground='#0f1adb', text_color='white')
        self.last_20.grid(row=0, column=0, columnspan=2)
        self.view_active = ctkp.CTkButton(width=150,
                                          height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                          border_width=3,
                                          corner_radius=8,
                                          text="View active game", command=self.thread,
                                          background='#BBF287', text_color='white', border_color='#005A34',
                                          hover_color='#005A34')
        # self.view_active.grid(row=7, column=0, sticky=EW, pady=10, columnspan=3)
        self.top_p = ctkp.CTkButton(width=150,
                                    height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                    border_width=3,
                                    corner_radius=8,
                                    text="Stats", command=self.graph_games_by_freq,
                                    background='#BBF287', text_color='white', border_color='#005A34',
                                    hover_color='#005A34')
        self.top_p.grid(row=10, column=0, sticky=EW, columnspan=3)
        self.loadbtn = ctkp.CTkButton(width=185,
                                      height=50, text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                      border_width=3,
                                      corner_radius=8,
                                      text="Show Calendar", command=self.make_calendar,
                                      background='#BBF287', text_color='white', border_color='#005A34',
                                      hover_color='#005A34')
        self.loadbtn.grid(row=8, column=1, sticky=E, columnspan=3, pady=10)
        self.listbox = Listbox(self.new_win4, justify=CENTER)

        self.selection = 0
        self.list.select_set(self.selection)
        self.list.bind("<Down>", self.OnEntryDown)
        self.list.bind("<Up>", self.OnEntryUp)
        self.listbox.bind('<Double-Button>', self.double_click2)

        self.listesansdoublon = []
        self.window.mainloop()

    def make_calendar(self):

        self.my_region = self.combo.get()
        if self.combo_player.get() == "" or self.combo_player.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must select a summoner name and region.")
        else:
            try:
                name = self.combo_player.get()
                nameF = name[:-1]
                me = self.watcher.summoner.by_name(self.my_region, nameF)

            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:

                init_calendar(nameF)

    def delete_alltables(self):
        try:
            self.database.drop_table("Partie")
            self.database.drop_table("all_summoner")
            os.remove("players_list.txt")
            print("TZESJDDDZJDZJDJZJJJJJJJJJJJJJJJJJJJJJJJJJ")
            with open('players_list.txt', 'w') as f:
                f.write('')
                f.close()
        except:
            print("No such tables")

    # def by_duration(self):
    #     name = self.combo_player.get()[:-1]
    #     query_end = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"',["col_timestamp"])#end
    #     query_start = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_matchstart"])
    #     query_gamedurations = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_gameduration"])
    #     print(query_end)
    #     print(query_start)
    #     start_timestamp =[]
    #     end_timestamp = []
    #     game_durations = []
    #     for a in query_end:
    #         end_timestamp.append(datetime.utcfromtimestamp(float(a[0])).strftime('%H'))
    #
    #     for b in query_end:
    #         start_timestamp.append(b[0])
    #
    #     for a in query_gamedurations:
    #         game_durations.append(datetime.utcfromtimestamp(float(a[0])).strftime('%H'))
    #
    #     print(end_timestamp)
    #     print(game_durations)









        query_starting_timestamp = 0


    def determine_role_by_puid(self):  # coute beaucoup de requ??tes
        roles = []
        main_role = ''

        # matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid,count = 100)
        # list_containing_all_roles = []
        # for a in range(games):
        #     temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     role = temp_match_detail['info']['participants'][
        #         self.find_position_of_a_player(puid, temp_match_detail['metadata']['participants'])][
        #         'individualPosition']
        #     list_containing_all_roles.append(role)

        name = self.combo_player.get()[:-1]
        list_containing_all_roles = []
        query = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_individualPosition"])
        for a in query:
            list_containing_all_roles.append(a[0])


        frequency = {'MIDDLE': 0, 'TOP': 0, 'JUNGLE': 0, 'SUPPORT': 0, 'BOTTOM': 0}
        for elem in list_containing_all_roles:
            if elem in frequency:
                frequency[elem] += 1
            else:
                frequency[elem] = 1

        for keys, values in frequency.items():
            if values / len(query) > 0.3:
                main_role += keys + ' '
        print(main_role)
        if ("Invalid" in main_role):
            main_role ="No Main role"


        return main_role

    def percentage_of_female_caracters_played(self):
        #matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid, count=100)
        list_containing_all_champs = []
        percentage = 0
        # for a in range(games):
        #     print(a)
        #     temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #
        #     champ = temp_match_detail['info']['participants'][
        #         self.find_position_of_a_player(puid, temp_match_detail['metadata']['participants'])]['championName']
        #     print(champ)
        #     print(self.watcher.summoner.by_puuid(self.my_region, puid)['name'])

        #     time.sleep(2)
        name = self.combo_player.get()[:-1]
        champ = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"',["col_championName"])
        print(self.combo_player.get(),"owo")
        print(champ)
        # for a in
        #     if self.champ_dict[champ] == 1:
        #         percentage += 1
        #     list_containing_all_champs.append(champ)
        champion_list = []
        for a in champ:
            champion_list.append(a[0])

        for a in champion_list:
            if self.champ_dict[a] == 1:
                percentage +=1
        print(champion_list)
        percentage = percentage/len(champion_list)
        return percentage




        # percentage = percentage / games
        # print(percentage)
        # print(list_containing_all_champs)
        # return percentage

    def percentage_of_role_played(self,role):
        name = self.combo_player.get()[:-1]
        role_query = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_individualPosition"])
        #matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid, count=100)
        percentage = 0
        # for a in range(games):
        #     temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     match_role = temp_match_detail['info']['participants'][self.find_position_of_a_player(puid, temp_match_detail['metadata']['participants'])]['individualPosition']
        #     time.sleep(1)
        #     if match_role == role:
        #         percentage += 1
        #
        # percentage = percentage / games
        # print(percentage)
        role_list = []
        for a in role_query:
            role_list.append(a[0])

        for match_role in role_list:
            if match_role == role:
                percentage += 1

        percentage = percentage/len(role_query)
        return percentage



    def clear(self):
        self.text.delete(0, END)

    def thread(self):
        s = Thread(target=self.view_active_game)
        s.start()

    def OnEntryDown(self, event):
        if self.selection < self.list.size() - 1:
            self.list.select_clear(self.selection)
            self.selection += 1
            self.list.select_set(self.selection)

    def OnEntryUp(self, event):
        if self.selection > 0:
            self.list.select_clear(self.selection)
            self.selection -= 1
            self.list.select_set(self.selection)

    def updatecblist(self):
        with open('players_list.txt') as inFile:
            players = [line for line in inFile]
        self.combo_player['values'] = tuple(players)

    def view_ranked_info(self):
        """Function that shows a message box with info about the Summoner ranked status"""

        # Get the combo item
        self.my_region = self.combo.get()
        print(self.my_region)
        print(self)
        # If statement to check if Summoner Entry is correct
        if self.combo_player.get() == "" or self.combo_player.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must select a summoner name and region.")
        else:
            try:
                # We get the Summoner info
                name = self.combo_player.get()
                nameF = name[:-1]
                me = self.watcher.summoner.by_name(self.my_region, nameF)
                self.puuid = me["puuid"]

                # Get the summoner ranked info
                my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
                gender_info=self.percentage_of_female_caracters_played()
                main_role=self.determine_role_by_puid()


            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                try:
                    self.savePlayers()
                    # Calculate the winrate
                    winrate = my_ranked_stats[0]['wins'] / (
                                my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                    winrate = winrate * 100

                    # Messagebox with all the info
                    messagebox.showinfo(title=f"{self.text.get()} ranked info",
                                        message=f"""
Mode: {my_ranked_stats[0]['queueType']}\n
Elo: {my_ranked_stats[0]['tier']}\n
League Points: {my_ranked_stats[0]['leaguePoints']}\n
Wins: {my_ranked_stats[0]['wins']}\n
Losses: {my_ranked_stats[0]['losses']}\n
Games: {my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses']}\n
Winrate: {round(winrate)}%\n
HotSreak: {my_ranked_stats[0]['hotStreak']}\n
Gender Info: {gender_info}\n
Most Played Role: {main_role}\n
""")
                except IndexError:
                    messagebox.showwarning(title="Atenci??n!", message="The player has not completed the placement"
                                                                      " games.")

    def find_position_of_a_player(self, puuid, lpart):
        x = 0

        for i in (lpart):

            if i != puuid:

                x = x + 1
            else:
                # print("we found")
                return (x)
        return


    def reseau2(self,puuid,taille):
        if len(self.all_players2) == taille:
            return self.all_players2
        try:
            temp_matches0 = self.watcher.match.matchlist_by_puuid(self.my_region, puuid,count=20)
        except:
            time.sleep(1)
            temp_matches0 = self.watcher.match.matchlist_by_puuid(self.my_region, puuid, count=20)


        try:
            self.my_matches2 = self.watcher.match.matchlist_by_puuid(self.my_region, puuid)
        except:
            time.sleep(1)
            self.my_matches2 = self.watcher.match.matchlist_by_puuid(self.my_region, puuid)

        if (len(temp_matches0) < 20):
            print('\033[94mARCHAMBEEEEEEEEEEEEEEEEEEEEEE VIEN LAAAAAAAAAAAAAAAAAAA",self.watcher.summoner.by_puuid(self.my_region, a)["name"]\033[0m')
        else:
            print("joueur bien ajout??")
            self.all_players2.append(puuid)
        try:
            match_detail3 = self.watcher.match.by_id(self.my_region, self.my_matches2[1])
        except:
            time.sleep(1)
            match_detail3 = self.watcher.match.by_id(self.my_region, self.my_matches2[1])

        # for puid in match_detail['metadata']['participants']: #participant de la game de swipe
        # participants.append(self.watcher.summoner.by_puuid(self.my_region, puid)['name'])
        rand = random.randint(0,5)


        for puid in match_detail3['metadata']['participants']:
            temp_matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid)
            temp_match_detail = self.watcher.match.by_id(self.my_region, temp_matches[rand])
            print(len(temp_matches))
            for a in temp_match_detail['metadata']['participants']:
                #self.all_players.append(self.watcher.summoner.by_puuid(self.my_region, a)['name'])
                print('\033[94mtestcouleur\033[0m')

                if (len(temp_matches)<20):
                    print('\033[94mARCHAMBEEEEEEEEEEEEEEEEEEEEEE VIEN LAAAAAAAAAAAAAAAAAAA",self.watcher.summoner.by_puuid(self.my_region, a)["name"]\033[0m')
                    continue
                print("lesmec",self.watcher.summoner.by_puuid(self.my_region, a)["name"])
                self.save_list_Players(self.watcher.summoner.by_puuid(self.my_region, a)["name"])
                self.all_players2.append(self.watcher.summoner.by_puuid(self.my_region, a)["puuid"])
                #self.all_players = list(set(self.all_players))
                self.all_players2 = list(set(self.all_players2))
            #print(self.all_players)
                print(len(self.all_players2))
                if (len(self.all_players2) == taille):
                    print(self.all_players2)
                    return self.all_players2

        self.reseau2(self.all_players2[self.rec + 1],taille)




    def when_player_plays(self):# return dict {lundi:num_of_games,mardi:'78    etc..}
        #matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid,count=100)
        name = self.text.get()[:-1]

        query = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_timestamp"])
        list_containing_all_timestamps_from_last_games = []
        for a in query:
            list_containing_all_timestamps_from_last_games.append(a[0])

        dico_jours = {0:'Lundi',1:'Mardi',2:'Mercredi',3:'Jeudi',4:'Vendredi',5:'Samedi',6:'Dimanche'}
        dict_to_return = {}
        # for a in range(games):
        #     try:
        #         temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     except:
        #         time.sleep(4)
        #         temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     timestamp = temp_match_detail['info']['gameStartTimestamp']
        #     list_containing_all_timestamps_from_last_games.append(timestamp)
        for timestamp in list_containing_all_timestamps_from_last_games:
            dt_object = datetime.fromtimestamp(timestamp)

            print(dt_object.weekday())
            day_occ = dt_object.weekday()
            if dico_jours[day_occ] in dict_to_return:
                dict_to_return[dico_jours[day_occ]].append(timestamp)
            else:
                dict_to_return[dico_jours[day_occ]] = []
            print(dt_object.weekday())
            time.sleep(3)
        print(list_containing_all_timestamps_from_last_games)
        print(dict_to_return)
        return dict_to_return

    def when_player_plays_hour(self):# return dict {lundi:num_of_games,mardi:'78    etc..}
        name = self.text.get()
        print("test",name)
        query = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_timestamp"])
        print('-------------------------------query-----------------------------------',query)
        list_containing_all_timestamps_from_last_games = []
        for timestamp in query:
            list_containing_all_timestamps_from_last_games.append(timestamp[0])
        print('uuuuuuuuuu',list_containing_all_timestamps_from_last_games)


        # matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid,count=100)
        # list_containing_all_timestamps_from_last_games = []
        dico_jours = {0:'Lundi',1:'Mardi',2:'Mercredi',3:'Jeudi',4:'Vendredi',5:'Samedi',6:'Dimanche'}
        dict_to_return = {}

        for timestamp in list_containing_all_timestamps_from_last_games:
            dt_object = datetime.fromtimestamp(float(timestamp))
            print(dt_object.day)
            day_occ = dt_object.weekday()
            print('owo')
            if dico_jours[day_occ] in dict_to_return:
                dict_to_return[dico_jours[day_occ]].append(datetime.utcfromtimestamp(float(timestamp)).strftime('%H'))
            else:
                dict_to_return[dico_jours[day_occ]] = []

        # for a in range(games):
        #     try:
        #         print(games)
        #         print(a)
        #         temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     except:
        #         time.sleep(4)
        #         temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     timestamp = temp_match_detail['info']['gameStartTimestamp']
        #     list_containing_all_timestamps_from_last_games.append(timestamp)
        #     dt_object = datetime.fromtimestamp(timestamp/1000)
        #     day_occ = dt_object.weekday()
        #
        #     if dico_jours[day_occ] in dict_to_return:
        #         dict_to_return[dico_jours[day_occ]].append(datetime.utcfromtimestamp(timestamp/1000).strftime('%H'))
        #     else:
        #         dict_to_return[dico_jours[day_occ]] = []
        #     print(dt_object.weekday())
        #     time.sleep(4)
        print(list_containing_all_timestamps_from_last_games)
        print(dict_to_return)
        return dict_to_return

    def graph_by_hour(self,day):#day is a string 'Lundi' for example
        #the goal of this function is to display a graph of the frequency of game played for the period of times of 2 hours
        timeperiods = [[x,x+2] for x in range(23) if x%2==0]#[[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12]..]
        left = [range(1,12)]


        dict_hours = self.when_player_plays_hour()
        print(dict_hours)
        list_hours = dict_hours[day]
        print(list_hours)

        # x-coordinates of left sides of bars
        left = [x for x in range(24)]

        # heights of bars
        tick_label = [x for x in range(24)]  # nb de games par lapse de temps

        # labels for bars
        height = []  # laspe de temps
        for x in range(24):
            height.append(0)

        for x in list_hours:
            height[int(x)] +=1



        # plotting a bar chart
        plt.bar(left, height, tick_label=tick_label,
                width=0.8, color=['blue', 'green'])

        # naming the x-axis
        plt.xlabel('heure de la journ??e')
        # naming the y-axis
        plt.ylabel('nombre de partie jou??es')
        # plot title
        plt.title(day.upper())

        # function to show the plot
        plt.show()













    def when_player_plays_freq(self):# return dict {lundi:num_of_games,mardi:'78    etc..}
        #matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid,count=100)
        #list_containing_all_timestamps_from_last_games = []


        dico_jours = {0:'Lundi',1:'Mardi',2:'Mercredi',3:'Jeudi',4:'Vendredi',5:'Samedi',6:'Dimanche'}
        dict_to_return = {}

        name = self.combo_player.get()[:-1]

        query  = self.database.select_data_with_condition("Partie", f' col_summonerName = "{name}"', ["col_timestamp"])
        list_containing_all_timestamps_from_last_games=[]
        for a in query:
            list_containing_all_timestamps_from_last_games.append(a[0])

        for timestamp in list_containing_all_timestamps_from_last_games:
            dt_object = datetime.fromtimestamp(float(timestamp))
            day_occ = dt_object.weekday()
            if dico_jours[day_occ] in dict_to_return:
                dict_to_return[dico_jours[day_occ]] += 1
            else:
                dict_to_return[dico_jours[day_occ]] = 1





        # for a in range(games):
        #     try:
        #         temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     except:
        #         time.sleep(2)
        #         temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
        #     timestamp = temp_match_detail['info']['gameStartTimestamp']
        #     list_containing_all_timestamps_from_last_games.append(timestamp)
        #     dt_object = datetime.fromtimestamp(timestamp/1000)
        #     day_occ = dt_object.weekday()
        #     if dico_jours[day_occ] in dict_to_return:
        #         dict_to_return[dico_jours[day_occ]] +=1
        #     else:
        #         dict_to_return[dico_jours[day_occ]] = 1
        #     print(dt_object.weekday())
        #     time.sleep(4)
        print(list_containing_all_timestamps_from_last_games)
        print(dict_to_return)
        return dict_to_return

    def graph_games_by_freq(self):
        # x-coordinates of left sides of bars
        dict_we_gonna_use = {}
        left = [1, 2, 3, 4, 5, 6, 7]

        # heights of bars
        height = [10, 24, 36, 40, 89, 12, 50]  # nb de games par lapse de temps
        height = []
        dict_of_days = self.when_player_plays_freq()

        for key,value in dict_of_days.items():
            height.append(value)
        left = list(range(1,len(dict_of_days)+1))

        # labels for bars
        tick_label = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']  # laspe de temps
        #tick_label = list(set(dict_of_days) & set(tick_label))
        tick_label = [x for x in tick_label if x in list(dict_of_days)]
        print(tick_label)
        height=[]
        for a in tick_label:#remettre dans l'ordre
            height.append(dict_of_days[a])

        # plotting a bar chart
        plt.bar(left, height, tick_label=tick_label,
                width=0.8, color=['red', 'green'])

        # naming the x-axis
        plt.xlabel('jour')
        # naming the y-axis
        plt.ylabel('parties jou??es')
        # plot title
        plt.title('Frequence de parties sur les derni??res')

        # function to show the plot
        plt.show()

    def ajoutbase_reseau(self,reseau_liste,nbgame):
        for b in range(len(reseau_liste)):
            init = False
            try:
                me3 = self.watcher.summoner.by_puuid(self.my_region, reseau_liste[b])
            except:
                time.sleep(1)
                me3 = self.watcher.summoner.by_puuid(self.my_region, reseau_liste[b])
            try:
                self.my_matches4 = self.watcher.match.matchlist_by_puuid(self.my_region, reseau_liste[b], count=nbgame)
            except:
                time.sleep(1)
                self.my_matches4 = self.watcher.match.matchlist_by_puuid(self.my_region, reseau_liste[b], count=nbgame)

            print("NOMBREDEGAMEDECEMEC", len(self.my_matches4))
            for j in range(len(self.my_matches4)):
                # print(self.my_matches4)
                try:
                    match_detail_choixmatch = self.watcher.match.by_id(self.my_region, self.my_matches4[int(j)])
                except:
                    time.sleep(2)
                    match_detail_choixmatch = self.watcher.match.by_id(self.my_region, self.my_matches4[int(j)])

                liste_part_puid = match_detail_choixmatch['metadata']['participants']

                print(liste_part_puid)
                pos = self.find_position_of_a_player(me3["puuid"], liste_part_puid)
                # kill = match_detail_choixmatch["info"]["participants"][pos]["kills"]
                all = match_detail_choixmatch["info"]["participants"][pos]

                # morts = match_detail_choixmatch["info"]["participants"][pos]["deaths"]
                # assist = match_detail_choixmatch["info"]["participants"][pos]["assists"]

                # print("kda", kill, morts, assist)

                try:

                    match_end = (match_detail_choixmatch["info"].get("gameEndTimestamp")) / 1000
                    match_dat1 = datetime.fromtimestamp(match_end)
                    match_date = match_dat1.strftime("%m/%d/%Y - %H:%M:%S")
                    game_duration = round(match_detail_choixmatch['info']['gameDuration'] / 60)
                    match_start = (match_detail_choixmatch["info"].get("gameStartTimestamp")) / 1000

                except:
                    break

                # liste_finale.append(listelem)
                last_dict = {}
                all.pop('perks')

                for key, value in all.items():
                    if type(value) == dict:

                        last_dict = last_dict | value

                    else:
                        last_dict = last_dict | {key: value}
                # print("test2", last_dict)
                last_dict = last_dict | {'timestamp': match_end}
                last_dict = last_dict | {'date': match_date}
                last_dict = last_dict | {'gameduration': game_duration}
                last_dict = last_dict | {'matchstart': match_start}
                try:
                    if init:
                        for ele in last_dict.keys():
                            if ele not in self.database.list_columns("Partie"):
                                self.database.add_column("Partie", ele)

                        # print(last_dict)
                    self.database.read_data_from_a_dict(last_dict, "Partie", ["summonerName","timestamp"])
                    init = True
                except :
                    self.database.read_data_from_a_dict(last_dict, "Partie", ["summonerName","timestamp"])
                    init = True
        print("FIN")

    def determine_if_female(self, puid, games):  # str
        if self.determine_role_by_puid(puid,games) == 'Support' and self.percentage_of_female_caracters_played(puid,games) > 0.9:
            return 'tres probable'
        if self.percentage_of_female_caracters_played(puid, games) > 0.9:
            return 'probable'
        if self.percentage_of_female_caracters_played(puid, games) > 0.7:
            return 'un peu moins probable'
        return 'tres peu probable'

    def add_one_person(self):
        init = False
        self.my_region = self.combo.get()
        # self.text.get() = summonername
        if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must enter a summoner name and region.")
        else:
            try:
                print("")
                me = self.watcher.summoner.by_name(self.my_region, self.text.get())
                print("test", me)
                print("testowo", me["name"])
            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                # self.savePlayers()
                self.save_list_Players(self.text.get())

                self.puuid = me['puuid']
                print(self.puuid)
                puuid_liste=[self.puuid]
                self.ajoutbase_reseau(puuid_liste,10)
                time.sleep(60 * 60)


    def create_dataset_and_add(self):
        while True:
            init = False
            self.my_region = self.combo.get()
            # self.text.get() = summonername
            if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
                messagebox.showerror(title="Error!", message="You must enter a summoner name and region.")
            else:
                try:
                    print("")
                    me = self.watcher.summoner.by_name(self.my_region, self.text.get())
                    print("test", me)
                    print("testowo", me["name"])
                except HTTPError:
                    messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                                 " api key"
                                                                 " or the Summoner does not exist in the specified region")
                except UnicodeEncodeError:
                    messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
                else:
                    #self.savePlayers()
                    self.save_list_Players(self.text.get())


                    self.puuid = me['puuid']
                    self.reseau2(self.puuid,5) #retourne all_player2 qui contient tout les membres d'un r??seau

                    # a = asyncio.get_event_loop()
                    # a.create_task(every(10*60,self.ajoutbase_reseau))
                    # a.run_forever()


                    self.ajoutbase_reseau(self.all_players2,10)
                    time.sleep(60*60)


    def run_db_scan(self):
        s = Thread(target=self.create_dataset_and_add)

        s.start()

    def run_db_scan2(self):
        s = Thread(target=self.add_one_person)

        s.start()





    def search_summoner(self):
        """Function that gets the last 20 games of the Summoner and adds them to the Listbox"""
        init = False
        self.my_region = self.combo.get()
        # self.text.get() = summonername
        if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            self.search_summoner_list()
        else:
            try:
                print("")
                me = self.watcher.summoner.by_name(self.my_region, self.text.get())
                print("test",me)
                print("testowo",me["name"])
            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                self.savePlayers()
                try:
                    self.save_list_Players(self.text.get())
                except:
                    pass


                self.puuid = me['puuid']

                # We search for the Summoner matches
                try:
                    self.my_matches = self.watcher.match.matchlist_by_puuid(self.my_region, self.puuid, count=100)
                except:
                    time.sleep(1)
                    self.my_matches = self.watcher.match.matchlist_by_puuid(self.my_region, self.puuid, count=100)



                self.list.delete(0, END)

                for i in range(1, 100):
                    self.list.insert(END, f'{me["name"]} ???? Game {i}')

                # Bind that allows user to interact with Listbox items by double clicking them
                self.list.bind("<Double-1>", self.OnDoubleClick)
                self.list.bind("<Return>", self.OnDoubleClick)
                self.last_20.config(text=f"Last 20 games of {me['name']}")




                #self.reseau2(self.puuid)


                #self.reseau(self.puuid)

                # match_detail3 = self.watcher.match.by_id(self.my_region, self.my_matches[0])
                # # for puid in match_detail['metadata']['participants']: #participant de la game de swipe
                # # participants.append(self.watcher.summoner.by_puuid(self.my_region, puid)['name'])
                #
                # all_players = []
                # for puid in match_detail3['metadata']['participants']:
                #     temp_matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid)
                #     temp_match_detail = self.watcher.match.by_id(self.my_region, temp_matches[0])
                #     for a in temp_match_detail['metadata']['participants']:
                #         all_players.append(self.watcher.summoner.by_puuid(self.my_region, a)['name'])
                #     print(all_players)
                #     print(len(all_players))



                liste_finale = []

                liste_kill = []
                liste_date = []
                liste_mort = []

                # a = asyncio.get_event_loop()
                # a.create_task(every(10*60,self.ajoutbase))
                # a.run_forever()
                #self.ajoutbase()


                # for b in range(len(self.all_players2)):
                #     init = False
                #     try:
                #         me3 = self.watcher.summoner.by_puuid(self.my_region, self.all_players2[b])
                #     except:
                #         time.sleep(1)
                #         me3 = self.watcher.summoner.by_puuid(self.my_region, self.all_players2[b])
                #     try:
                #         self.my_matches4 = self.watcher.match.matchlist_by_puuid(self.my_region, self.all_players2[b],count=10)
                #     except:
                #         time.sleep(1)
                #         self.my_matches4 = self.watcher.match.matchlist_by_puuid(self.my_region, self.all_players2[b],count=10)
                #
                #     print("NOMBREDEGAMEDECEMEC",len(self.my_matches4))
                #     for j in range(len(self.my_matches4)):
                #         #print(self.my_matches4)
                #         try:
                #             match_detail_choixmatch = self.watcher.match.by_id(self.my_region, self.my_matches4[int(j)])
                #         except:
                #             time.sleep(1)
                #             match_detail_choixmatch = self.watcher.match.by_id(self.my_region, self.my_matches4[int(j)])
                #
                #         liste_part_puid = match_detail_choixmatch['metadata']['participants']
                #
                #         print(liste_part_puid)
                #         pos = self.find_position_of_a_player(me3["puuid"], liste_part_puid)
                #         #kill = match_detail_choixmatch["info"]["participants"][pos]["kills"]
                #         all = match_detail_choixmatch["info"]["participants"][pos]
                #
                #         #morts = match_detail_choixmatch["info"]["participants"][pos]["deaths"]
                #         #assist = match_detail_choixmatch["info"]["participants"][pos]["assists"]
                #
                #         #print("kda", kill, morts, assist)
                #
                #         try:
                #
                #             match_start = (match_detail_choixmatch["info"].get("gameEndTimestamp")) / 1000
                #             match_dat1 = datetime.fromtimestamp(match_start)
                #             match_date = match_dat1.strftime("%m/%d/%Y - %H:%M:%S")
                #         except:
                #             break
                #
                #
                #
                #         #liste_finale.append(listelem)
                #         last_dict = {}
                #         all.pop('perks')
                #
                #         for key, value in all.items():
                #             if type(value) == dict:
                #
                #                 last_dict = last_dict | value
                #
                #             else:
                #                 last_dict = last_dict | {key: value}
                #         #print("test2", last_dict)
                #         last_dict = last_dict | {'timestamp': match_start}
                #         last_dict = last_dict | {'date': match_date}
                #         try:
                #             if init:
                #                 for ele in last_dict.keys():
                #                     if ele not in self.database.list_columns(last_dict.get("summonerName")):
                #                         self.database.add_column(last_dict.get("summonerName"), ele)
                #
                #                 #print(last_dict)
                #             self.database.read_data_from_a_dict(last_dict, "summonerName", "timestamp")
                #             init = True
                #         except sqlite3.Error as error:
                #             self.database.read_data_from_a_dict(last_dict, "summonerName", "timestamp")
                #             init = True
                #print("FIN")
    def search_summoner_list(self):
        """Function that gets the last 20 games of the Summoner in combo_players and adds them to the Listbox"""

        self.my_region = self.combo.get()
        if self.combo_player.get() == "" or self.combo_player.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must select a summoner name and region.")
        else:
            try:
                name = self.combo_player.get()
                print("a")
                print(name[:-1])
                print("a")
                nameF = name[:-1]
                me = self.watcher.summoner.by_name(self.my_region, nameF)

            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:

                self.puuid = me['puuid']

                # We search for the Summoner matches
                self.my_matches = self.watcher.match.matchlist_by_puuid(self.my_region, self.puuid)
                self.list.delete(0, END)

                for i in range(1, 21):
                    self.list.insert(END, f'{me["name"]} ???? Game {i}')

                # Bind that allows user to interact with Listbox items by double clicking them
                self.list.bind("<Double-1>", self.OnDoubleClick)
                self.list.bind("<Return>", self.OnDoubleClick)
                self.last_20.config(text=f"Last 20 games of {me['name']}")



    def OnDoubleClick(self, event):
        """
        Function that allows user to interact with Listbox items by double clicking them and
            shows a pop up window with a Treeview with all game selected info
        """
        #self.graph_by_hour('Samedi')
        #self.graph_games_by_freq()
        print('owo')
        self.new_win.config(cursor='top_left_arrow')
        item = self.list.curselection()
        item2 = ''.join(map(str, item))
        try:
            match_detail = self.watcher.match.by_id(self.my_region, self.my_matches[int(item2)])
        except HTTPError:
            messagebox.showerror(title='Error!', message='Close the window and try again.')
        participants = []
        for puid in match_detail['metadata']['participants']:
            participants.append(self.watcher.summoner.by_puuid(self.my_region, puid)['name'])

        par = [i for i in participants]
        champ1 = [i['championName'] for i in match_detail['info']['participants']]
        role1 = [i['individualPosition'] for i in match_detail['info']['participants']]
        kills = [i['kills'] for i in match_detail['info']['participants']]
        match_timestamp_to_convert = match_detail['info']['gameStartTimestamp']
        date_in_sec = match_timestamp_to_convert / 1000  # convert milliseconde in second

        match_dat1 = datetime.fromtimestamp(date_in_sec)
        match_date = match_dat1.strftime("%m/%d/%Y - %H:%M:%S")
        print("date_time:", match_date)
        # print("type of dt:", type(match_date))

        match_end = match_detail['info']['gameEndTimestamp']
        deaths1 = [i['deaths'] for i in match_detail['info']['participants']]
        assists1 = [i['assists'] for i in match_detail['info']['participants']]
        wards1 = [i['wardsPlaced'] for i in match_detail['info']['participants']]
        gold = [i['goldEarned'] for i in match_detail['info']['participants']]
        minions = [i['totalMinionsKilled'] for i in match_detail['info']['participants']]
        neu_minions = [i['neutralMinionsKilled'] for i in match_detail['info']['participants']]
        suma1 = [x + y for x, y in zip(minions, neu_minions)]
        dano_total = [i['totalDamageDealtToChampions'] for i in match_detail['info']['participants']]
        dano_recibido = [i['totalDamageTaken'] for i in match_detail['info']['participants']]
        win = [i['win'] for i in match_detail['info']['participants']]

        data = {
            'Summoner': par,
            'Champion': champ1,
            'Role': role1,
            'Kills': kills,
            'Deaths': deaths1,
            'Assists': assists1,
            'Wards': wards1,
            'match Date': match_date,
            'Farm': suma1,
            'Total Damage Dealt': dano_total,
            'Total Taken Damage': dano_recibido,
            'Result': win
        }

        # Create pandas Dataframe
        df = pd.DataFrame(data)
        df['Role'].replace(to_replace=dict(UTILITY='SUPPORT'), inplace=True)
        df['Champion'].replace(to_replace=dict(MonkeyKing='Wukong'), inplace=True)
        df['Result'].replace({True: 'VICTORY', False: 'DEFEAT'}, inplace=True)
        self.summoner_result = str(df.loc[df['Summoner'] == self.text.get()]['Result'])
        game_start = datetime.fromtimestamp(match_detail['info']['gameStartTimestamp'] / 1000)
        game_start = game_start.strftime("%m/%d/%Y - %H:%M:%S")
        game_end = datetime.fromtimestamp(match_detail['info']['gameEndTimestamp'] / 1000)
        game_end = game_end.strftime("%m/%d/%Y - %H:%M:%S")
        game_duration = round(match_detail['info']['gameDuration'] / 60)

        for name in match_detail['info']['participants']:
            if str(name['summonerName']).lower() == self.text.get().lower():
                if name['win']:
                    self.summoner_result = "VICTORY"
                else:
                    self.summoner_result = "DEFEAT"

        for r in role1:
            if r == 'Invalid':
                match_de = 'ARAM'
            else:
                match_de = match_detail["info"]["gameType"]

        self.new_win.title(f'[Game ID: {match_detail["info"]["gameId"]}] [Game Type:'
                           f' {match_de}]'
                           f' [Summoner Result: [{self.summoner_result}] '
                           f'[Game Start: {game_start}] [Game End: {game_end}]'
                           f' [Game Duration: {game_duration} minutes]')

        # Had to delete Treeview object because a bug???
        del self.my_tree

        # Create the Treeview with DataFrame info
        self.my_tree = ttk.Treeview(self.new_win, selectmode=BROWSE, style="mystyle.Treeview")
        self.my_tree["column"] = list(df.columns)
        self.my_tree["show"] = "headings"
        self.my_tree.bind('<Double-Button>', self.double_click3)
        self.my_tree.bind('<Return>', self.double_click3)

        for column in self.my_tree["column"]:
            self.my_tree.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.my_tree.insert("", END, values=row)

        def copyy():
            try:
                curItem = self.my_tree.focus()
                item = self.my_tree.item(curItem)
                self.new_win.clipboard_clear()
                self.new_win.clipboard_append(item['values'][0])
                messagebox.showinfo(title="Info!", message="Copied succesfully!")
            except IndexError:
                messagebox.showwarning(title="Atention!", message="You must make a selection.")

        self.my_tree.column("Summoner", width=150, minwidth=150, anchor=CENTER)
        self.my_tree.column("Champion", width=100, minwidth=100, anchor=CENTER)
        self.my_tree.column("Role", width=100, minwidth=100, anchor=CENTER)
        self.my_tree.column("Kills", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Deaths", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Assists", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Wards", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("match Date", width=180, minwidth=180, anchor=CENTER)
        self.my_tree.column("Farm", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Total Damage Dealt", width=190, minwidth=190, anchor=CENTER)
        self.my_tree.column("Total Taken Damage", width=190, minwidth=190, anchor=CENTER)
        self.my_tree.column("Result", width=100, minwidth=100, anchor=CENTER)
        m = Menu(self.new_win, tearoff=0)
        m.add_command(label="View Player OPGG", command=self.view_opgg)
        m.add_command(label="Copy Summoner Name", command=copyy)

        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        self.my_tree.bind("<Button-3>", do_popup)

        self.my_tree.grid(row=0, column=0)

        self.window.grab_set()
        self.new_win.deiconify()

    def on_closing5(self):
        """Function that triggers when user closes second window."""
        m = messagebox.askyesno(title="Exit?", message="Are you sure you want to exit?")
        if m:
            self.window.destroy()

    def on_closing(self):
        """Function that triggers when user closes second window."""

        self.new_win.withdraw()

    def on_closing2(self):
        """Function that triggers when user closes second window."""

        self.new_win2.withdraw()

    def on_closing3(self):
        """Function that triggers when user closes second window."""

        self.new_win3.withdraw()

    def on_closing4(self):
        """Function that triggers when user closes second window."""

        self.new_win4.withdraw()

    def view_active_game(self):
        """
        Function that allows user to look at the game that player is actually playing.
        """

        self.my_region = self.combo.get()

        if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title='Error!', message='You must enter a Summoner name and region.')
        else:
            try:
                me = self.watcher.summoner.by_name(self.my_region, self.text.get())
                me_now = me['name']
                active_game = self.watcher.spectator.by_summoner('EUW1', me['id'])
            except HTTPError:
                messagebox.showerror(title='Error!', message='Requested Summoner is not in an active game.')
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                participants = []
                elos = []
                l_points = []
                wins = []
                losses = []
                hot_streak = []
                win_r = []
                total_g = []
                rank = []
                for p in active_game['participants']:
                    participants.append(p['summonerName'])

                for p in participants:
                    me = self.watcher.summoner.by_name(self.my_region, p)
                    my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
                    try:
                        elos.append(my_ranked_stats[0]['tier'])
                        l_points.append(my_ranked_stats[0]['leaguePoints'])
                        wins.append(my_ranked_stats[0]['wins'])
                        losses.append(my_ranked_stats[0]['losses'])
                        hot_streak.append(my_ranked_stats[0]['hotStreak'])
                        winrate = my_ranked_stats[0]['wins'] / (
                                my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                        winrate = winrate * 100
                        win_r.append(f'{round(winrate)}%')
                        total_g.append(my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                        rank.append(my_ranked_stats[0]['rank'])
                    except KeyError:
                        messagebox.showwarning(title="Error!", message="Something went wrong, try again")
                    except ValueError:
                        messagebox.showwarning(title="Error!", message="Something went wrong, try again")

                par = [i for i in participants]

                game_start = datetime.fromtimestamp(active_game['gameStartTime'] / 1000)
                game_start = game_start.strftime("%m/%d/%Y - %H:%M:%S")
                game_duration = round(active_game['gameLength'] / 60)

                data = {
                    'Summoner': par,
                    'Elo': elos,
                    'Division': rank,
                    'League Points': l_points,
                    'Wins': wins,
                    'Losses': losses,
                    'Total Games': total_g,
                    'Win Rate': win_r
                }

                def copyy():
                    try:
                        curItem = my_tree2.focus()
                        item = my_tree2.item(curItem)
                        self.new_win2.clipboard_clear()
                        self.new_win2.clipboard_append(item['values'][0])
                        messagebox.showinfo(title="Info!", message="Copied succesfully!")
                    except IndexError:
                        messagebox.showwarning(title="Atention!", message="You must make a selection.")

                # Create pandas Dataframe
                try:
                    df = pd.DataFrame(data)
                except ValueError:
                    messagebox.showwarning(title="Error!", message="Something went wrong, try again")
                else:

                    my_tree2 = ttk.Treeview(self.new_win2, selectmode=BROWSE, style="mystyle.Treeview")
                    my_tree2["column"] = list(df.columns)
                    my_tree2["show"] = "headings"

                    for column in my_tree2["column"]:
                        my_tree2.heading(column, text=column)

                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        my_tree2.insert("", END, values=row)

                    my_tree2.column("Summoner", width=150, minwidth=150, anchor=CENTER)
                    my_tree2.column("Elo", width=140, minwidth=140, anchor=CENTER)
                    my_tree2.column("Division", width=100, minwidth=100, anchor=CENTER)
                    my_tree2.column("League Points", width=140, minwidth=140, anchor=CENTER)
                    my_tree2.column("Wins", width=80, minwidth=80, anchor=CENTER)
                    my_tree2.column("Losses", width=80, minwidth=80, anchor=CENTER)
                    my_tree2.column("Total Games", width=140, minwidth=140, anchor=CENTER)
                    my_tree2.column("Win Rate", width=120, minwidth=120, anchor=CENTER)

                    m = Menu(self.new_win2, tearoff=0)
                    m.add_command(label="View Player OPGG", command=self.view_opgg)
                    m.add_command(label="Copy Summoner Name", command=copyy)

                    def do_popup(event):
                        try:
                            m.tk_popup(event.x_root, event.y_root)
                        finally:
                            m.grab_release()

                    my_tree2.bind("<Button-3>", do_popup)

                    my_tree2.grid(row=0, column=0)

                    self.new_win2.title(f'{me_now} is now playing! '
                                        f'[Game Start: {game_start}] [Game Actual Duration: {game_duration} minutes]')

                    self.savePlayers()
                    self.window.grab_set()
                    self.new_win2.deiconify()

    def top_Players(self):
        """Pop up window that shows a Treeview with the best players of the specified region"""

        if self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must specify the Region.")
        else:
            top = self.watcher.league.challenger_by_queue(self.combo.get(), 'RANKED_SOLO_5x5')

            name = [i['summonerName'] for i in top['entries']]
            points = [i['leaguePoints'] for i in top['entries']]
            wins = [i['wins'] for i in top['entries']]
            losses = [i['losses'] for i in top['entries']]

            data = {
                'Summoner': name,
                'League Points': points,
                'Wins': wins,
                'Losses': losses,
            }

            df = pd.DataFrame(data)
            df.sort_values(by=['League Points'], ascending=False, inplace=True)

            my_tree3 = ttk.Treeview(self.new_win3, selectmode=BROWSE, style="mystyle.Treeview")
            my_tree3["column"] = list(df.columns)
            my_tree3["show"] = "headings"

            scroll = Scrollbar(self.new_win3, orient="vertical", command=my_tree3.yview)
            scroll.grid(row=0, column=1, sticky=NS)

            my_tree3.configure(yscrollcommand=scroll.set)

            for column in my_tree3["column"]:
                my_tree3.heading(column, text=column)

            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                my_tree3.insert("", END, values=row)

            my_tree3.column("Summoner", width=150, minwidth=150, anchor=CENTER)
            my_tree3.column("League Points", width=140, minwidth=140, anchor=CENTER)
            my_tree3.column("Wins", width=100, minwidth=100, anchor=CENTER)
            my_tree3.column("Losses", width=100, minwidth=100, anchor=CENTER)

            my_tree3.grid(row=0, column=0)

            def copyy():
                try:
                    curItem = my_tree3.focus()
                    item = my_tree3.item(curItem)
                    self.window.clipboard_clear()
                    self.window.clipboard_append(item['values'][0])
                    messagebox.showinfo(title="Info!", message="Copied succesfully!")
                except IndexError:
                    messagebox.showwarning(title="Warning!", message="You must make a selection.")

            def opgg():
                curItem = my_tree3.focus()
                if curItem:
                    item = my_tree3.item(curItem)
                    if self.combo.get() == 'EUW1':
                        region = 'euw'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'NA1':
                        region = 'na'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'BR1':
                        region = 'br'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'JP1':
                        region = 'jp'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'EUN1':
                        region = 'eune'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'KR':
                        region = 'kr'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'LA1':
                        region = 'lan'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'LA2':
                        region = 'las'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'OC1':
                        region = 'oce'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'TR1':
                        region = 'tr'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'RU':
                        region = 'ru'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                else:
                    messagebox.showwarning(title="Warning!", message="You must select an element.")

            def info():
                curItem = my_tree3.focus()
                item = my_tree3.item(curItem)

                self.my_region = self.combo.get()
                # We get the Summoner info
                try:
                    me = self.watcher.summoner.by_name(self.my_region, item['values'][0])
                    my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
                    total_games = my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses']
                    winrate = my_ranked_stats[0]['wins'] / (
                            my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                    winrate = round(winrate * 100)

                    messagebox.showinfo(title=f"{item['values'][0]}",
                                        message=f"""
Elo: {my_ranked_stats[0]['tier']}
League Points: {my_ranked_stats[0]['leaguePoints']}
Wins: {my_ranked_stats[0]['wins']}
Losses: {my_ranked_stats[0]['losses']}
Total Games: {total_games}
Win Rate: {winrate}%
""")
                except HTTPError:
                    messagebox.showerror(title='Error!', message='Summoner selected region is invalid.')
                except IndexError:
                    messagebox.showerror(title='Error!', message="Summoner selected region is invalid.")

            m = Menu(self.new_win3, tearoff=0)
            m.add_command(label="Copy Summoner Name", command=copyy)
            m.add_command(label="Search Ranked Info", command=info)
            m.add_command(label="Search Player OPGG", command=opgg)

            def do_popup(event):
                try:
                    m.tk_popup(event.x_root, event.y_root)
                finally:
                    m.grab_release()

            my_tree3.bind("<Button-3>", do_popup)

            self.new_win3.title(f'Top {len(name)} Challenger Players of {self.combo.get()}')
            self.savePlayers()

            self.window.grab_set()
            self.new_win3.deiconify()

    def savePlayers(self):
        try:
            with open('summoners.txt', mode='a') as f:
                f.writelines(f"{self.text.get()} | {self.combo.get()}\n")
            f.close()
        except UnicodeEncodeError:
            with open('summoners.txt', mode='a', encoding='utf-8') as f:
                f.writelines(f"{self.text.get()} | {self.combo.get()}\n")
            f.close()

    def save_list_Players(self,name):




        l = list(set(self.listesansdoublon))
        try:

            with open('players_list.txt', mode='a+') as f:

                f.writelines(f"{name}\n")
                # lines = f.readlines()
                # line_set= set(lines)
                # for line in line_set:
                #     f.write(line)
            f.close()
        except UnicodeEncodeError:

            with open('players_list.txt', mode='a+', encoding='utf-8') as f:

                f.writelines(f"{name}\n")
                # lines = f.readlines()
                # line_set= set(lines)
                # for line in line_set:
                #     f.write(line)
            f.close()



    def loadPlayers(self):
        self.listbox.delete(0, END)
        scroll = Scrollbar(self.new_win4)
        scroll.grid(row=0, column=1, sticky=NS)
        try:
            with open('summoners.txt', mode='r', encoding='utf-8') as f:
                content = f.readlines()
            f.close()
        except FileNotFoundError:
            messagebox.showwarning(title="Warning!", message="There are not recent searchs or"
                                                              " not 5 searches at least.")
        except UnicodeEncodeError:
            with open('summoners.txt', mode='r', encoding='euc_kr') as f:
                content = f.readlines()
            f.close()
        else:

            final_content = list(dict.fromkeys(content))

            f_cont = []
            for i in final_content:
                f_cont.append(i.replace('\n', ''))

            strings = [x for x in f_cont if x]

            self.listbox.config(borderwidth=2, activestyle=NONE, fg="white",
                                bg="#1d238c", font=("Arial", 15, "bold"), selectforeground="#03f8fc",
                                selectbackground="#03052e", selectborderwidth=2, selectmode=SINGLE,
                                highlightbackground='#313cf7', highlightcolor='#2029c7', yscrollcommand=scroll.set,
                                width=33)
            scroll.config(command=self.listbox.yview)
            btn = Button(self.new_win4, text="Limpiar historial", command=self.limpiarHist,
                         font=('Comic Sans MS', 14, 'bold'), background='#858aed')
            btn.grid(row=1, column=0, sticky=EW, columnspan=2)

            if len(strings) >= 5:
                self.listbox.insert(END, *strings)
                self.listbox.grid(row=0, column=0)
                self.new_win4.title(f'Last {len(strings)} searches')
                self.new_win4.config(bg='blue')

                self.window.grab_set()
                self.new_win4.deiconify()

            else:
                messagebox.showwarning(title="Warning!", message="There are not 5 searches at least.")

    def double_click2(self, event):
        """Called when user double clicks element from ListBox"""
        self.text.delete(0, 'end')
        content = self.listbox.get(self.listbox.curselection())
        content = content.split(sep=' | ')
        self.window.clipboard_clear()
        self.window.clipboard_append(content[0])
        self.text.insert(0, content[0])
        self.combo.set(content[1])
        self.graph_by_hour('Samedi')

    def double_click3(self, event):
        """Called when user double clicks element from ListBox"""
        curItem = self.my_tree.focus()
        item = self.my_tree.item(curItem)

        self.my_region = self.combo.get()
        # We get the Summoner info
        try:
            me = self.watcher.summoner.by_name(self.my_region, item['values'][0])
            my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
            total_games = my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses']
            winrate = my_ranked_stats[0]['wins'] / (
                    my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
            winrate = round(winrate * 100)

            messagebox.showinfo(title=f"{item['values'][0]}",
                                message=f"""
                Elo: {my_ranked_stats[0]['tier']}
                League Points: {my_ranked_stats[0]['leaguePoints']}
                Wins: {my_ranked_stats[0]['wins']}
                Losses: {my_ranked_stats[0]['losses']}
                Total Games: {total_games}
                Win Rate: {winrate}%
                """)
        except HTTPError:
            messagebox.showerror(title='Error!', message='Summoner selected region is invalid.')
        except IndexError:
            messagebox.showerror(title='Error!', message="Summoner selected region is invalid.")
        except KeyError:
            messagebox.showerror(title='Error!', message="Summoner selected region is invalid.")
        except UnicodeEncodeError:
            messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")

    def limpiarHist(self):
        y = messagebox.askyesno(title='Atention!', message='Are you sure you want to delete the search history?')
        if y:
            try:
                os.remove('summoners.txt')
            except FileNotFoundError:
                print("File Not Found")
            else:
                self.listbox.delete(0, END)
                messagebox.showinfo(title="Info", message="Search history deleted succesfully")
                self.on_closing4()

    def view_opgg(self):
        curItem = self.my_tree.focus()
        if curItem:
            item = self.my_tree.item(curItem)
            if self.combo.get() == 'EUW1':
                region = 'euw'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'NA1':
                region = 'na'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'BR1':
                region = 'br'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'JP1':
                region = 'jp'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'EUN1':
                region = 'eune'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'KR':
                region = 'kr'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'LA1':
                region = 'lan'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'LA2':
                region = 'las'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'OC1':
                region = 'oce'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'TR1':
                region = 'tr'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'RU':
                region = 'ru'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
        else:
            messagebox.showwarning(title="Warning!", message="You must select an element.")


if __name__ == "__main__":
    LI = LoLInterface()

