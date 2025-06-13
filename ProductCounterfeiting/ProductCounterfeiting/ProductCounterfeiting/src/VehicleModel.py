from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class VehicleModel:
    def __init__(self, vehicleID = '',vehicleNbr = '',registrationCertifiateFile = '',insuranceFile = '',transporterID = '',transporterModel = None):
        self.vehicleID = vehicleID
        self.vehicleNbr = vehicleNbr
        self.registrationCertifiateFile = registrationCertifiateFile
        self.insuranceFile = insuranceFile
        self.transporterID = transporterID
        self.transporterModel = transporterModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Vehicle ORDER BY vehicleID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = VehicleModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT vehicleID, vehicleNbr FROM Vehicle ORDER BY vehicleNbr"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = VehicleModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Vehicle WHERE vehicleID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = VehicleModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.vehicleID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Vehicle (vehicleID,vehicleNbr,registrationCertifiateFile,insuranceFile,transporterID) VALUES(?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.vehicleID,obj.vehicleNbr,obj.registrationCertifiateFile,obj.insuranceFile,obj.transporterID))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Vehicle SET vehicleNbr = ?,registrationCertifiateFile = ?,insuranceFile = ?,transporterID = ? WHERE vehicleID = ?"
        cursor.execute(sqlcmd1,  (obj.vehicleNbr,obj.registrationCertifiateFile,obj.insuranceFile,obj.transporterID,obj.vehicleID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Vehicle WHERE vehicleID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

    @staticmethod
    def get_count():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT COUNT(*) FROM Vehicle"
        cursor.execute(sqlcmd1)
        cnt = cursor.fetchval()
        cursor.close()
        conn.close()
        return cnt