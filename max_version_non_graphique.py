#import discord
import requests
import riotwatcher
from datetime import datetime

name = "Swipe04"
name_max="Evangelinebe"
api_key = "RGAPI-794efd89-94df-4d6b-9563-d88d1fff37d9"



def process(name):
    def recherche_id(name):

        urlname = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"

        composition = urlname + name + "?api_key=" + api_key
        connection1 = requests.get(composition)
        connection1.json()

        summonerid = connection1.json()["id"]
        accountId = connection1.json()["accountId"]
        summpuuid = connection1.json()["puuid"]
        return summpuuid


    def find_position_of_a_player(puuid, lpart):
        x = 0

        for i in (lpart):

            if i != puuid:

                x = x + 1
            else:
                # print("we found")
                return (x)
        return


    historyid = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
    h2 = "/ids"
    compo2 = historyid + recherche_id(name) + h2 + "?api_key=" + api_key + "&" + "count=100"
    #print(compo2)
    print(recherche_id("Evangelinebe"))

    h1 = requests.get(compo2)

    # boucle for apres pour parcourir les games

    print(h1.json())


    nombre_game_int = 0
    score_miserable = [0, 0, 0]
    perso_miserable = 'GG'
    print("idgame",h1.json()[0])
    #print("testdate", riotwatcher._apis.league_of_legends.MatchApiV5.timeline_by_match("EUW1","EUW1_5918272588"))

    for j in range(10):
        #print(h1.json()[j])
        #print(h1.json()[j])


        gameinfo = "https://europe.api.riotgames.com/lol/match/v5/matches/"
        compo3 = gameinfo + h1.json()[j] + "?api_key=" + api_key
        print(compo3)
        test = requests.get(compo3)

        listeparticipant = test.json()["metadata"]["participants"]
        # print(listeparticipant)

        pos = find_position_of_a_player(recherche_id(name),listeparticipant)

        morts = test.json()["info"]["participants"][pos]["deaths"]

        kill = test.json()["info"]["participants"][pos]["kills"]

        match_start = test.json()["info"]["gameStartTimestamp"]
        match_start = (test.json()["info"]["gameEndTimestamp"])/1000
        match_dat1 = datetime.fromtimestamp(match_start)
        match_date = match_dat1.strftime("%m/%d/%Y - %H:%M:%S")
        print("date_time:", match_date)



        assist = test.json()["info"]["participants"][pos]["assists"]
        perso = test.json()["info"]["participants"][pos]["championName"]
        print(kill, morts, assist,perso)

        #print("Nombre de kill", kill)
        #print("Nombre de mort", morts)
        #print("Nombre d'assists", assist)
        if morts>0:
            kda = (kill + assist) / morts
            if kda < 1.2:
                #print("ce joueur a int ")
                nombre_game_int = nombre_game_int + 1
                score_miserable = [kill,morts,assist]
                perso_miserable = perso





    #print(name, "a INT COMME UN ENCULER,", nombre_game_int, "de ces 10 dernieres games",score_miserable[0],score_miserable[1],score_miserable[2])
    return nombre_game_int,score_miserable,perso_miserable

#print(process("Evangelinebe")[0])
print(process("Evangelinebe"))


# class MyClient(discord.Client):
# 
# 
# 
#     async def on_ready(self):
#         print('Logged in as')
#         print(self.user.name)
#         print(self.user.id)
#         print('------')
# 
# 
#     async def on_message(self, message):
#         leo_id = "225688497955012610"
#         maxime_id= "378946612552007682"
#         este_id="194884866951610368"
#         corenid="337213918818598914"
#         curr_id="1"
#         # we do not want the bot to reply to itself
#         if message.author.id == self.user.id:
#             return
# 
#         if message.content.startswith('!'):
#             stock = message.content
#             print(stock)
# 
#             stock2 = stock[1:]
#             print(stock2)
#             nbgameint,kdaint,persoint = process(stock2)
# 
#             if message.content.startswith('!Swipe04'):
#                 curr_id =leo_id
#                 await message.channel.send(file=discord.File('leo.jpg'))
#             if message.content.startswith('!Evangelinebe'):
#                 curr_id = maxime_id
#                 await message.channel.send(file=discord.File('cassio.jpg'))
# 
#             if message.content.startswith('!EasyPotatoEU'):
#                 curr_id = este_id
#                 await message.channel.send(file=discord.File('brand.jpg'))
# 
#             if message.content.startswith('!Marto Thoteur'):
#                 curr_id = corenid
#                 await message.channel.send(file=discord.File('velk.gif'))
# 
# 
#             if nbgameint == 0:
#                 await message.channel.send(file=discord.File('ahri.gif'))
#                 await message.channel.send("Ce joueur est exemplaire il n'a INT aucune des 10 dernieres games")
# 
#             if nbgameint >0:
#                 if curr_id=="1":
#                     await message.channel.send(f' {stock2} a INT COMME UN ENCULER {nbgameint} de ces 10 dernieres games avec des KDA NUL A CHIER COMME {kdaint[0]}/{kdaint[1]}/{kdaint[2]} avec {persoint} :relieved: MAKOMÉ?????')
#                 else:
#                     await message.channel.send(f' <@{curr_id}> a INT COMME UN ENCULER {nbgameint} de ces 10 dernieres games avec des KDA NUL A CHIER COMME {kdaint[0]}/{kdaint[1]}/{kdaint[2]} avec {persoint} :relieved: MAKOMÉ?????')
# 




#client = MyClient()
#client.run('OTgxNjE2MzUyMjk5MjE2OTI2.G2t1-j.uJp_WGJYVeomF6nw02hX3A_Q_xUz79WL_o8VLA')
