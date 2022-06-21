from tkinter import *
from tkcalendar import Calendar
from lolapi import  LoLInterface
import datetime
def init_calendar():

            root = Tk()

            root.geometry("400x400")

            cal = Calendar(root, selectmode='day',
                           year=2022, month=6,
                           day=22)

            cal.pack(pady=20)
            day = datetime.date(2022, 6, 20)
            cal.calevent_create(day, "", tags="hi")
            cal.tag_config("hi", background="red")
            Button(root, text="View Graph",
                   command=grad_date).pack(pady=20)

            date = Label(root, text="")
            date.pack(pady=20)


def grad_date():
    date.config(text="Selected Date is: " )


