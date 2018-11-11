from image_table import image_table

image_table_test = image_table('first_flask','ImagesDatabase')
image_table_test.connect_to_database()
image_table_test.check_by_type('fat',True)
image_table_test.check_by_user('Allen',True)
image_table_test.disconnect_database()