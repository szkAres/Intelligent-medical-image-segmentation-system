import MySQLdb

class medical_image():
    
    def __init__(self,User = None,Time = None,Type = None,Path=None,Image = None,db=None,cursor=None,data_fetched = None):
        self.User = User
        self.Time = Time
        self.Type = Type
        self.Path = Path
        self.Image = Image
        
    def connect_to_database(self,host,username,password,database_name):
        self.db = MySQLdb.connect(host, username, password, database_name)
        self.cursor = self.db.cursor()
        print('database connected')
        
    def disconnect_database(self):
        self.cursor.close()
        self.db.close()
        print('database disconnected')
        
    def commit_database(self):
        self.db.commit()
        print('database committed')
        
    def check_database_version(self):
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print ("Database version : %s " % data)
        
    def insert(self,table_name):
        sql_command = "INSERT INTO " + table_name + "(User,Time,Type,Path) VALUES('"+self.User+"','"+self.Time+"','"+self.Type+"','"+self.Path+"')"
        print(sql_command)
        self.cursor.execute(sql_command)
        print('insert done')
        
    def select(self,table_name):
        self.cursor.execute("SELECT * FROM " + table_name)
        print('select done')
        
    def read(self):
        self.data_fetched = self.cursor.fetchone()
        self.User = self.data_fetched[1]
        self.Time = self.data_fetched[2]
        self.Type = self.data_fetched[3]
        self.Path = self.data_fetched[4]
        print('read done '+ self.User + ' '+ self.Time + ' ' + self.Type + ' ' + self.Path)
        
    def select_by_type(self,type_name,table_name):
        sql_command = "SELECT * FROM " + table_name + " WHERE Type = '" + type_name + "'"
        print(sql_command)
        self.cursor.execute(sql_command)
        print('select ' + type_name + ' done')
        
    def select_by_user(self,user_name,table_name):
        sql_command = "SELECT * FROM " + table_name + " WHERE User = '" + user_name + "'"
        print(sql_command)
        self.cursor.execute(sql_command)
        print('select ' + user_name + ' done')