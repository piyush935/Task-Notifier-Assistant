try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    from tkinter import messagebox
    import mysql.connector
    import re
    import random
    import string
    from tkcalendar import *
    import datetime


except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x750")
        self.title("Task Notifier Assistant")


        self.title_font = tkfont.Font(family='Acmefont', size=25)
        self.describe_font = tkfont.Font(family='Verdana', size=15)
        self.iconbitmap('favicon.ico')


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.title_font = tkfont.Font(family='Acmefont', size=30)
        self.describe_font = tkfont.Font(family='Verdana', size=15)

        heading = tk.Label(self,text="Task Notifier Assistant",font=self.title_font)
        heading.pack(padx=20,pady=110)

        button1 = tk.Button(self, text="Schedule New Task",font=self.describe_font,
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="View All Tasks",font=self.describe_font,
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack(pady = 50)
        button2.pack(pady = 50)

        footer = tk.Label(self, text = "Made with love   ❤️by Group 1",relief="sunken", bd=1)
        footer.pack(side="bottom", fill="x")



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.title_font = tkfont.Font(family='Acmefont', size=30)
        self.describe_font = tkfont.Font(family='Verdana', size=10)

        ###################

        temp_label = tk.Label(self,text="")
        temp_label.pack(padx=20,pady=10)

        name_label = tk.Label(self,text="Enter the Name of the task ",font=self.describe_font)
        name_label.pack(padx=20,pady=10)

        name = tk.Entry(self, width = 30)
        name.pack(padx=20,pady=5)

        def grab_name():
            global name_set
            name_set = name.get()
            if len(name_set)!=0:
                success_msg1 = "Entered the event : " + name_set
                messagebox.showinfo("Success",success_msg1)
            else:
                messagebox.showinfo("Error","Empty Field")



        name_button =  tk.Button(self, text="set the name", command=grab_name,font=self.describe_font)
        name_button.pack(pady=10)

        now = datetime.datetime.now()

        cal = Calendar(self,date_pattern='dd/mm/y', selectmode="day", year=int(now.strftime("%Y")), month=int(now.strftime("%m")), day=int(now.strftime("%d")))
        cal.pack(pady=20)

        list1 = list(range(24))
        list2 = list(range(60))

        clicked1 = tk.StringVar()
        clicked1.set("hour")

        drop1 = tk.OptionMenu(self, clicked1, *list1)
        drop1.pack(padx=20,pady=5)

        clicked2 = tk.StringVar()
        clicked2.set("minutes")

        drop2 = tk.OptionMenu(self, clicked2, *list2)
        drop2.pack(padx=20,pady=5)


        def grab_date():

            all_time=""

            temp = cal.get_date()+" "+clicked1.get()+":"+clicked2.get()+":00"
            global element
            element = datetime.datetime.strptime(temp,"%d/%m/%Y %H:%M:%S")
            global timestamp
            timestamp = datetime.datetime.timestamp(element)
            all_time=clicked1.get()+" "+clicked2.get()+" "+cal.get_date()
            success_msg2 = "selected date is : "+temp
            messagebox.showinfo("Success",success_msg2)


        my_button =  tk.Button(self, text="set date", command=grab_date,font=self.describe_font,)
        my_button.pack(pady=10)


        ####################################

        def submit():
            mydb = mysql.connector.connect(
              host="********",
              user="root",
              password="*************",
              database="*************"
            )


            mycursor = mydb.cursor()
            sql = "INSERT INTO tasks (name, timestamp) VALUES (%s, %s)"
            val = (name_set,element)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            messagebox.showinfo("Success","Successfully submitted in database")


        ##################################

        button0 = tk.Button(self, text="Submit Into DataBase",command=submit,font=self.describe_font,)
        button0.pack(pady=10)


        button1 = tk.Button(self, text="Home Page",font=self.describe_font,
                           command=lambda: controller.show_frame("HomePage"))
        button1.pack(pady=20)

        button2 = tk.Button(self, text="View All Tasks",font=self.describe_font,
                           command=lambda: controller.show_frame("PageTwo"))
        button2.pack(pady=20)

        footer = tk.Label(self, text = "Made with love   ❤️by Group 1",relief="sunken", bd=1)
        footer.pack(side="bottom", fill="x")



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        def refresh_list():

            mydb = mysql.connector.connect(
              host="*********",
              user="root",
              password="*********",
              database="**************"
            )

            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM tasks order by timestamp")

            global lst
            lst = mycursor.fetchall()

            mycursor.close()

            if len(lst) != 0:
                total_rows = len(lst)
                total_columns = len(lst[0])

                ######### Modifying the dates ############


                lst = [list(ele) for ele in lst]

                global uptodate_lst
                uptodate_lst = []

                for i in range(total_rows):
                    for j in range(total_columns):
                        if j==2:
                            d_db = datetime.datetime.strptime(str(lst[i][j]), '%Y-%m-%d %H:%M:%S')
                            d_curr = datetime.datetime.now()
                            if d_db>d_curr:
                                uptodate_lst.append(lst[i])


                if len(uptodate_lst) != 0:
                    total_rows_uptodate = len(uptodate_lst)
                    total_columns_uptodate = len(uptodate_lst[0])

                    for i in range(total_rows_uptodate):
                        for j in range(total_columns_uptodate):
                            if j==2:
                                uptodate_lst[i][j] = str(uptodate_lst[i][j])
                                d = datetime.datetime.strptime(uptodate_lst[i][j], '%Y-%m-%d %H:%M:%S')
                                uptodate_lst[i][j] = datetime.date.strftime(d,  "%H:%M" + "  " + "%d %B")



                    ##########################################

                    for i in range(total_rows_uptodate):
                        for j in range(total_columns_uptodate):

                            if j==0:
                                self.e = tk.Entry(self, width=5, fg='blue', font=('Verdana',10))
                            elif j==1:
                                self.e = tk.Entry(self, width=50, fg='blue', font=('Verdana',10))
                            else:
                                self.e = tk.Entry(self, width=20, fg='blue', font=('Verdana',10))

                            self.e.grid(row=i+8, column=j)
                            self.e.insert(tk.END, uptodate_lst[i][j])

                else:
                    print("updated list empty")


            else:
                print("list empty")



            ############################################



        temp_label1 = tk.Label(self,text="",pady=15)
        temp_label1.grid(row=0)

        button0 = tk.Button(self, text="Home Page",command=lambda: controller.show_frame("HomePage"))
        button0.grid(row=1,column=1)

        button1 = tk.Button(self, text="Refresh",command=refresh_list)
        button1.grid(row=1,column=2)

        temp_label2 = tk.Label(self,text="Here is the list of all the Tasks",pady=5,font=('Verdana',16))
        temp_label2.grid(row=2,column=1)


        temp_label3 = tk.Label(self,text="",pady=15)
        temp_label3.grid(row=3)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
