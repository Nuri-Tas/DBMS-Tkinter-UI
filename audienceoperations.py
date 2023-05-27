from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, ttk
import mysql.connector
import os 

PASSWORD = "nuri"
DATABASE_NAME = "movie_db2"

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database=DATABASE_NAME
)

def validate_login_audience(username, password):
    # fetch database manager credentials
    cursor = mydb.cursor()
    sql = "select * from users"
    cursor.execute(sql)
    users = cursor.fetchall()
    
    # fetch audience usernames to check if the given user is an audience
    direct_sql = "select username from audience"
    cursor.execute(direct_sql)
    audience_usernames = [item[0] for item in cursor.fetchall()]

    # Check if the audience username and password are valid
    for user in users:
        if username == user[0] and password == user[1] and username in audience_usernames:
                messagebox.showinfo("Login", "Login Successful!")
                os.environ["AUDIENCE_USERNAME"] = username
                return audienceoptions()
    messagebox.showerror("Login", "Invalid username or password")

def audienceoptions():
    optionpage = Toplevel()
    optionpage.title("Audience Main Menu")
    optionpage.geometry("400x400")
    listmoviebutton = Button(optionpage,
                           text="List All Movies",
                            command=view_all_movies)
    buymoviebutton = Button(optionpage,
                                  text="Buy Movie Ticket",
                            command=open_buymovieticket)
    viewticketbutton = Button(optionpage,
                                  text="View Bought Tickets",
                             command=view_bought_tickets)
    listmoviebutton.pack(pady=10)
    buymoviebutton.pack(pady=10)
    viewticketbutton.pack(pady=10)

#buy movie ticket ui
def open_buymovieticket():
    form_window = Toplevel()
    form_window.title("Buy Ticket")
    form_window.geometry("400x400")

    lbl_sessid = Label(form_window, text="Session ID")
    lbl_sessid.pack()
    entry_sessid = Entry(form_window)
    entry_sessid.pack()

    btn_buymovieticket = Button(form_window, text="Buy Movie Ticket", command=lambda : buymovieticket(entry_sessid.get()))
    btn_buymovieticket.pack()


def buymovieticket(session_id):
    cursor = mydb.cursor()
    audience_username = os.environ["AUDIENCE_USERNAME"]
    try:
        sql = "insert into bought_tickets(username, session_id) values (%s, %s)"
        values = (audience_username, session_id)
        cursor.execute(sql, values)
        mydb.commit()
        messagebox.showinfo("Buy Ticket", f"The ticket for the session id {session_id} has been bought successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Buy Ticket", err)


