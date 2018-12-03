#this program is used to setup the sql table of users 
import MySQLdb

#mysql setup params
host = "localhost"
username = "root"
password = "temppwd"
database_name = "flask_sql"
table_name = "UsersDatabase"

#check the database
db = MySQLdb.connect(host, username, password, database_name)
print('database connected')
cursor = db.cursor()

#create table of images
cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + "(Id INT PRIMARY KEY AUTO_INCREMENT, User VARCHAR(30), Password VARCHAR(30), Time VARCHAR(25), Type VARCHAR(25))")
print ("create table " + table_name)
cursor.execute("INSERT INTO " + table_name + "(User,Password,Time,Type) VALUES('Allen','allen','2018-12-02 13:20:00','super')")
cursor.execute("INSERT INTO " + table_name + "(User,Password,Time,Type) VALUES('Mike','mike','2018-12-02 13:20:00','general')")

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