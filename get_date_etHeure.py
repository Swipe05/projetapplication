import interact_with_db
import AMERGEKAI
from datetime import datetime
import time

class HeureEtDate:
    def __init__(self, pseudo_name) -> None:
        self.pseudo = pseudo_name
        self.database = interact_with_db.Data_base("LienMinh.db")

    def timestamp_to_date(self, timestamp):
        dmy = datetime.fromtimestamp(timestamp).strftime('%d/%m/%y')
        DMY = dmy.split("/")
        return DMY
    # format:  "day/month/year"
    def date_to_timestamp(self, DMY):
        return time.mktime(datetime.strptime(DMY, "%d/%m/%Y").timetuple())

    # select match_start_time, match_end_time, number_of_match_in_a_day, timestamp
    # datemonthyear format is %d/%m/%y
    def select_data(self, daymonthyear):
        return self.database.select_data_with_condition(self.pseudo,f" date LIKE   '{daymonthyear}%'",('timestamp','date'))



get_swipe = HeureEtDate("TTSiHades")
get_swipe.select_data("04/03/2022")