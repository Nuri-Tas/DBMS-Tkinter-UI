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

def dbmanageroptions():
    optionpage = Toplevel()
    optionpage.title("Database Manager Main Menu")
    optionpage.geometry("400x400")
    adduserbutton = Button(optionpage,
                           text="Add User",
                           command= open_add_user_form)
    deleteaudiencebutton = Button(optionpage,
                                  text="Delete Audience",
                                  command= open_delete_audience)
    updateplatformbutton = Button(optionpage,
                                  text="Update Platform of Director",
                                  command= open_updateidfordirector)
    viewdirectorbutton = Button(optionpage,
                                text="View all Directors",
                                command= view_all_directors)
    viewaudiencerating = Button(optionpage,
                                text="View Audience Ratings",
                                command=open_rating_audience)
    viewmoviesofdirector = Button(optionpage,
                                  text="View Movies of Director")
    viewavgrating = Button(optionpage,
                           text="View Average Rating of a Movie")
    adduserbutton.pack(pady= 10)
    deleteaudiencebutton.pack(pady=10)
    updateplatformbutton.pack(pady=10)
    viewdirectorbutton.pack(pady=10)
    viewaudiencerating.pack(pady=10)
    viewmoviesofdirector.pack(pady=10)
    viewavgrating.pack(pady=10)

# Function to open the form to add a new user
def open_add_user_form():
    form_window = Toplevel()
    form_window.title("Add User")
    form_window.geometry("1600x800")

    # Button for adding new users to the system
    lbl_usertype = Label(form_window, text="User Type:")
    lbl_usertype.pack()
    entry_usertype = Entry(form_window)
    entry_usertype.pack()

    lbl_username = Label(form_window, text="Username:")
    lbl_username.pack()
    entry_username = Entry(form_window)
    entry_username.pack()

    lbl_password = Label(form_window, text="Password:")
    lbl_password.pack()
    entry_password = Entry(form_window)
    entry_password.pack()

    lbl_name = Label(form_window, text="Name:")
    lbl_name.pack()
    entry_name = Entry(form_window)
    entry_name.pack()

    lbl_surname = Label(form_window, text="Surname:")
    lbl_surname.pack()
    entry_surname = Entry(form_window)
    entry_surname.pack()

    lbl_nation = Label(form_window, text="Nationality (Only for Directors):")
    lbl_nation.pack()
    entry_nation = Entry(form_window)
    entry_nation.pack()

    lbl_platformid = Label(form_window, text="Platform ID (Only for Directors):")
    lbl_platformid.pack()
    entry_platformid = Entry(form_window)
    entry_platformid.pack()

    btn_add_user = Button(form_window, text="Add User",
                                 command=lambda: add_user(entry_usertype.get(), entry_username.get(),
                                                          entry_password.get(), entry_name.get(),
                                                          entry_surname.get(), entry_nation.get(), entry_platformid.get()
                                                          ))
    btn_add_user.pack()

# Function to add a new user to the database
def add_user(user_type, username, password, name, surname, nationality, platformid):
    try:
        if user_type.lower() == "audience":
            cursor = mydb.cursor()
            insert_query = "INSERT INTO Users (username, _password, _name, surname) VALUES (%s, %s, %s, %s)"
            values = (username, password, name, surname)
            cursor.execute(insert_query, values)
            mydb.commit()
            insert_query = "INSERT INTO Audience (username) VALUES (%s)"
            values = (username,)
            cursor.execute(insert_query, values)
            mydb.commit()
            messagebox.showinfo("Database", "New user added successfully!")
        elif user_type.lower() == "director":
            #need to check to see nationality is not null and the platform id matches!
            nationalitycheck = True
            if len(nationality) == 0:
                nationalitycheck = False
                messagebox.showinfo("Database", "Nationality of a director cannot be null!")
            #check platform id:
            idcheck = False
            idnull = False
            if len(platformid) == 0:
                idcheck = True
                idnull = True
            else:
                integerid = int(platformid)
                cursor = mydb.cursor()
                platformidcheck = "select platform_id from rating_platform"
                cursor.execute(platformidcheck)
                platformids = cursor.fetchall()
                for id in platformids:
                    if integerid == id[0]:
                        idcheck = True
            if not idcheck:
                messagebox.showinfo("Database", "Platform ID not in list!")
            if nationalitycheck and idcheck:
                cursor = mydb.cursor()
                insert_query = "INSERT INTO Users (username, _password, _name, surname) VALUES (%s, %s, %s, %s)"
                values = (username, password, name, surname)
                cursor.execute(insert_query, values)
                mydb.commit()
                insert_query = "INSERT INTO Director (username, nationality, platform_id) VALUES (%s, %s, %s)"
                if idnull:
                    values = (username, nationality, None)
                else:
                    values = (username, nationality, integerid)
                cursor.execute(insert_query, values)
                mydb.commit()
                messagebox.showinfo("Database", "New user added successfully!")
        else:
            print("Only Audience and Directors user type is allowed")
            return False
    except mysql.connector.Error as error:
        messagebox.showerror("Database", f"Failed to connect to the database: {error}")

