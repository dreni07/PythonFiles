import sqlite3
import models
import validating
def create_connection():
    conn = sqlite3.connect('app.db')
    return conn

def createUsers():
    the_connection = create_connection()
    cursor = the_connection.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id integer primary key autoincrement,
            username text not null,
            email text not null,
            password text not null
        );''')
    except Exception as e:
        print('Failed Due To',str(e))
    finally:
        the_connection.close()

createUsers()

def createFileHandlers():
    the_connection = create_connection()
    cursor = the_connection.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS files(
            file_id integer primary key autoincrement,
            file_name text not null,
            file_type text not null,
            user_id integer,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );''')
        the_connection.commit()
    except Exception as e:
        print('Failed Because Of',str(e))
    finally:
        the_connection.close()

createFileHandlers()

def is_username_valid(user:models.userModel):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM users WHERE username = :username;''',{'username':user.username})
        the_fetched = the_cursor.fetchall()
        if the_fetched:
             return True
        else:
            return False
    except Exception as e:
        print('Failed Due To',str(e))
    finally:
        the_connection.close()


def checking_username(user:models.userModel):
    the_answer = is_username_valid(user)
    if the_answer:
        return {'success':'User Exists'}
    else:
        return {'success':'User Not Exists'}

def insertData(user:models.userModel):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''INSERT INTO users (username,email,password) VALUES (?,?,?); ''',(user.username,user.email,user.password))
        connection.commit()
        get_changed = cursor.rowcount

        if get_changed:
            return {'success': 'True'}
        else:
            return {'success': 'False'}

    except Exception as e:
        print(str(e))
        return {'success':'Failed ADDING'}
    finally:
        connection.close()



def logIn(user:models.logInModel):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE username = :username AND password = :password',{"username":user.username,"password":user.password})
        fetching = cursor.fetchone()
        if fetching:
            return {'success':'True','data':fetching}
        else:
            return {'success':'False'}
    except Exception as e:
        print('Failed Bro',str(e))


def addingFile(file:models.fileUploader):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''INSERT INTO files (file_name,file_type,user_id) VALUES (:file_name,:file_type,:user_id);''',{"file_name":file.file_name,"file_type":file.file_type,"user_id":file.user_id})
        connection.commit()
        count_changed = cursor.rowcount
        if count_changed:
            return {'File Added':'Successfully'}
        else:
            return {'File Added':'Failed To Add'}
    except Exception as e:
        print('Failed Adding Due To',str(e))

    finally:
        connection.close()

def is_file_valid(file:models.fileUploader):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''SELECT * FROM files WHERE file_name = :file_name AND user_id = :user_id;''',{'file_name':file.file_name,'user_id':file.user_id})
        fetching = cursor.fetchall()
        if fetching:
            return {'success':'File Exists'}
        else:
            return {'success':'File Does Not Exist'}
    except Exception as e:
        print('Failed Because Of',str(e))

    finally:
        connection.close()

def see_files(userId:int):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''SELECT * FROM files INNER JOIN users ON files.user_id = users.id WHERE users.id = :user_id''',{'user_id':userId})
        fetched = cursor.fetchall()
        if fetched:
            return {'data':fetched}
        else:
            return {'data':'Failed'}
    except Exception as e:
        print('Failed Because Of',str(e))
    finally:
        connection.close()










