from class_user import class_user
import datetime

#mysql setup
host = "localhost"
username = "root"
password = "temppwd"
database_name = "flask_sql"
table_name = "UsersDatabase"

user1 = class_user('Allen')
user1.connect_to_database(host,username,password,database_name)
user1.user_check(table_name)
user1.disconnect_database()

user2 = class_user('Mike')
user2.connect_to_database(host,username,password,database_name)
user2.user_check(table_name)
user2.disconnect_database()

user3 = class_user('John')
user3.connect_to_database(host,username,password,database_name)
user3.user_check(table_name)
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
user3.user_create(table_name,'john',nowTime,False)
user3.disconnect_database()

user4 = class_user('Amy')
user4.connect_to_database(host,username,password,database_name)
user4.user_check(table_name)
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
user4.user_create(table_name,'amy',nowTime,False)
user4.disconnect_database()

user5 = class_user('James')
user5.connect_to_database(host,username,password,database_name)
user5.user_check(table_name)
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
user5.user_create(table_name,'james',nowTime,True)
user5.disconnect_database()