def view_all_movies():
    cursor = mydb.cursor()
    # get all movie id's of the given author
    sql = "select movie_id, movie_name, username from Movie"
    cursor.execute(sql)
    id_name_username = cursor.fetchall()
    results = []
    for idx, item in enumerate(id_name_username):
        movie_id = item[0]
        new_row = [item[0], item[1]]
        director_username = item[-1]

        # get director's surname
        sql = "select surname from Users where username = %s"
        cursor.execute(sql, (director_username, ))
        director_surname = cursor.fetchall()[0]
        new_row.append(director_surname)

        # get directors' platform
        sql = "select distinct(platform_id) from Movie where username = %s"
        cursor.execute(sql, (director_username, ))
        director_platform = cursor.fetchall()[0]
        new_row.append(director_platform)

        movie_id = item[0]
        # get session id to fetch the theatre id and other attributes
        sql = "select session_id from screens_as where movie_id = %s"
        cursor.execute(sql, (movie_id,))
        session_id = cursor.fetchall()[0]

        # add theatre id and time slot
        sql = "select theatre_id, time_slot from Movie_Sessions where session_id = %s"
        cursor.execute(sql, (session_id[0],))
        theatre_id, time_slot = cursor.fetchall()[0]
        new_row.extend([theatre_id, time_slot])


        # create predecessors list as comma separated values
        sql = "select predecessor_id from predecessors where movie_id = %s"
        cursor.execute(sql, (movie_id, ))
        predecessor_results = cursor.fetchall()
        predecessor_list = []
        while len(predecessor_results) > 0:
            predecessor_id = predecessor_results[0][0]
            predecessor_list.append(str(predecessor_id))
            movie_id = predecessor_id

            sql = "select predecessor_id from predecessors where movie_id = %s"
            cursor.execute(sql, (movie_id,))
            predecessor_results = cursor.fetchall()

        predecessor_str = ",".join(predecessor_list)
        new_row.append(predecessor_str)
        results.append(new_row)

    myview = Toplevel()
    trv = ttk.Treeview(myview, selectmode="browse")
    trv.grid(row=1, column=1, padx=50, pady=50)

    # number of columns
    trv["columns"] = ("1", "2", "3", "4", "5", "6", "7")

    # Defining heading
    trv['show'] = 'headings'

    # width of columns and alignment
    trv.column("1", width=80, anchor='c')
    trv.column("2", width=100, anchor='c')
    trv.column("3", width=80, anchor='c')
    trv.column("4", width=100, anchor='c')
    trv.column("5", width=80, anchor='c')
    trv.column("6", width=100, anchor='c')
    trv.column("7", width=80, anchor='c')
    # Headings
    # respective columns
    trv.heading("1", text="movie_id")
    trv.heading("2", text="movie_name")
    trv.heading("3", text="director's surname")
    trv.heading("4", text="platform id")
    trv.heading("5", text="theatre_id")
    trv.heading("6", text="time_slot")
    trv.heading("7", text="predecessors list")
    for i in results:
        trv.insert("", 'end', iid=i[0], text=i[0],
                   values=i)
    myview.mainloop()


def view_bought_tickets():
    mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database=DATABASE_NAME)
    
    audience_username = os.environ.get("AUDIENCE_USERNAME")
    cursor = mydb.cursor()
    # get all session id's bought by the user
    sql = "select session_id from bought_tickets where username = %s"
    cursor.execute(sql, (audience_username, ))
    session_ids = [item[0] for item in cursor.fetchall()]
    results = []
    for idx, item in enumerate(session_ids):
        session_id = item

        # get movie id's
        sql = "select movie_id from screens_as where session_id = %s"
        cursor.execute(sql, (session_id, ))
        movie_id = cursor.fetchall()[0][0]
        new_row = [movie_id]

        # get movie name
        sql = "select movie_name from Movie where movie_id = %s"
        cursor.execute(sql, (movie_id, ))
        movie_name = cursor.fetchall()[0][0]
        new_row.extend([movie_name, session_id])

        # get rating, if available, otherwise return NULL
        sql = "select rating from Ratings where username = %s and movie_id = %s"
        cursor.execute(sql, (audience_username, movie_id))
        try:
            rating = cursor.fetchall()[0][0]
        except:
            rating = "NULL"
        new_row.append(rating)

        # get overall rating of the film - overall rating can be null as well
        sql = "select average_rating from average_ratings where movie_id = %s"
        cursor.execute(sql, (movie_id, ))
        try:
            avg_rating = cursor.fetchall()[0][0]
        except:
            avg_rating = "NULL"
        new_row.append(avg_rating)

        results.append(new_row)


    myview = Toplevel()
    trv = ttk.Treeview(myview, selectmode="browse")
    trv.grid(row=1, column=1, padx=50, pady=50)

    # number of columns
    trv["columns"] = ("1", "2", "3", "4", "5")

    # Defining heading
    trv['show'] = 'headings'

    # width of columns and alignment
    trv.column("1", width=80, anchor='c')
    trv.column("2", width=100, anchor='c')
    trv.column("3", width=80, anchor='c')
    trv.column("4", width=100, anchor='c')
    trv.column("5", width=80, anchor='c')
    # Headings
    # respective columns
    trv.heading("1", text="movie_id")
    trv.heading("2", text="movie_name")
    trv.heading("3", text="session id")
    trv.heading("4", text="rating")
    trv.heading("5", text="average rating")

    for i in results:
        trv.insert("", 'end', iid=i[2], text=i[2],
                   values=i)
    myview.mainloop()    
