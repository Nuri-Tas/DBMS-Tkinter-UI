import os
from datetime import date
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, ttk
import mysql.connector

PASSWORD = "nuri"
DATABASE_NAME = "movie_db2"

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database=DATABASE_NAME
)

def validate_login_director(username, password):
    # fetch database manager credentials
    cursor = mydb.cursor()
    sql = "SELECT users.username, users._password FROM users inner join director on users.username = director.username;"
    cursor.execute(sql)
    users = cursor.fetchall()

    # Check if the director username and password are valid
    for user in users:
        if username == user[0] and password == user[1]:
                messagebox.showinfo("Login", "Login Successful!")
                os.environ["director_username"] = username
                return directoroptions()
    messagebox.showerror("Login", "Invalid username or password")

def directoroptions():
    optionpage = Toplevel()
    optionpage.title("Director Main Menu")
    optionpage.geometry("400x400")
    listtheatrebutton = Button(optionpage,
                           text="List Available Theatres",
                               command=get_slot)
    addmoviebutton = Button(optionpage,
                                  text="Add Movie",
                            command=addmovie)
    addpredecessorbutton = Button(optionpage,
                                  text="Add Predecessor",
                                  command=add_predec)
    viewdirectedmoviesbutton = Button(optionpage,
                                text="View Directed Movies",
                                      command=directedmov)
    viewaudienceticketinfobutton = Button(optionpage,
                                text="View Audience Ticket Info",
                                          command=viewaudienceticket)
    updatemovienamebutton = Button(optionpage,
                                  text="Update Movie Name",
                                   command=updatemoviename)
    listtheatrebutton.pack(pady=10)
    addmoviebutton.pack(pady=10)
    addpredecessorbutton.pack(pady=10)
    viewdirectedmoviesbutton.pack(pady=10)
    viewaudienceticketinfobutton.pack(pady=10)
    updatemovienamebutton.pack(pady=10)

#get the slot info for listing available theatres
def get_slot():
    form_window = Toplevel()
    form_window.title("Get Slot Info")
    form_window.geometry("400x400")

    lbl_usertype = Label(form_window, text="Slot")
    lbl_usertype.pack()
    entry_slot = Entry(form_window)
    entry_slot.pack()

    lbl_date = Label(form_window, text="Date (yy/mm/dd)")
    lbl_date.pack()
    entry_date = Entry(form_window)
    entry_date.pack()

    choose_slot_button = Button(form_window, text="Choose Slot",
                                command=lambda: listavailabletheatre(entry_slot.get(), entry_date.get()))
    choose_slot_button.pack()


#use the slot to give out the info
def listavailabletheatre(slot, date1):
    try:
        intgrslot = int(slot)
        if intgrslot not in range(1,5):
            messagebox.showerror("Slot Error", "Slots need to be numbers between 1-4.")
        else:
            try:
            #buraya sql kodu gelecek
                moviedate = date1.split("/")
                year = int(moviedate[0])
                month = int(moviedate[1])
                day = int(moviedate[2])
                moviedate1 = date(year, month, day)
                cursor = mydb.cursor()
                rating = "SELECT theatre_id FROM movie_sessions WHERE time_slot = %s and _date = %s"
                values = (intgrslot, moviedate1)
                cursor.execute(rating, values)
                occupiedslot = cursor.fetchall()
                occupiedlist = []
                for i in occupiedslot:
                    occupiedlist.append(i[0])

                cursor = mydb.cursor()
                selecttheatre = "SELECT theatre_id, theatre_district, theatre_capacity from theatre"
                cursor.execute(selecttheatre)
                alltheatre = cursor.fetchall()
                alltlist = []
                for i in alltheatre:
                    alltlist.append(i[0])

                for a in occupiedlist:
                    for b in alltlist:
                        if a == b:
                            alltlist.remove(b)
                finallist = []
                for c in alltlist:
                    cursor = mydb.cursor()
                    finalize = "SELECT theatre_id, theatre_district, theatre_capacity from theatre WHERE theatre_id = %s"
                    values = (c,)
                    cursor.execute(finalize, values)
                    truet = cursor.fetchall()
                    finallist.append(truet[0])
                myview = Toplevel()
                trv = ttk.Treeview(myview, selectmode="browse")
                trv.grid(row=1, column=1, padx=20, pady=20)

                # number of columns
                trv["columns"] = ("1", "2", "3")

                # Defining heading
                trv['show'] = 'headings'

                # width of columns and alignment
                trv.column("1", width=80, anchor='c')
                trv.column("2", width=100, anchor='c')
                trv.column("3", width=80, anchor='c')
                # Headings
                # respective columns
                trv.heading("1", text="Theatre ID")
                trv.heading("2", text="Theatre District")
                trv.heading("3", text="Theatre Capacity")
                for i in finallist:
                    trv.insert("", 'end', iid=i[0], text=i[0],
                               values=(i[0], i[1], i[2],))
                myview.mainloop()
            except:
                messagebox.showerror("Date Error", "Date is not in the right format.")
    except:
        messagebox.showerror("Slot Error", "Slot needs to be an integer!")

