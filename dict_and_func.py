dict_champions = {'Aatrox':0, 'Ahri':1 ,'Akali':1 , 'Akshan':0,'Alistar':0,'Amumu':0, 'Anivia':1, 'Annie':1, 'Aphelios':0, 'Ashe':1, 'AurelionSol':0, 'Azir':0 ,'Bard':0, 'Belveth':1,'Blitzcrank':0, 'Brand':0,'Braum':0,'Caitlyn':1,'Camille':1 ,'Cassiopeia':1 ,'Chogath':0, 'Corki':0, 'Darius':0,'Diana':1,'DrMundo':0,'Draven':0 ,'Ekko':0,'Elise':1, 'Evelynn':1,'Ezreal':0,'Fiddlesticks':0, 'Fiora':1, 'Fizz':0, 'Galio':0,'Gangplank':0,'Garen':0,'Gnar':0,'Gragas':0,'Graves':0,'Gwen':1,'Hecarim':0,'Heimerdinger':0,'Illaoi':0,'Irelia':1,'Ivern':0,'Janna':1,'JarvanIV':0 ,'Jax':0,'Jayce':0, 'Jhin':0,'Jinx':1,'Kaisa':1,'Kalista':1,'Karma':1,'Karthus':0,'Kassadin':0,'Katarina':1,'Kayle':1,'Kayn':0,'Kennen':0,'Khazix':0,'Kindred':0,'Kled':0,
                  'KogMaw':0,'LeBlanc':1,'LeeSin':0,'Leona':1,'Lissandra':1,'Lillia':1,'Lucian':0,'Lulu':1,'Lux':1,'MasterYi':0,'Malphite':0,'Malzahar':0,'Maokai':0,'MissFortune':1,'Mordekaiser':0,'Morgana':1,'Nami':1,'Nasus':0,'Nautilus':0,'Nidalee':1,'Neeko':1,'Nocturne':0,'Nunu':0,'Olaf':0,'Orianna':1,'Ornn':0,'Pantheon':0,'Poppy':1,'Pyke':0,'Qiyana':1,
                  'Quinn':1,'Rakan':0,'Rammus':0,'RekSai':0,'Rell':1,'Renekton':0,'Renata':1,'Rengar':0,'Riven':1,'Rumble':0,'Ryze':0,'Samira':1,'Sejuani':1,'Senna':1,'Seraphine':1,'Sett':0,'Shaco':0,'Shen':0,'Shyvana':1,'Singed':0,'Sion':0,'Sivir':1,'Skarner':1,'Sona':1,'Soraka':1,'Swain':0,'Sylas':0,'Syndra':0,'TahmKench':0,'Taliyah':1,'Talon':0,'Taric':0,'Teemo':0,'Thresh':0 ,'Tristana':1,'Trundle':0,'Tryndamere':0,'TwistedFate':0,'Twitch':0,'Udyr':0,'Urgot':0,'Varus':0,'Vayne':1,'Veigar':0,'Velkoz':0,'Vex':1,'Vi':1,'Viego':0,'Viktor':0,'Vladimir':0,'Volibear':0,'Warwick':0,'MonkeyKing':0,'Xayah':1,'Xerath':0,'XinZhao':0,'Yasuo':0,'Yone':0,'Yorick':0,'Yuumi':1,'Zac':0,'Zed':0,'Zeri':1,'Ziggs':0,'Zilean':0,'Zoe':1,'Zyra':1}

self.champ_dict = dict_champions#dans intit

    def determine_role_by_puid(self,puid,games):#coute beaucoup de requêtes
        roles = []
        main_role = None

        matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid)
        list_containing_all_roles = []
        for a in range(games):
            temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
            role = temp_match_detail['info']['participants'][self.find_position_of_a_player(puid,temp_match_detail['metadata']['participants'])]['individualPosition']
            list_containing_all_roles.append(role)
        frequency = {'MIDDLE':0,'TOP':0,'JUNGLE':0,'SUPPORT':0,'BOTTOM':0}
        for elem in list_containing_all_roles:
            if elem in frequency:
                frequency[elem] +=1
            else:
                frequency[elem] = 1

        for keys,values in frequency.items():
            if values/games > 0.7:
                main_role = keys

        return main_role


    def percentage_of_female_caracters_played(self,puid,games):
        matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid,count=100)
        list_containing_all_champs = []
        percentage = 0
        for a in range(games):
            print(a)
            temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])

            champ = temp_match_detail['info']['participants'][self.find_position_of_a_player(puid,temp_match_detail['metadata']['participants'])]['championName']
            print(champ)
            print(self.watcher.summoner.by_puuid(self.my_region, puid)['name'])
            time.sleep(2)
            if self.champ_dict[champ] == 1:
                percentage +=1
            list_containing_all_champs.append(champ)
        percentage = percentage/games
        print(percentage)
        print(list_containing_all_champs)
        return percentage

    def percentage_of_role_played(self,puid,role,games):
        matches = self.watcher.match.matchlist_by_puuid(self.my_region, puid,count=100)
        percentage = 0
        for a in range(games):
            temp_match_detail = self.watcher.match.by_id(self.my_region, matches[a])
            match_role = temp_match_detail['info']['participants'][self.find_position_of_a_player(puid,temp_match_detail['metadata']['participants'])]['individualPosition']
            time.sleep(1)
            if match_role == role:
                percentage+=1

        percentage = percentage/games
        print(percentage)
        return percentage
