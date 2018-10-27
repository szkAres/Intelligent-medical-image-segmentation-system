from medical_image import medical_image

image_write = medical_image('Adams','2018-10-26 11:21:00','fat','E:/1.jpg')
image_write.connect_to_database()
image_write.check_database_version()
image_write.insert()
image_write.commit_database()
image_write.disconnect_database()

image_read = medical_image()
image_read.connect_to_database()
#image_read.select()
image_read.select_by_type('ventricular')
image_read.read()
image_read.disconnect_database()

print(image_read.User + ' '+ image_read.Time + ' ' + image_read.Type + ' ' + image_read.Path)