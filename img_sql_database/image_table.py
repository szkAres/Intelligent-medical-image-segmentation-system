import MySQLdb

class image_table():
    
    def __init__(self,Database = None,Table = None,db=None,cursor=None,results = None):
        self.database = Database
        self.table = Table
        
    def connect_to_database(self):
        self.db = MySQLdb.connect("localhost", "root", "temppwd", self.database)
        self.cursor = self.db.cursor()
        print('database '+self.database+' connected')
        
    def disconnect_database(self):
        self.cursor.close()
        self.db.close()
        print('database '+self.database+' disconnected')
        
    def check_by_type(self,type_name,print_out):
        sql_command = "SELECT * FROM " + self.table + " WHERE Type = '" + type_name + "'"
        print(sql_command)
        self.cursor.execute(sql_command)
        self.results = self.cursor.fetchall()
        print('select ' + type_name + ' done')
        if(print_out == True):
            for row in self.results:
                result_id = row[0]
                result_user = row[1]
                result_time = row[2]
                result_type = row[3]
                result_path = row[4]
                print(str(result_id)+result_user+result_time+result_type+result_path)
                
    def check_by_user(self,user_name,print_out):
        sql_command = "SELECT * FROM " + self.table + " WHERE User = '" + user_name + "'"
        print(sql_command)
        self.cursor.execute(sql_command)
        self.results = self.cursor.fetchall()
        print('select ' + user_name + ' done')
        if(print_out == True):
            for row in self.results:
                result_id = row[0]
                result_user = row[1]
                result_time = row[2]
                result_type = row[3]
                result_path = row[4]
                print(str(result_id)+result_user+result_time+result_type+result_path)