import tkinter as tk
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="nuri",
    database="movie_db"
)

# Function to validate login and add new user
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
                # Open the form to add a new user
                return open_add_user_form()

    messagebox.showerror("Login", "Invalid username or password")

# Function to open the form to add a new user
def open_add_user_form():
    form_window = tk.Toplevel(root)
    form_window.title("Add User")
    form_window.geometry("1600x800")

    # Button for adding new users to the system
    lbl_usertype = tk.Label(form_window, text="User Type:")
    lbl_usertype.pack()
    entry_usertype = tk.Entry(form_window)
    entry_usertype.pack()

    lbl_username = tk.Label(form_window, text="Username:")
    lbl_username.pack()
    entry_username = tk.Entry(form_window)
    entry_username.pack()

    lbl_password = tk.Label(form_window, text="Password:")
    lbl_password.pack()
    entry_password = tk.Entry(form_window)
    entry_password.pack()

    lbl_name = tk.Label(form_window, text="Name:")
    lbl_name.pack()
    entry_name = tk.Entry(form_window)
    entry_name.pack()

    lbl_surname = tk.Label(form_window, text="Surname:")
    lbl_surname.pack()
    entry_surname = tk.Entry(form_window)
    entry_surname.pack()

    btn_add_user = tk.Button(form_window, text="Add User",
                             command=lambda: add_user(entry_usertype.get(), entry_username.get(),
                                                      entry_password.get(), entry_name.get(),
                                                      entry_surname.get()
                                                      ))
    btn_add_user.pack()


    # Button for deleting audience (Q3)
    lbl_audience_to_be_deleted = tk.Label(form_window, text="Audience Username to be Deleted:")
    lbl_audience_to_be_deleted.pack()
    entry_lbl_audience_to_be_deleted = tk.Entry(form_window)
    entry_lbl_audience_to_be_deleted.pack()

    btn_delete_audience = tk.Button(form_window, text="Delete Audience",
                                    command=lambda: delete_audience(entry_lbl_audience_to_be_deleted.get()))
    btn_delete_audience.pack()
    # ---------------

    # Button for updating the director's platform id (Q4)
    lbl_director_username = tk.Label(form_window, text="Director Username:")
    lbl_director_username.pack()
    entry_lbl_director_username = tk.Entry(form_window)
    entry_lbl_director_username.pack()

    lbl_new_id = tk.Label(form_window, text="New Platform Id:")
    lbl_new_id.pack()
    entry_lbl_new_id = tk.Entry(form_window)
    entry_lbl_new_id.pack()

    btn_update_platform_id = tk.Button(form_window, text="Update Platform ID",
                                    command=lambda: update_director_platform(entry_lbl_director_username.get(),
                                                                             entry_lbl_new_id.get()))
    btn_update_platform_id.pack()
    # ---------------

    # Button for viewing all directors (Q5)
    btn_view_all_directors = tk.Button(form_window, text="View All Directors",
                                    command=lambda: view_all_directors())
    btn_view_all_directors.pack()
    # ---------------

    # Button for viewing the ratings of an audience (Q6)
    lbl_audience_username = tk.Label(form_window, text="Audience Username")
    lbl_audience_username.pack()
    entry_lbl_audience_username = tk.Entry(form_window)
    entry_lbl_audience_username.pack()

    btn_audience_ratings = tk.Button(form_window, text="Audience Ratings",
                                    command=lambda: get_ratings(entry_lbl_audience_username.get()))
    btn_audience_ratings.pack()
    # ---------------

    # Button for viewing all movies of a given director (Q7)
    lbl_director_username = tk.Label(form_window, text="Director Username")
    lbl_director_username.pack()
    entry_lbl_director_username = tk.Entry(form_window)
    entry_lbl_director_username.pack()

    btn_all_movies = tk.Button(form_window, text="View All Movies",
                                    command=lambda: get_all_movies(entry_lbl_director_username.get()))
    btn_all_movies.pack()
    # ---------------

    # Button for viewing the average rating of a movie (Q8)
    lbl_movie_id = tk.Label(form_window, text="Movie ID")
    lbl_movie_id.pack()
    entry_lbl_movie_id = tk.Entry(form_window)
    entry_lbl_movie_id.pack()

    btn_overall_rating = tk.Button(form_window, text="View Overall Rating",
                                    command=lambda: average_rating(entry_lbl_movie_id.get()))
    btn_overall_rating.pack()
    # ---------------


