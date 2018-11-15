from image_table import image_table

#mysql setup
host = "localhost"
username = "root"
password = "temppwd"
database_name = "flask_sql"
table_name = "ImagesDatabase"

image_table_test = image_table(database_name,table_name)
image_table_test.connect_to_database(host,username,password)
#true:print the table; false:not print the table 
image_table_test.check_by_type('fat',True)
image_table_test.check_by_user('Allen',True)
image_table_test.check_all(True)
image_table_test.disconnect_database()