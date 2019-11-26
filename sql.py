'''
Resets the db file by clearing out all information and initializing
the tables:
- credentials: username | password
'''
import sqlite3
from sqlite3 import Error
def db_reset(filename):
    open(filename, 'w').close()
    with sqlite3.connect("sample.db") as connection:
        c = connection.cursor()
        c.execute("CREATE TABLE credentials(username TEXT, password TEXT)")
        c.execute('INSERT INTO credentials VALUES("admin", "admin")')

def user_find(conn,user):

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM credentials WHERE username=?", (user,))
        list_of_user_info = cur.fetchall()
        print(list_of_user_info)
        if list_of_user_info == []:
            return(Error)
        return list_of_user_info[0][1]
    except Error as e:
        return(e)

filename = "sample.db"
if __name__ == '__main__':
    db_reset(filename)


# Future implementations
'''
Parses JSON file and insert user information into db
'''
