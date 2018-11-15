from medical_image import medical_image

#mysql setup
host = "localhost"
username = "root"
password = "temppwd"
database_name = "flask_sql"
table_name = "ImagesDatabase"

image_write = medical_image('Adams','2018-10-26 11:21:00','fat','E:/1.jpg')
image_write.connect_to_database(host,username,password,database_name)
image_write.check_database_version()
image_write.insert(table_name)
image_write.commit_database()
image_write.disconnect_database()

image_read = medical_image()
image_read.connect_to_database(host,username,password,database_name)
#image_read.select(table_name)
image_read.select_by_type('ventricular',table_name)
image_read.read()
print(image_read.User + ' '+ image_read.Time + ' ' + image_read.Type + ' ' + image_read.Path)

image_read.select_by_user('Mike',table_name)
image_read.read()
print(image_read.User + ' '+ image_read.Time + ' ' + image_read.Type + ' ' + image_read.Path)

image_read.disconnect_database()