from lib2to3.refactor import get_all_fix_names
from sqlite3 import Timestamp
import interact_with_db
import AMERGEKAI
from datetime import datetime
import time

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
    def get_data_of_a_day(self, monthdayyear):
        return self.database.select_data_with_condition(self.pseudo,f" date LIKE   '{monthdayyear}%'",('timestamp','date'))

    def get_all_data_a_month(self, month, year):
        return self.database.select_data_with_condition(self.pseudo,f" date LIKE   '%{month}%{year}%'",('timestamp','date'))

    def get_number_of_match_a_month(self, month, year):
        return  len(self.get_all_data_a_month(month,year))

    def get_number_of_match_a_day(self, month , day ,  year):
        rq = f"{month}/{day}/{year}"
        return len(self.get_data_of_a_day(rq))

    def get_dict_num(self, month, year):
        dict_return = {}
        data = self.get_all_data_a_month(month, year)
        # print(data)
        # all_day_heure = [x[1] for x in data]

        # all_day = [(x.split(" - "))[0] for x in all_day_heure]
        for element in data:
            MdateY_heure = element[1].split(" - ")
            if MdateY_heure[0] in dict_return.keys():
                dict_return[MdateY_heure[0]] += 1
            else:
                dict_return[MdateY_heure[0]] = 1
        return dict_return


get_swipe = HeureEtDate("HentEye")
print(get_swipe.get_dict_num("04","2022"))