def addmovie():
    form_window = Toplevel()
    form_window.title("Add Movie")
    form_window.geometry("400x400")

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()

    lbl_moviename = Label(form_window, text="Movie Name")
    lbl_moviename.pack()
    entry_moviename = Entry(form_window)
    entry_moviename.pack()

    lbl_moviegenre = Label(form_window, text="Genre List (write with commas between each genre)")
    lbl_moviegenre.pack()
    entry_genre = Entry(form_window)
    entry_genre.pack()

    lbl_movieduration = Label(form_window, text="Movie Duration")
    lbl_movieduration.pack()
    entry_movieduration = Entry(form_window)
    entry_movieduration.pack()

    lbl_tid = Label(form_window, text="Theatre ID")
    lbl_tid.pack()
    entry_tid = Entry(form_window)
    entry_tid.pack()

    lbl_date = Label(form_window, text="Date (YY-MM-DD)")
    lbl_date.pack()
    entry_date = Entry(form_window)
    entry_date.pack()

    lbl_time = Label(form_window, text="Time Slot")
    lbl_time.pack()
    entry_time = Entry(form_window)
    entry_time.pack()

    btn = Button(form_window, text="Add Movie", command=lambda : add_movie(entry_movieid.get(), entry_moviename.get(), entry_genre.get(), entry_movieduration.get(), entry_tid.get(), entry_date.get(), entry_time.get()))
    btn.pack()

