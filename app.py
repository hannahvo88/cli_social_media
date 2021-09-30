import dbcreds
import mariadb

conn = None
cursor = None
loginToken = None

print("Username: ")
username= input()

print("Password: ")
user_password= input()
try:
    conn=mariadb.connect(
                    user=dbcreds.user,
                    password=dbcreds.password,
                    host=dbcreds.host,
                    port=dbcreds.port,
                    database=dbcreds.database
                    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hackers")
    users = cursor.fetchall()
    for user in users:
        cursor.execute("SELECT password FROM hackers WHERE alias=?",[username])
        loginToken = cursor.fetchone()
        print(loginToken)
except mariadb.OperationalError:
    print("There seems to be a connection issue!")
except mariadb.ProgrammingError:
    print("Apparently you do not know how to code")
except mariadb.IntergrityError:
    print("Error with DB integrity, most likely consraint failure")
except:
    print("Opps! Somthing went wrong")

    if loginToken == username:
        print("Please select your option: ")
        print("Enter a new exploit. Press 1")
        print("See all of your exploits. Press 2")
        print("See all other exploits by everyone. Press 3")
        print("Exit the application. Press 4")
        user_action = input ()
    while True:
        try:
            cursor.execute("SELECT id FROM hackers WHERE alias=?", [username])
            loggin_user = cursor.fetchone()
            print(loggin_user)
            if user_action == "1":
                print("Please write new exploit: ")
                exploit = input()
                cursor.execute("INSERT INTO exploits(content, user_id) VALUES(?,?)", [exploit, loggin_user])
                conn.commit()
                print("Your new exploit has been posted")
            elif user_action == "2":
                cursor.execute("SELECT content FROM exploits WHERE user_id=?", [loggin_user])
                contents = cursor.fetchall()
                print(contents)
                for content in contents:
                    print(content)
            elif user_action == "3":
                cursor.execute("SELECT content FROM exploits EXCEPT SELECT content FROM exploits WHERE user_id=?", [loggin_user])
                content_lists = cursor.fetchall()
                print(content_lists)
                for content in content_lists:
                    print(content)
            elif user_action == "4":
                print("Would you like continue?")
                print("Yes = y")
                print("No = n")
                logOut= input()
                if(logOut == "y"):
                    continue
                elif (logOut== "n"):
                    break
                else:
                    continue

        except mariadb.OperationalError:
            print("There seems to be a connection issue!")
        except mariadb.ProgrammingError:
            print("Apparently you do not know how to code")
        except mariadb.IntergrityError:
            print("Error with DB integrity, most likely consraint failure")
        except:
            print("Opps! Somthing went wrong")
        finally:
            if (cursor != None):
                cursor.close()
            else:
                print("No cursor to begin with.")
            
            if (conn != None):
                conn.rollback()
                conn.close()
            else:
                print("No connection!")