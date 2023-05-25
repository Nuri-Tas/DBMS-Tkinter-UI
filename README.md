# DBMS-Tkinter-UI

That is how the directory should look like 

```
${ROOT}
├── firstpage.py
├── audienceoperations.py
├── dbmanageroperations.py
├── directoroperations.py
├── createTables.sql
├── insertTables.sql
├── dropTables.sql
```

`createTables.sql` and `dropTables.sql` files must be run to set up the database. 

The default MYSQL connection credentials are given below and they shall be changed according to the user credentials on all .py files (`firstpage.py, dbmanageroperations.py, directoroperations.py, audience.py`):


```
PASSWORD = "nuri"
DATABASE_NAME = "movie_db2"

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database=DATABASE_NAME
)
).
```


