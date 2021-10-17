import pymysql
import pymysql.cursors as cursor_

# Connection to database

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             database="db_pass",
                             cursorclass=cursor_.DictCursor)
##USE ONCE at first run ONLY!
# with connection:
#     with connection.cursor() as concur:
#         #Create a new database
#         sql_statement1 = "CREATE DATABASE db_pass"
#         concur.execute(sql_statement1)

# with connection:
#     with connection.cursor() as concur:
#         #Create a new Table
#         sql_statement2 = """CREATE TABLE Passwords(id int NOT NULL AUTO_INCREMENT,
#                                                     website varchar(255) NOT NULL,
#                                                      email varchar(255) NOT NULL,
#                                                       password varchar(255) NOT NULL,
#                                                       PRIMARY KEY (id))"""
#         concur.execute(sql_statement2)

# with connection:
#      with connection.cursor() as concur:
#          sql_statement3 = "INSERT INTO Passwords(website,email,password) VALUES('myweb','myemail@gg.com','qw123ewq2@@Q')"
#          concur.execute(sql_statement3)
#
#          connection.commit()

with connection:
    with connection.cursor() as concur:
        sql_fetch = """SELECT website,email,password FROM Passwords WHERE website = 'myweb'"""
        concur.execute(sql_fetch)
        result = concur.fetchone()
        if result:
            print(result["email"])
        else:
            print("No Match Found")