# Function to add a new user to the database
def add_user(user_type, username, password, name, surname):
    try:
        cursor = mydb.cursor()
        insert_query = "INSERT INTO User (username, password, name, surname) VALUES (%s, %s, %s, %s)"
        values = (username, password, name, surname)
        cursor.execute(insert_query, values)
        mydb.commit()
        if user_type.lower() == "audience":
            insert_query = "INSERT INTO Audience (username) VALUES (%s)"
        elif user_type.lower() == "director":
            insert_query = "INSERT INTO Directors (username) VALUES (%s)"
        else:
            print("Only Audience and Directors user type is allowed")
            return False
        values = (username,)
        cursor.execute(insert_query, values)
        mydb.commit()

        messagebox.showinfo("Database", "New user added successfully!")
    except mysql.connector.Error as error:
        messagebox.showerror("Database", f"Failed to connect to the database: {error}")


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
            sql = "DELETE FROM User WHERE username = %s"
            values = (audience_username,)
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Database", f"The audience {audience_username} is deleted!")
        except mysql.connector.Error as error:
            messagebox.showerror("Database", f"Failed to connect to the database: {error}")


def update_director_platform(director_username, platform_id):
    cursor = mydb.cursor()
    sql = "select username from Directors"
    cursor.execute(sql)
    results = [item[0] for item in cursor.fetchall()]
    if director_username not in results:
        print(f"{director_username} is not in the Directors.")
        messagebox.showerror("Database", f"{director_username} is not in the Audience")
    else:
        try:
            # Update director's platform ID in the database
            sql = "UPDATE Agreement SET platform_id = %s WHERE username = %s"
            values = (platform_id, director_username)
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Database", f"The Platform Id of {director_username} is updated to {platform_id}!")
        except:
            messagebox.showerror("Database", f"The id {platform_id} must be in the Rating Platform IDs.")


def view_all_directors():
    cursor = mydb.cursor()

    sql = "SELECT username, name, surname from user where username in (select username from directors)"
    cursor.execute(sql)
    director_users = cursor.fetchall()
    print(director_users)
    for idx, user in enumerate(director_users):
        nation_sql = "select nation from Nationality where username = %s"
        platform_id_sql = "select platform_id from Agreement where username = %s"
        values = (user[0], )

        # add corresponding nations of directors
        cursor.execute(nation_sql, values)
        nation_result = cursor.fetchall()[0]
        director_users[idx] += nation_result

        # as a director may not have an agreement with a platform, we'll add None if the try block fails
        try:
            cursor.execute(platform_id_sql, values)
            nation_result = cursor.fetchall()[0]
            director_users[idx] += nation_result
        except:
            director_users[idx] += None

    # Create a new Toplevel window
    results_window = tk.Toplevel(root)
    results_window.title("All Directors")

    # Create a listbox to display the results
    listbox = tk.Listbox(results_window, width=100)
    listbox.pack()

    # Add results to the listbox
    director_users.insert(0, ("username", "name", "surname", "nation", "platform id"))
    director_users = [", ".join(item) for item in director_users]
    for result in director_users:
        listbox.insert(tk.END, result)

def get_results(cursor, sql, values=None):
    if values is not None:
        cursor.execute(sql, values)
    else:
        cursor.execute(sql)
    results = cursor.fetchall()
    return results