#add movie code
def add_movie(movie_id, movie_name, genrelist, duration, theatre_id, moviedate, time_slot):
    #check if movie id already in movie list
    directr_username = os.environ.get("director_username")
    cursor = mydb.cursor()
    count = "SELECT COUNT(*) FROM movie WHERE movie_id= %s"
    values = (int(movie_id),)
    cursor.execute(count, values)
    a = cursor.fetchall()
    if a[0][0] != 0:
        messagebox.showerror("Movie Error", "Movie ID already exists")
    else:
        #check if movie name is already in the list
        cursor = mydb.cursor()
        count = "SELECT COUNT(*) FROM movie WHERE movie_name = %s"
        values = (movie_name,)
        cursor.execute(count, values)
        a = cursor.fetchall()
        if a[0][0] != 0:
            messagebox.showerror("Movie Error", "Movie name already exists")
        else:
            #check if given genres are in the list
            each_genre = genrelist.replace(" ","")
            each_genre = each_genre.split(",")
            true_genre = []
            cursor = mydb.cursor()
            look_genre = "SELECT genre_name FROM genre_list"
            cursor.execute(look_genre)
            all_genres = cursor.fetchall()
            for i in each_genre:
                genreappended = False
                for indx in range(0, len(all_genres)):
                    if i == all_genres[indx][0]:
                        true_genre.append(i)
                        genreappended = True
                if not genreappended:
                    messagebox.showerror("Genre Error", f"Your input {i} not in genre list")
            if len(true_genre) != 0:
                #check if duration is the right format -it cant be more than 4
                try:
                    intduration = int(duration)
                except:
                    messagebox.showerror("Duration error", "Duration must be an integer")
                else:
                    if intduration>5 or intduration<1:
                        messagebox.showerror("Duration error", "Duration must be between 1-4")
                    else:
                        #check if the theatre id is in the theatre list
                        cursor = mydb.cursor()
                        theatreidcheck = "SELECT COUNT(*) FROM theatre WHERE theatre_id = %s"
                        values = (int(theatre_id),)
                        cursor.execute(theatreidcheck, values)
                        a = cursor.fetchall()
                        if a[0][0] == 0:
                            messagebox.showerror("Theatre ID error", "Theatre not found")
                        else:
                            #check movie date has the right format
                            try:
                                moviedate = moviedate.split("/")
                                year = int(moviedate[0])
                                month = int(moviedate[1])
                                day = int(moviedate[2])
                                moviedate1 = date(year, month, day)
                                datetrue = True
                            except:
                                messagebox.showerror("Date Error", "Date is not in the right format")
                            else:
                                if datetrue:
                                    #check timeslot is correct format
                                    try:
                                        intgerslot = int(time_slot)
                                        if intgerslot not in range(1, 5):
                                            messagebox.showerror("Slot Error", "Slots need to be numbers between 1-4.")
                                    except:
                                        messagebox.showerror("Slot Error", "Slot needs to be an integer")
                                    else:
                                        #check if the theatre is available for that time and date
                                        cursor = mydb.cursor()
                                        checkavailable = "SELECT COUNT(*) FROM movie_sessions WHERE _date = %s AND time_slot = %s"
                                        values = (moviedate1, intgerslot)
                                        cursor.execute(checkavailable, values)
                                        countavailable = cursor.fetchall()
                                        if countavailable[0][0] != 0:
                                            messagebox.showerror("Availability error", "Theatre is booked on those dates and slot")
                                        else:
                                            # I moved auto-increment part out of the try-except block to keep increasing session ids
                                            sessid = "SELECT max(session_id) FROM screens_as"
                                            cursor.execute(sessid)
                                            a = cursor.fetchall()
                                            session_id = a[-1][0] + 1
                                            try:
                                                # insert into movie table
                                                cursor = mydb.cursor()
                                                getplatformid = "SELECT platform_id FROM director WHERE username = %s"
                                                values = (directr_username,)
                                                cursor.execute(getplatformid, values)
                                                plat = cursor.fetchall()
                                                platid = plat[0][0]
                                                cursor = mydb.cursor()
                                                insertmovie = "INSERT INTO movie VALUES (%s, %s, %s, %s, %s)"
                                                values = (
                                                int(movie_id), movie_name, intduration, directr_username, platid)
                                                cursor.execute(insertmovie, values)
                                                mydb.commit()
                                                #add movie into has genre list
                                                #first get genre ids of given genres:
                                                genre_ids_final = []
                                                for genre in true_genre:
                                                    cursor = mydb.cursor()
                                                    getgenreid = "SELECT genre_id FROM genre_list WHERE genre_name = %s "
                                                    values = (genre,)
                                                    cursor.execute(getgenreid, values)
                                                    genreids = cursor.fetchall()
                                                    genre_ids_final.append(genreids[0][0])
                                                #insert into has genre
                                                for final_genre_id in genre_ids_final:
                                                    cursor = mydb.cursor()
                                                    insertgenre = "INSERT INTO has_genre VALUES (%s, %s)"
                                                    values = (int(movie_id), final_genre_id)
                                                    cursor.execute(insertgenre, values)
                                                    mydb.commit()
                                                # insert into movie sessions
                                                cursor = mydb.cursor()
                                                # sessid = "SELECT session_id FROM screens_as"
                                                # cursor.execute(sessid)
                                                # a = cursor.fetchall()
                                                # session_id = a[-1][0] + 1
                                                # cursor = mydb.cursor()
                                                insertsession = "INSERT INTO movie_sessions VALUES (%s, %s, %s, %s)"
                                                values = (session_id, intgerslot, moviedate1, int(theatre_id))
                                                cursor.execute(insertsession, values)
                                                mydb.commit()


                                                #insert into sessions as
                                                cursor = mydb.cursor()
                                                insertscreen = "INSERT INTO screens_as VALUES (%s, %s)"
                                                values = (int(movie_id), session_id)
                                                cursor.execute(insertscreen, values)
                                                mydb.commit()
                                                messagebox.showinfo("Movie Insertion", "Movie Added Succesfully")

                                            except mysql.connector.Error as error:
                                                messagebox.showerror("Movie Insertion",
                                                                     f"Failed to insert movie: {error}")

