from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, ttk
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Devrim1-",
    database="new_schema"
)

def validate_login_audience(username, password):
    # fetch database manager credentials
    cursor = mydb.cursor()
    sql = "select * from users"
    cursor.execute(sql)
    users = cursor.fetchall()

    # Check if the manager username and password are valid
    for user in users:
        if username == user[0] and password == user[1]:
                messagebox.showinfo("Login", "Login Successful!")
                return audienceoptions()
    messagebox.showerror("Login", "Invalid username or password")

def audienceoptions():
    optionpage = Toplevel()
    optionpage.title("Audience Main Menu")
    optionpage.geometry("400x400")
    listmoviebutton = Button(optionpage,
                           text="List All Movies")
    buymoviebutton = Button(optionpage,
                                  text="Buy Movie Ticket",
                            command=buymovieticket)
    viewticketbutton = Button(optionpage,
                                  text="View Bought Tickets")
    listmoviebutton.pack(pady=10)
    buymoviebutton.pack(pady=10)
    viewticketbutton.pack(pady=10)

#buy movie ticket ui
def buymovieticket():
    form_window = Toplevel()
    form_window.title("Buy Ticket")
    form_window.geometry("400x400")

    lbl_sessid = Label(form_window, text="Session ID")
    lbl_sessid.pack()
    entry_sessid = Entry(form_window)
    entry_sessid.pack()
