When we are working with any group or team, it happens with almost all of us, that we have a group meeting at some time and we forget to join, or maybe some important task and we just forget to do that.
Well our Python project is a one stop solution to all these problems. It is made for all the wonderful teams and their hardworking members, to notify them the group related important tasks or meetings.
Now coming to the functionality of the project. As suggested by the name that it is basically a task notifier assistant.
But wait, we have brought some exciting features to it.
It has got a database where you can store all your team's important tasks and the time on which it has to notify all the group members. You will use a nice frontend made with Tkinter to save the tasks as well as view them from the database.

Then we have got a file which will serve as the backend for our project. It will run continuously and will notify team members if something important has to be done. 
If there is a task scheduled in the database and the time of the task has come then it will give an alarm on your pc or laptop. 
But wait here is something exciting, it will not play that same boring alarm tone again and again, rather it would repeat the name of the task again and again to make sure you get to know about that task.

But what will happen if your laptop is closed? In that case you might not be hearing the sound then, now what ??
Don't worry we've got this covered too. It will also send a message to your whatsapp or telegram account, so that you never miss anything important.

Now coming to what technologies we have used to implement our project.
We are using Tkinter for the frontend of our project.
We are using Cloud Instance for Mysql Database (on Google Cloud Platform), so that every team member has access to the database. 
We are using PYTTSX3 engine to convert text to voice, so that you will hear your task name as the alarm.
We are using APIs of Telegram and WhatsApp and automating the sending of task names as  messages as soon as any event or task is triggered.
Our python backend file is running on a Heroku server, so it will run always. No worries if the laptops of team members are off. You will still receive notifications on your phones.
______________ Group 1 - CSE _____________________


Shubham Khandelwal ( 2019KUCP1008 )
Piyush Gupta ( 2019KUCP1024 )
Yash Agrawal (2019KUCP1027 )
Aman Jain ( 2019KUCP1122 )


_________________________ Modules to import to use this project ____________________


1.  tkinter
2.  mysql.connector
3.  string
4.  tkcalender
5.  datetime
6.  winsound
7.  pyttsx3
8.  requests
9.  os