#add predecessor ui
def add_predec():
    form_window = Toplevel()
    form_window.title("Add Predecessor")
    form_window.geometry("400x400")

    lbl_preid = Label(form_window, text="Predecessor's Movie_ID")
    lbl_preid.pack()
    entry_preid = Entry(form_window)
    entry_preid.pack()

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()

    btn_addpre = Button(form_window, text="Add", command=lambda : add_fnct_predecessor(entry_preid.get(), entry_movieid.get()))
    btn_addpre.pack()

#function to add predecessor
def add_fnct_predecessor(predec_id, movie_id):
    try:
        director_username = os.environ.get("director_username")
        cursor = mydb.cursor()
        rating = "SELECT COUNT(*) FROM movie inner join director on movie.username = director.username WHERE director.username= %s and movie_id= %s"
        values = (director_username, int(movie_id))
        cursor.execute(rating, values)
        b = cursor.fetchall()
        if b[0][0] != 0:
            cursor = mydb.cursor()
            insertpre = "INSERT INTO predecessors (predecessor_id, movie_id) VALUES (%s, %s)"
            values = (predec_id, movie_id)
            cursor.execute(insertpre, values)
            mydb.commit()
            messagebox.showinfo("Database", "Predecessor added successfully!")
        else:
            messagebox.showerror("Director Error", "Incorrect MovieID: Choose a movie you directed")
    except mysql.connector.Error as error:
        messagebox.showerror("Database", f"Failed to add predecessor: {error}")


#view audience ticket ui
def viewaudienceticket():
    direct_username = os.environ.get("director_username")
    form_window = Toplevel()
    form_window.title("Audience Tickets")
    form_window.geometry("400x400")

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()

    btn_enter = Button(form_window, text="Enter", command=lambda : view_audienceticket(entry_movieid.get(), direct_username))
    btn_enter.pack()



def directedmov():
    director_username = os.environ.get("director_username")
    return viewdirectedmov(director_username)


def viewdirectedmov(director_username):
    cursor = mydb.cursor()
    rating = "SELECT distinct a.movie_id, movie_name, time_slot, theatre_id from (select movie_id, movie_name FROM movie inner " \
             "join director on movie.username = %s ORDER BY movie_id) AS a inner join (select movie_id, " \
             "movie_sessions.session_id, time_slot, theatre_id from screens_as inner join movie_sessions where " \
             "screens_as.session_id = movie_sessions.session_id) as b where a.movie_id = b.movie_id ORDER BY a.movie_id "
    values = (director_username,)
    cursor.execute(rating, values)
    a = cursor.fetchall()
    movie_id_list = []
    for i in a:
        if i[0] not in movie_id_list:
            movie_id_list.append(i[0])
    id_ve_pre = []
    for i in movie_id_list:
        cursor = mydb.cursor()
        komut = "SELECT predecessor_id from predecessors WHERE movie_id = %s"
        value = (i,)
        cursor.execute(komut, value)
        c = cursor.fetchall()
        id_ve_pre.append([i, c])

    myview = Tk()
    trv = ttk.Treeview(myview, selectmode="browse")
    trv.grid(row=1, column=1, padx=20, pady=20)

    # number of columns
    trv["columns"] = ("1", "2", "3", "4", "5")

    # Defining heading
    trv['show'] = 'headings'

    # width of columns and alignment
    trv.column("1", width=80, anchor='c')
    trv.column("2", width=100, anchor='c')
    trv.column("3", width=80, anchor='c')
    trv.column("4", width=80, anchor='c')
    trv.column("5", width=100, anchor="c")
    # Headings
    # respective columns
    trv.heading("1", text="Movie ID")
    trv.heading("2", text="Movie Name")
    trv.heading("3", text="Time Slot")
    trv.heading("4", text="Theatre ID")
    trv.heading("5", text="Predecessors")
    # getting data from MySQL student table
    for i in a:
        ida = i[0]
        pred = ""
        for b in id_ve_pre:
            if b[0] == ida:
                pred = str(b[1]).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",,", ",")
        trv.insert("", 'end', text=i[0],
                   values=(i[0], i[1], i[2], i[3], pred))
    myview.mainloop()


