from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class ProductionReceiptsModel:
    def __init__(self, uniqueID = '',effDate = None,manufacturerID = '',productID = '',lotNumber = 0,manufacturerModel = None,productModel = None):
        self.uniqueID = uniqueID
        self.effDate = effDate
        self.manufacturerID = manufacturerID
        self.productID = productID
        self.lotNumber = lotNumber
        self.manufacturerModel = manufacturerModel
        self.productModel = productModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionReceipts ORDER BY productID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductionReceiptsModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT uniqueID, productID FROM ProductionReceipts ORDER BY productID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductionReceiptsModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionReceipts WHERE uniqueID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = ProductionReceiptsModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.uniqueID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO ProductionReceipts (uniqueID,effDate,manufacturerID,productID) VALUES(?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.uniqueID,datetime.datetime.strptime(obj.effDate.replace('T', ' '), '%Y-%m-%d'),obj.manufacturerID,obj.productID))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE ProductionReceipts SET effDate = ?,manufacturerID = ?,productID = ? WHERE uniqueID = ?"
        cursor.execute(sqlcmd1,  (datetime.datetime.strptime(obj.effDate.replace('T', ' '), '%Y-%m-%d'),obj.manufacturerID,obj.productID,obj.uniqueID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM ProductionReceipts WHERE uniqueID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

