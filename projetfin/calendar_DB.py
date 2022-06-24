from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from main import  LoLInterface
import customtkinter as ctkp
import datetime
#import get_date_et_heure
import get_date_et_heure
def init_calendar(name):

            root = Tk()

            root.geometry("400x500")
            style = ttk.Style(root)
            style.theme_use('clam')
            root.config(pady=10, padx=10, background='#2F2F2F')
            cal = Calendar(root, background="black", disabledbackground="black", bordercolor="black",
                           headersbackground="black", normalbackground="black", foreground='white',
                           normalforeground='white', headersforeground='white')
            cal.config(background="black")

            cal = Calendar(root, selectmode='day',
                           year=2022, month=6,
                           day=22)
            db = get_date_et_heure.HeureEtDate(name)
            dict_an = {}
            for i in range(1, 13):
                mois = f"{i:02d}"
                dict_match = db.get_dict_num(mois, "2022")
                print(dict_match)
                if dict_match:
                    dict_an[f"{i}"] = dict_match
            #print(dict_an)
            #print(list(dict_an.keys()))
            #print(list(dict_an.values()))
            for it in dict_an.items():
                print(f"Le {it[0]} est {it[1]}")
                for i in it[1].items():
                    print(f"le {i[0]} il a jouer {i[1]} matches")
                    if (i[1] < 3 and i[1] != 0):
                        list_date = i[0].split("/")
                        day = datetime.datetime.strptime(i[0], '%m/%d/%Y')
                        cal.calevent_create(day, "", tags="ho")
                        cal.tag_config("ho", background="green")
                    elif (i[1] >= 3 and i[1] != 0 and i[1]<5):
                        list_date = i[0].split("/")
                        day = datetime.datetime.strptime(i[0], '%m/%d/%Y')
                        cal.calevent_create(day, "", tags="hi")
                        cal.tag_config("hi", background="orange")
                    elif (i[1] >= 5  and i[1] != 0 and i[1]<10):
                        list_date = i[0].split("/")
                        day = datetime.datetime.strptime(i[0], '%m/%d/%Y')
                        cal.calevent_create(day, "", tags="ha")
                        cal.tag_config("ha", background="red")
                    elif (i[1] >= 10  and i[1] != 0):
                        list_date = i[0].split("/")
                        day = datetime.datetime.strptime(i[0], '%m/%d/%Y')
                        cal.calevent_create(day, "", tags="hy")
                        cal.tag_config("hy", background="purple")


            cal.pack(pady=20)

            def grad_date(db):

                list_date = cal.get_date().split("/")
                list_date[0] = f"{int(list_date[0]):02d}"
                list_date[1] = f"{int(list_date[1]):02d}"
                list_date[2] = "20" + list_date[2]
                date2 = "/".join(list_date)
                print(date2)

                date.config(text=f"Game from Selected Date :  {db.get_list_num_heure(date2)}")
            '''day = datetime.date(2022, 7, 20)
            cal.calevent_create(day, "", tags="hi")
            cal.tag_config("hi", background="red")'''
            ctkp.CTkButton(root,text_font=('Helvetica Neue', 12, 'bold'), fg_color=("#2F2F2F"),
                                          border_width=3,
                                          corner_radius=8,
                                          text="Show Time",
                   command=lambda:grad_date(db),background='#858aed',
                                          text_color='white', border_color='#005A34',
                    hover_color='#005A34').pack(pady=20)

            date = Label(root, text="",background='#2F2F2F',fg='white')
            date.pack(pady=20)

