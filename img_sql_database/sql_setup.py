#this program is used to setup the sql and create the image database and table
import MySQLdb

#mysql setup params
host = "localhost"
username = "root"
password = "temppwd"
database_name = "flask_sql"
table_name = "ImagesDatabase"

#create the database
db = MySQLdb.connect(host, username, password)
cursor = db.cursor()
cursor.execute("CREATE database " + database_name)
print ("create database " + database_name)
db.commit()
cursor.close()
db.close()

#check the database
db = MySQLdb.connect(host, username, password, database_name)
print('database connected')
cursor = db.cursor()
#check the version of mysql
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)

#create table of images
cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + "(Id INT PRIMARY KEY AUTO_INCREMENT, User VARCHAR(25), Time VARCHAR(25), Type VARCHAR(25),Path VARCHAR(200))")
print ("create table " + table_name)
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Allen','2018-10-19 20:00:00','fat','e:/img1')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Mike','2018-10-19 20:00:02','fat','e:/img2')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('John','2018-10-19 20:00:04','fat','e:/img3')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Amy','2018-10-19 20:00:06','ventricular','e:/img4')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('James','2018-10-19 20:00:08','brain','e:/img5')")

#check the table
cursor.execute("SELECT * FROM " + table_name)
rows = cursor.fetchall()
for row in rows:
        print (row)

#commit and close
db.commit()
cursor.close()
db.close()
print('database disconnected')