def get_ratings(username):
    cursor = mydb.cursor()
    # an audience may have not given any rating yet
    try:
        sql = "select movie_id, ratings from Rate where username = %s"
        # this will return only movie id and corresponding rating of the given user
        movie_id_rating = get_results(cursor, sql, (username, ))
    except:
        print("No rating is available for the given username.")
        return False
    # we also need to find movie names
    for idx, result in enumerate(movie_id_rating):
        movie_id = (result[0], )
        sql = "select movie_name from Movies where movie_id = %s"
        movie_name = get_results(cursor, sql, movie_id)[0]
        movie_id_rating[idx] += movie_name
        # convert tuple to list to change the order of elements
        movie_id_rating[idx] = list(movie_id_rating[idx])
        movie_id_rating[idx][1], movie_id_rating[idx][2] = movie_id_rating[idx][2], movie_id_rating[idx][1]

    # Create a new Toplevel window
    results_window = tk.Toplevel(root)
    results_window.title("Audience Ratings")

    # Create a listbox to display the results
    listbox = tk.Listbox(results_window, width=100)
    listbox.pack()

    # Add results to the listbox
    movie_id_rating.insert(0, ("movie id", "movie name", "rating"))
    #movie_id_rating = [", ".join(str(item)) for item in movie_id_rating]
    for result in movie_id_rating:
        listbox.insert(tk.END, result)


def get_all_movies(author_username):
    cursor = mydb.cursor()
    # get all movie id's of the given author
    sql = "select movie_id from Directed_By where username = %s"
    movie_ids = get_results(cursor, sql, (author_username, ))
    for idx, movie_id in enumerate(movie_ids):
        # add movie name
        sql = "select movie_name from Movies where movie_id = %s"
        movie_name = get_results(cursor, sql, (movie_id[0], ))[0]
        movie_ids[idx] += movie_name

        # add theatre id and time slot
        sql = "select theatre_id, time_slot from Filmed where movie_id = %s"
        theatre_id_time_slot = get_results(cursor, sql, (movie_id[0], ))[0]
        movie_ids[idx] += theatre_id_time_slot

        # add theatre district
        sql = "select theatre_district from Theatre_Location where theatre_id = %s"
        theatre_id = theatre_id_time_slot[0]
        theatre_district = get_results(cursor, sql, (theatre_id, ))[0]
        movie_ids[idx] += theatre_district

        # convert tuple to list to change the order
        movie_ids[idx] = list(movie_ids[idx])
        movie_ids[idx][3], movie_ids[idx][4] = movie_ids[idx][4], movie_ids[idx][3]

    # Create a new Toplevel window
    results_window = tk.Toplevel(root)
    results_window.title(f"{author_username}'s All Movies")

    # Create a listbox to display the results
    listbox = tk.Listbox(results_window, width=100)
    listbox.pack()

    # Add results to the listbox
    movie_ids.insert(0, ("movie id", "movie name", "theatre id", "theatre district", "time slot"))
    #movie_id_rating = [", ".join(str(item)) for item in movie_id_rating]
    for result in movie_ids:
        listbox.insert(tk.END, result)

def average_rating(movie_id):
    cursor = mydb.cursor()
    # get movie name
    sql = "select movie_name from Movies where movie_id = %s"
    movie_name = get_results(cursor, sql, (movie_id,))[0][0]

    sql = "select rating from ratings where movie_id = %s"
    results = get_results(cursor, sql, (movie_id, ))
    overall_rating = sum(item[0] for item in results) / len(results)
    results = [[movie_id, movie_name, float(overall_rating)]]

    # Create a new Toplevel window
    results_window = tk.Toplevel(root)
    results_window.title(f"{movie_id}'s Overall Rating")

    # Create a listbox to display the results
    listbox = tk.Listbox(results_window, width=100)
    listbox.pack()

    # Add results to the listbox
    results.insert(0, ("movie id", "movie name", "overall_rating"))
    #movie_id_rating = [", ".join(str(item)) for item in movie_id_rating]
    for result in results:
        listbox.insert(tk.END, result)

# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("400x200")

# Create the login form
lbl_username = tk.Label(root, text="Username:")
lbl_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

lbl_password = tk.Label(root, text="Password:")
lbl_password.pack()
entry_password = tk.Entry(root)
entry_password.pack()

btn_login = tk.Button(root, text="Login", command=lambda: validate_login(entry_username.get(), entry_password.get()))
btn_login.pack()


# Start the Tkinter event loop
root.mainloop()
