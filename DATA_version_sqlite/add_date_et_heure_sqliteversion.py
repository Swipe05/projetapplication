from lib2to3.refactor import get_all_fix_names
from sqlite3 import Timestamp
import interact_with_db
#import AMERGEKAI
from datetime import datetime
import time
import matplotlib.pyplot as plt

class HeureEtDate:
    def __init__(self, pseudo_name) -> None:
        self.pseudo = pseudo_name
        self.database = interact_with_db.Data_base("LienMinh.db")

    def timestamp_to_date(self, timestamp):
        dmy = datetime.fromtimestamp(timestamp).strftime('%m/%d/%y')
        DMY = dmy.split("/")
        return DMY
    # format:  "day/month/year"
    def date_to_timestamp(self, MDY):
        return time.mktime(datetime.strptime(MDY, "%m/%d/%Y").timetuple())

    # select match_start_time, match_end_time, number_of_match_in_a_day, timestamp
    # datemonthyear format is %d/%m/%y
    def get_data_of_a_day(self, monthdayyear, table ="Partie"):
        return self.database.select_data_with_condition(table,f" date LIKE   '{monthdayyear}%' AND summonerName = '{self.pseudo}'",('timestamp','date'))

    def get_all_data_a_month(self, month, year,table="Partie"):
        return self.database.select_data_with_condition(table,f" date LIKE   '%{month}%{year}%' AND summonerName = '{self.pseudo}' ",('timestamp','date'))

    def get_number_of_match_a_month(self, month, year):
        return  len(self.get_all_data_a_month(month,year))

    def get_number_of_match_a_day(self, month , day ,  year):
        rq = f"{month}/{day}/{year}"
        return len(self.get_data_of_a_day(rq))

    def get_dict_num(self, month, year):
        dict_return = {}
        data = self.get_all_data_a_month(month, year)
        for element in data:
            MdateY_heure = element[1].split(" - ")
            if MdateY_heure[0] in dict_return.keys():
                dict_return[MdateY_heure[0]] += 1
            else:
                dict_return[MdateY_heure[0]] = 1
        return dict_return
    def get_heure_of_date(self, month, day, year):
        rq = f"{month}/{day}/{year}"
        data = self.get_data_of_a_day(rq)
        return [ (x[1].split(" - "))[1] for x in data]

    def get_list_num_heure(self, monthdayyear, tb_name="Partie"):
        data = self.database.select_data_with_condition( tb_name,f" date LIKE   '{monthdayyear}%' AND summonerName='{self.pseudo}'",('timestamp', 'date'))

        data = self.database.select_data_with_condition(tb_name,
                                                        f" date LIKE   '{monthdayyear}%' AND summonerName='{self.pseudo}'",
                                                        ('timestamp', 'date'))

        all_hours = []
        for a in data:
            all_hours.append(datetime.utcfromtimestamp(float(a[0])).strftime('%H'))

            dt_object = datetime.fromtimestamp(float(a[0]))

        self.graph_by_hours(all_hours)

        all_hours = []
        for a in data:
            all_hours.append(datetime.utcfromtimestamp(float(a[0])).strftime('%H'))

            dt_object = datetime.fromtimestamp(float(a[0]))

        self.graph_by_hours(all_hours)

        li = []
        for i in data:
            li.append(i[1])
        l = "\n".join(li)
        return l

    def graph_by_hours(self,tab):
        left = [x for x in range(24)]

        # heights of bars
        tick_label = [x for x in range(24)]  # nb de games par lapse de temps

        # labels for bars
        height = []  # laspe de temps
        for x in range(24):
            height.append(0)

        for x in tab:
            height[int(x)] += 1

        # plotting a bar chart
        plt.bar(left, height, tick_label=tick_label,
                width=0.8, color=['blue', 'green'])

        # naming the x-axis
        plt.xlabel('heure de la journée')
        # naming the y-axis
        plt.ylabel('nombre de partie jouées')
        # plot title
        plt.title('')

        # function to show the plot
        plt.show()



# get_swipe = HeureEtDate("HentEye")