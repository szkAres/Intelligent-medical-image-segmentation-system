import MySQLdb

class medical_image():
    
    def __init__(self,User = None,Time = None,Type = None,Path=None,Image = None,db=None,cursor=None,data_fetched = None):
        self.User = User
        self.Time = Time
        self.Type = Type
        self.Path = Path
        self.Image = Image
        
    def connect_to_database(self):
        self.db = MySQLdb.connect("localhost", "root", "temppwd", "first_flask")
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
        
    def insert(self):
        sql_command = "INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('"+self.User+"','"+self.Time+"','"+self.Type+"','"+self.Path+"')"
        print(sql_command)
        self.cursor.execute(sql_command)
        print('insert done')
        
    def select(self):
        self.cursor.execute("SELECT * FROM ImagesDatabase")
        print('select done')
        
    def read(self):
        self.data_fetched = self.cursor.fetchone()
        self.User = self.data_fetched[1]
        self.Time = self.data_fetched[2]
        self.Type = self.data_fetched[3]
        self.Path = self.data_fetched[4]
        print('read done '+ self.User + ' '+ self.Time + ' ' + self.Type + ' ' + self.Path)
        
    def select_by_type(self,type_name):
        sql_command = "SELECT * FROM ImagesDatabase WHERE Type = '" + type_name + "'"
        print(sql_command)
        self.cursor.execute(sql_command)
        print('select ' + type_name + ' done')