def view_audienceticket(movie_id, director_username):
    cursor = mydb.cursor()
    rating = "SELECT COUNT(*) FROM movie inner join director on movie.username = director.username WHERE director.username= %s and movie_id= %s"
    values = (director_username, int(movie_id))
    cursor.execute(rating, values)
    b = cursor.fetchall()
    if b[0][0] != 0:
        cursor = mydb.cursor()
        rating = "SELECT username, _name, surname FROM (SELECT users.username, _name, surname, movie_id, director_username " \
                 "FROM (SELECT a.username,  movie.username as director_username, movie.movie_id FROM (SELECT username, " \
                 "movie_id FROM bought_tickets inner join screens_as where bought_tickets.session_id = screens_as.session_id) " \
                 "as a inner join movie where movie.movie_id = a.movie_id) AS B inner join users where users.username = " \
                 "B.username) as M WHERE M.movie_id = %s AND M.director_username = %s "
        #BURAYA KOD GELECEK
        values = (movie_id, director_username)
        cursor.execute(rating, values)
        a = cursor.fetchall()
        myview = Toplevel()
        trv = ttk.Treeview(myview, selectmode="browse")
        trv.grid(row=1, column=1, padx=20, pady=20)

        # number of columns
        trv["columns"] = ("1", "2", "3")

        # Defining heading
        trv['show'] = 'headings'

        # width of columns and alignment
        trv.column("1", width=100, anchor='c')
        trv.column("2", width=80, anchor='c')
        trv.column("3", width=80, anchor='c')
        # Headings
        # respective columns
        trv.heading("1", text="username")
        trv.heading("2", text="name")
        trv.heading("3", text="surname")
        # getting data from MySQL student table
        for i in a:
            trv.insert("", 'end', iid=i[0], text=i[0],
                       values=(i[0], i[1], i[2]))
        myview.mainloop()
    else:
        messagebox.showerror("Director Error", "Incorrect MovieID: Choose an ID of a movie you directed")


#update moviename ui
def updatemoviename():
    form_window = Toplevel()
    form_window.title("Update Movie Name")
    form_window.geometry("400x400")

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()

    lbl_newname = Label(form_window, text="Updated Name")
    lbl_newname.pack()
    entry_newname = Entry(form_window)
    entry_newname.pack()

    btn_update_movie_name= Button(form_window, text=f"Update Movie Name",
                                  command=lambda : update_moviename(entry_movieid.get(), entry_newname.get()))
    btn_update_movie_name.pack()

def update_moviename(movie_id, movie_name):
    cursor = mydb.cursor()
    # check if the given movie id belongs to the director who logged in the system
    director_username = os.environ.get("director_username")
    sql = "select movie_id from movie where username = %s"
    cursor.execute(sql, (director_username,))
    movie_ids = [str(item[0]) for item in cursor.fetchall()]
    if movie_id in movie_ids:
        sql = "UPDATE Movie SET movie_name = %s where movie_id = %s"
        cursor.execute(sql, (movie_name, movie_id))
        mydb.commit()
        messagebox.showinfo("Database", "The movie name has changed successfully!")
    else:
        messagebox.showerror("Database", f"The movie id {movie_id} belongs to another director!")


