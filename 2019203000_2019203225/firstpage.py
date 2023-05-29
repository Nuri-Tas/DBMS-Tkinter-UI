# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import mysql.connector
from dbmanageroperations import dbmanageroptions
from directoroperations import validate_login_director
from audienceoperations import validate_login_audience
import os


PASSWORD = "nuri"
DATABASE_NAME = "movie_db2"

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database=DATABASE_NAME
)


def validate_login(username, password):
    # fetch database manager credentials
    cursor = mydb.cursor()
    sql = "select * from database_managers"
    cursor.execute(sql)
    db_managers = cursor.fetchall()

    # Check if the manager username and password are valid
    for manager in db_managers:
        if username == manager[0] and password == manager[1]:
                messagebox.showinfo("Login", "Login Successful!")
                return dbmanageroptions()
    messagebox.showerror("Login", "Invalid username or password")

# creates a Tk() object
master = Tk()

# sets the geometry of main
# root window
master.geometry("400x400")
master.title("Movie DB System")


# function to open a new window
# on a button click
def dbWindow():

    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)

    # sets the title of the
    # Toplevel widget
    newWindow.title("Database Manager Login")

    # sets the geometry of toplevel
    newWindow.geometry("400x400")


    lbl_username = Label(newWindow, text="Username:")
    lbl_username.pack()
    entry_username = Entry(newWindow)
    entry_username.pack()

    lbl_password = Label(newWindow, text="Password:")
    lbl_password.pack()
    entry_password = Entry(newWindow)
    entry_password.pack()

    loginbutton = Button(newWindow,
                         text= "Login",
                         command=lambda: validate_login(entry_username.get(), entry_password.get()))
    loginbutton.pack()





def directorwindow():
    newWindow = Toplevel(master)
    newWindow.title("Director UI")
    newWindow.geometry("400x400")

    lbl_username = Label(newWindow, text="Username:")
    lbl_username.pack()
    entry_username = Entry(newWindow)
    entry_username.pack()

    lbl_password = Label(newWindow, text="Password:")
    lbl_password.pack()
    entry_password = Entry(newWindow)
    entry_password.pack()

    loginbutton = Button(newWindow,
                         text="Login",
                         command=lambda: validate_login_director(entry_username.get(), entry_password.get()))
    loginbutton.pack()


def audiencewindow():
    newWindow = Toplevel(master)
    newWindow.title("Audience UI")
    newWindow.geometry("400x400")

    lbl_username = Label(newWindow, text="Username:")
    lbl_username.pack()
    entry_username = Entry(newWindow)
    entry_username.pack()

    lbl_password = Label(newWindow, text="Password:")
    lbl_password.pack()
    entry_password = Entry(newWindow)
    entry_password.pack()

    loginbutton = Button(newWindow,
                         text="Login",
                         command=lambda: validate_login_audience(entry_username.get(), entry_password.get()))
    loginbutton.pack()




label = Label(master,
              text ="To login, choose user type:")

label.pack(pady = 10)

# a button widget which will open a
# new window on button click
btndbmanager = Button(master,
             text ="Database Manager",
             command = dbWindow)
btndbmanager.pack(pady = 10)

btndirector = Button(master,
             text="Director",
             command= directorwindow)
btndirector.pack(pady= 10)


btnaudience = Button(master,
                     text= "Audience",
                     command=audiencewindow)
btnaudience.pack(pady=10)


# mainloop, runs infinitely
mainloop()
