import MySQLdb

db = MySQLdb.connect("localhost", "root", "temppwd", "first_flask")
cursor = db.cursor()

#check the version of mysql
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)

#create table of images
cursor.execute("CREATE TABLE IF NOT EXISTS ImagesDatabase(Id INT PRIMARY KEY AUTO_INCREMENT, User VARCHAR(25), Time VARCHAR(25), Type VARCHAR(25),Path VARCHAR(50))")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Allen','2018-10-19 20:00:00','fat','e:/img1')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Mike','2018-10-19 20:00:02','fat','e:/img2')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('John','2018-10-19 20:00:04','fat','e:/img3')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Amy','2018-10-19 20:00:06','ventricular','e:/img4')")
cursor.execute("INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('James','2018-10-19 20:00:08','brain','e:/img5')")

#check the table
cursor.execute("SELECT * FROM ImagesDatabase")
rows = cursor.fetchall()
for row in rows:
        print (row)

#commit and close
db.commit()
cursor.close()
db.close()