#open delete audience page
def open_delete_audience():
    form_window = Toplevel()
    form_window.title( "Delete User")
    form_window.geometry("400x400")

    lbl_username = Label(form_window, text="Username:")
    lbl_username.pack()
    entry_username = Entry(form_window)
    entry_username.pack()

    btn_delete_audience = Button(form_window, text="Delete User", command=lambda : delete_audience(entry_username.get()))
    btn_delete_audience.pack()



#Function to delete audience
def delete_audience(audience_username):
    cursor = mydb.cursor()
    sql = "select username from audience"
    cursor.execute(sql)
    results = [item[0] for item in cursor.fetchall()]
    if audience_username not in results:
        print(f"{audience_username} is not in the Audience.")
        messagebox.showerror("Database", f"{audience_username} is not in the Audience")
    else:
        try:
            sql = "DELETE FROM Users WHERE username = %s"
            values = (audience_username,)
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Database", f"The audience {audience_username} is deleted!")
        except mysql.connector.Error as error:
            messagebox.showerror("Database", f"Failed to connect to the database: {error}")

#open update platform id for director page:
def open_updateidfordirector():
    form_window = Toplevel()
    form_window.title("Update Platform ID of a Director")
    form_window.geometry("400x400")

    # Button for updating the director's platform id (Q4)
    lbl_director_username = Label(form_window, text="Director Username:")
    lbl_director_username.pack()
    entry_lbl_director_username = Entry(form_window)
    entry_lbl_director_username.pack()

    lbl_new_id = Label(form_window, text="New Platform Id:")
    lbl_new_id.pack()
    entry_lbl_new_id = Entry(form_window)
    entry_lbl_new_id.pack()

    btn_update_platform_id = Button(form_window, text="Update Platform ID",
                                    command=lambda: update_director_platform(entry_lbl_director_username.get(),
                                                                             entry_lbl_new_id.get()))
    btn_update_platform_id.pack()

#function to update the platformid of the director
def update_director_platform(director_username, platform_id):
    cursor = mydb.cursor()
    sql = "select username from Director"
    cursor.execute(sql)
    results = [item[0] for item in cursor.fetchall()]
    if director_username not in results:
        print(f"{director_username} is not in the Director table.")
        messagebox.showerror("Database", f"{director_username} is not in the Director table")
    else:
        try:
            # Update director's platform ID in the database
            sql = "UPDATE Director SET platform_id = %s WHERE username = %s"
            values = (platform_id, director_username)
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Database", f"The Platform Id of {director_username} is updated to {platform_id}!")
        except:
            messagebox.showerror("Database", f"The id {platform_id} must be in the Rating Platform IDs.")

#function to view all directors
def view_all_directors():
    cursor = mydb.cursor()
    platformidcheck = "SELECT director.username, _name, surname, nationality, platform_id from users INNER JOIN director on users.username = director.username"
    cursor.execute(platformidcheck)
    platformids = cursor.fetchall()

    myview = Tk()
    trv = ttk.Treeview(myview, selectmode="browse")
    trv.grid(row=1, column=1, padx=20, pady=20)

    # number of columns
    trv["columns"] = ("1", "2", "3", "4", "5")

    # Defining heading
    trv['show'] = 'headings'

    # width of columns and alignment
    trv.column("1", width=30, anchor='c')
    trv.column("2", width=80, anchor='c')
    trv.column("3", width=80, anchor='c')
    trv.column("4", width=80, anchor='c')
    trv.column("5", width=80, anchor='c')
    # Headings
    # respective columns
    trv.heading("1", text="username")
    trv.heading("2", text="_name")
    trv.heading("3", text="surname")
    trv.heading("4", text="nation")
    trv.heading("5", text="platform_id")
    # getting data from MySQL student table
    for i in platformids:
        trv.insert("", 'end', iid=i[0], text=i[0],
                   values=(i[0], i[1], i[2], i[3], i[4]))
    myview.mainloop()

#function to open page for viewing ratings of an audience:
def open_rating_audience():
    form_window = Toplevel()
    form_window.title("View Ratings of an Audience Member")
    form_window.geometry("400x400")

    lbl_rating_username = Label(form_window, text="Username:")
    lbl_rating_username.pack()
    entry_lbl_rating_username = Entry(form_window)
    entry_lbl_rating_username.pack()

    btn_enter_rating_username = Button(form_window, text="View Ratings", command=lambda: get_rating_audience(entry_lbl_rating_username.get()))
    btn_enter_rating_username.pack()

def get_rating_audience(username):
    try:
        cursor = mydb.cursor()
        rating = "select movie.movie_id, movie_name, rating from movie inner join ratings on movie.movie_id = ratings.movie_id where ratings.username = %s"
        values = (username,)
        cursor.execute(rating, values)
        allratings = cursor.fetchall()

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
        trv.heading("1", text="movie_id")
        trv.heading("2", text="movie_name")
        trv.heading("3", text="rating")
        for i in allratings:
            trv.insert("", 'end', iid=i[0], text=i[0],
                       values=(i[0], i[1], i[2], ))
        myview.mainloop()
    except:
        messagebox.showerror("Database", f"User not found!")



