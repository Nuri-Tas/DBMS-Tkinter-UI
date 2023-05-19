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

def validate_login_director(username, password):
    # fetch database manager credentials
    cursor = mydb.cursor()
    sql = "select * from users"
    cursor.execute(sql)
    users = cursor.fetchall()
    
    # fetch director usernames to check if the given user is a director
    direct_sql = "select username from director"
    cursor.execute(direct_sql)
    director_usernames = [item[0] for item in cursor.fetchall()]

    # Check if the manager username and password are valid
    for user in users:
        if username == user[0] and password == user[1] and username in director_usernames:
                messagebox.showinfo("Login", "Login Successful!")
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
                                text="View Directed Movies")
    viewaudienceticketinfobutton = Button(optionpage,
                                text="View Audience Ticket Info",
                                          command=viewaudienceticket)
    updatemovienamebutton = Button(optionpage,
                                  text="Update Movie Name",
                                   command=open_updatemoviename)
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

    choose_slot_button = Button(form_window, text="Choose Slot", command=lambda : listavailabletheatre(entry_slot.get()))
    choose_slot_button.pack()

#use the slot to give out the info
def listavailabletheatre(slot):
    try:
        intgrslot = int(slot)
        if intgrslot not in range(1,6):
            messagebox.showerror("Slot Error", "Slots need to be numbers between 1-5.")
        else:
            #buraya sql kodu gelecek
            messagebox.showinfo("Slot Success", "Chosen Succesfully")
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

    lbl_tid = Label(form_window, text="Theatre ID")
    lbl_tid.pack()
    entry_tid = Entry(form_window)
    entry_tid.pack()

    lbl_time = Label(form_window, text="Time Slot")
    lbl_time.pack()
    entry_time = Entry(form_window)
    entry_time.pack()

#add predecessor ui
def add_predec():
    form_window = Toplevel()
    form_window.title("Add Predecessor")
    form_window.geometry("400x400")

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()

    lbl_preid = Label(form_window, text="Predecessor's Movie_ID")
    lbl_preid.pack()
    entry_preid = Entry(form_window)
    entry_preid.pack()

#view audience ticket ui
def viewaudienceticket():
    form_window = Toplevel()
    form_window.title("Audience Tickets")
    form_window.geometry("400x400")

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()


#view audience ticket ui
def viewaudienceticket():
    form_window = Toplevel()
    form_window.title("Audience Tickets")
    form_window.geometry("400x400")

    lbl_movieid = Label(form_window, text="Movie_ID")
    lbl_movieid.pack()
    entry_movieid = Entry(form_window)
    entry_movieid.pack()



#update moviename ui
def open_updatemoviename():
    cursor = mydb.cursor()
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
    director_username = os.environ.get("DIRECTOR_USERNAME")
    sql = "select movie_id from Movie where username = %s"
    cursor.execute(sql, (director_username,))
    movie_ids = [str(item[0]) for item in cursor.fetchall()]
    if movie_id in movie_ids:
        sql = "UPDATE Movie SET movie_name = %s where movie_id = %s"
        cursor.execute(sql, (movie_name, movie_id))
        mydb.commit()
        messagebox.showinfo("Database", "The movie name has changed successfully!")
    else:
        messagebox.showerror("Database", f"The movie id {movie_id} belongs to another director!")











