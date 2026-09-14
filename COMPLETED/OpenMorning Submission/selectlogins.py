import sqlite3 as sq
import encrypter


def selectlogins():
    connection = sq.connect("NavigationAppData.db")
    cursor = connection.cursor()
    select_query = ("SELECT * FROM LoginDetails")
    result = cursor.execute(select_query)
    details = []
    for item in result:
        details.append(item)

    connection.close()

    decryptlogins(details)

def decryptlogins(details):
    usernames = [item[0] for item in details]
    encrypted_passwords = [item[1] for item in details]
    keys = [item[2] for item in details]
    passwords = [encrypter.decrypt(encrypted_passwords[item],keys[item]) for item in range(len(encrypted_passwords))]
    user_pass = [(usernames[item],passwords[item]) for item in range(len(usernames))]
    return user_pass


