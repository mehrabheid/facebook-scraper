import mysql.connector

#create object for DataBase connections
class DBconn:
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                        database='your_database_name',
                                        user='your_MySQL_user',
                                        password='your_MySQL_user_password',
                                        auth_plugin='mySQL_auth_plugin #optional')
                                        
        self.cursor = self.connection.cursor()