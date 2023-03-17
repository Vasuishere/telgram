import sqlite3

def viewer():
    conn = sqlite3.connect('RegisteredUser.db')

    cursor = conn.cursor()


    cursor.execute("SELECT * FROM users")

    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()
viewer()