from tkinter import *
from tkcalendar import Calendar
import AMERGEKAI
import datetime
import get_date_etHeure


def init_calendar(name):

       root = Tk()

       root.geometry("400x400")

       cal = Calendar(root, selectmode='day',
                     year=2022, month=6,
                     day=22)

       db = get_date_etHeure.HeureEtDate(name)
       dict_an = {}
       for i in range(1,13):
              mois = f"{i:02d}"
              dict_match = db.get_dict_num(mois,"2022")
              # print(dict_match)
              if dict_match:
                     dict_an[f"{i}"] = dict_match
       print(dict_an)
       print(list(dict_an.keys()))
       print(list(dict_an.values()))
       for it in dict_an.items():
              print(f"Le {it[0]} est {it[1]}")
              for i in it[1].items():
                     print(f"le {i[0]} il a jouer {i[1]} matches")
                     list_date = i[0].split("/")
                     print(list_date)
       db.database.select_all_data("Swipe04")

       cal.pack(pady=20)
       # day = datetime.date(2022, 6, 20)
       # cal.calevent_create(day, "", tags="hi")
       # cal.tag_config("hi", background="red")
       Button(root, text="View Graph",
              command=grad_date).pack(pady=20)

       date = Label(root, text="")
       date.pack(pady=20)


def grad_date():
       datetime.date.config(text="Selected Date is: " )


