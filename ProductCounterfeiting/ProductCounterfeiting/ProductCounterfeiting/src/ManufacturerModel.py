from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class ManufacturerModel:
    def __init__(self, manufacturerID = '',manufacturerName = '',address = '',contactNbr = '',email = '',address1 = '',city = '',county = '',postcode = '',country = '',gstNumber = '',licenseFile = ''):
        self.manufacturerID = manufacturerID
        self.manufacturerName = manufacturerName
        self.address = address
        self.contactNbr = contactNbr
        self.email = email
        self.address1 = address1
        self.city = city
        self.county = county
        self.postcode = postcode
        self.country = country
        self.gstNumber = gstNumber
        self.licenseFile = licenseFile
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Manufacturer ORDER BY manufacturerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ManufacturerModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT manufacturerID, manufacturerName FROM Manufacturer ORDER BY manufacturerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ManufacturerModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Manufacturer WHERE manufacturerID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = ManufacturerModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.manufacturerID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Manufacturer (manufacturerID,manufacturerName,address,contactNbr,email,address1,city,county,postcode,country,gstNumber,licenseFile) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.manufacturerID,obj.manufacturerName,obj.address,obj.contactNbr,obj.email,obj.address1,obj.city,obj.county,obj.postcode,obj.country,obj.gstNumber,obj.licenseFile))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Manufacturer SET manufacturerName = ?,address = ?,contactNbr = ?,email = ?,address1 = ?,city = ?,county = ?,postcode = ?,country = ?,gstNumber = ?,licenseFile = ? WHERE manufacturerID = ?"
        cursor.execute(sqlcmd1,  (obj.manufacturerName,obj.address,obj.contactNbr,obj.email,obj.address1,obj.city,obj.county,obj.postcode,obj.country,obj.gstNumber,obj.licenseFile,obj.manufacturerID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Manufacturer WHERE manufacturerID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

    @staticmethod
    def get_count():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT COUNT(*) FROM Manufacturer"
        cursor.execute(sqlcmd1)
        cnt = cursor.fetchval()
        cursor.close()
        conn.close()
        return cnt

