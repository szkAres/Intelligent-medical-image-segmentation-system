import MySQLdb

class class_user():
    
    def __init__(self,User = None,Password = None,Time = None,Type = None,exist = False ,db=None,cursor=None,data_fetched = None):
        self.User = User
        
    def connect_to_database(self,host,username,password,database_name):
        self.db = MySQLdb.connect(host, username, password, database_name)
        self.cursor = self.db.cursor()
        print('database connected')
        
    def disconnect_database(self):
        self.cursor.close()
        self.db.close()
        print('database disconnected')
        
    def user_check(self,table_name):
        sql_command = "SELECT * FROM " + table_name + " WHERE User = '" + self.User + "'"
        print(sql_command)
        self.cursor.execute(sql_command)
        self.data_fetched = self.cursor.fetchone()
        if self.data_fetched == None:
            self.Password = None
            self.Time = None
            self.Type = None
            self.exist = False
            print('user ' + self.User + ' not exists')
        else:
            self.Password = self.data_fetched[2]
            self.Time = self.data_fetched[3]
            self.Type = self.data_fetched[4]
            self.exist = True
            print('check done '+ self.User + ' '+ self.Password + ' ' + self.Time + ' ' + self.Type)
        
    def user_create(self,table_name,password_set,time_now,is_super):
        if self.exist == True:
            print('create wrong, user ' + self.User + ' exists')
            return
        if is_super == True:
            sql_command = "INSERT INTO " + table_name + "(User,Password,Time,Type) VALUES('"+self.User+"','"+password_set+"','"+time_now+"','super')"
            print(sql_command)
            self.cursor.execute(sql_command)
            print('super user ' + self.User + ' insert done')
        else:
            sql_command = "INSERT INTO " + table_name + "(User,Password,Time,Type) VALUES('"+self.User+"','"+password_set+"','"+time_now+"','general')"
            print(sql_command)
            self.cursor.execute(sql_command)
            print('general user ' + self.User + ' insert done')
        self.db.commit()
        print('database committed')