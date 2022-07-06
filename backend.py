import mysql.connector
import re
import random
import string
import datetime
import time
import winsound
import pyttsx3
engine = pyttsx3.init()
import requests
import os


def refresh_list():

    mydb = mysql.connector.connect(
      host="*****",
      user="****",
      password="*************",
      database="*******"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tasks order by timestamp")

    global lst
    lst = mycursor.fetchall()

    mycursor.close()

    global uptodate_lst
    uptodate_lst = []

    if len(lst) != 0:
        total_rows = len(lst)
        total_columns = len(lst[0])

        ######### Modifying the dates ############


        lst = [list(ele) for ele in lst]


        for i in range(total_rows):
            for j in range(total_columns):
                if j==2:
                    d_db = datetime.datetime.strptime(str(lst[i][j]), '%Y-%m-%d %H:%M:%S')
                    d_curr = datetime.datetime.now()
                    if (d_db.year>=d_curr.year and d_db.month>=d_curr.month and d_db.day>=d_curr.day and d_db.hour>=d_curr.hour and d_db.minute>=d_curr.minute) or d_db>d_curr:   # I have updated here:
                        uptodate_lst.append(lst[i])


        if len(uptodate_lst)!=0:
            total_rows_uptodate = len(uptodate_lst)
            total_columns_uptodate = len(uptodate_lst[0])

            for i in range(total_rows_uptodate):
                for j in range(total_columns_uptodate):
                    if j==2:
                        uptodate_lst[i][j] = str(uptodate_lst[i][j])
                        d = datetime.datetime.strptime(uptodate_lst[i][j], '%Y-%m-%d %H:%M:%S')
                        uptodate_lst[i][j] = d

        else:
            print("Empty Up to date list")
            return

    else:
        print("Empty List")
        return


    ##########################################

def Text_to_speech():
    Message = uptodate_lst[0][1]
    i=10
    while i!=0:
        engine.say(Message)
        engine.runAndWait()
        i=i-1
        time.sleep(1)
    time.sleep(35)
    return


def telegram_bot_sendtext(bot_message):

    bot_token = '*******************'
    bot_chatID = '************' 
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return


def alarm():
    while True:
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_min = current_time.minute
        current_day = current_time.day
        current_month = current_time.month
        current_year = current_time.year
        date = current_time.strftime("%d/%m/%Y")
        if len(uptodate_lst)!=0 :
            print(uptodate_lst)
            if current_day==uptodate_lst[0][2].day and current_month==uptodate_lst[0][2].month and current_year==uptodate_lst[0][2].year and current_hour==uptodate_lst[0][2].hour and current_min == (uptodate_lst[0][2].minute or (uptodate_lst[0][2].minute + 1) or (uptodate_lst[0][2].minute - 1))  :
                print("Time to Wake up")
                telegram_bot_sendtext(uptodate_lst[0][1])
                Text_to_speech()

            break
            return
        return


def renew_screen():
   # for mac and linux(here, os.name is 'posix')
   time.sleep(2)
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')


while(True):
    refresh_list()
    alarm()
    renew_screen()
