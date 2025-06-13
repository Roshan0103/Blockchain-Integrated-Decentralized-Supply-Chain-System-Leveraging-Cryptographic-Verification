from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class TransporterModel:
    def __init__(self, transporterID = '',transporterName = '',contactNbr = '',gstNumber = '',gstCertificateFile = ''):
        self.transporterID = transporterID
        self.transporterName = transporterName
        self.contactNbr = contactNbr
        self.gstNumber = gstNumber
        self.gstCertificateFile = gstCertificateFile
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Transporter ORDER BY transporterName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = TransporterModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT transporterID, transporterName FROM Transporter ORDER BY transporterName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = TransporterModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Transporter WHERE transporterID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = TransporterModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.transporterID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Transporter (transporterID,transporterName,contactNbr,gstNumber,gstCertificateFile) VALUES(?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.transporterID,obj.transporterName,obj.contactNbr,obj.gstNumber,obj.gstCertificateFile))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Transporter SET transporterName = ?,contactNbr = ?,gstNumber = ?,gstCertificateFile = ? WHERE transporterID = ?"
        cursor.execute(sqlcmd1,  (obj.transporterName,obj.contactNbr,obj.gstNumber,obj.gstCertificateFile,obj.transporterID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Transporter WHERE transporterID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

