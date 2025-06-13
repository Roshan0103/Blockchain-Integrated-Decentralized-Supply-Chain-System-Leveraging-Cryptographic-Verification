from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class DispatchModel:
    def __init__(self, uniqueID = '',dsipatchDate = None,lotNumber = 0,vehicleID = '',vehicleModel = None):
        self.uniqueID = uniqueID
        self.dsipatchDate = dsipatchDate
        self.lotNumber = lotNumber
        self.vehicleID = vehicleID
        self.vehicleModel = vehicleModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Dispatch ORDER BY uniqueID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = DispatchModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT uniqueID, productID FROM Dispatch ORDER BY productID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = DispatchModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Dispatch WHERE uniqueID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = DispatchModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.uniqueID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Dispatch (uniqueID,dsipatchDate,lotNumber,vehicleID) VALUES(?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.uniqueID,datetime.datetime.strptime(obj.dsipatchDate.replace('T', ' '), '%Y-%m-%d'),obj.lotNumber,obj.vehicleID))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Dispatch SET dsipatchDate = ?,lotNumber = ?,vehicleID = ? WHERE uniqueID = ?"
        cursor.execute(sqlcmd1,  (datetime.datetime.strptime(obj.dsipatchDate.replace('T', ' '), '%Y-%m-%d'),obj.lotNumber,obj.vehicleID,obj.uniqueID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Dispatch WHERE uniqueID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

