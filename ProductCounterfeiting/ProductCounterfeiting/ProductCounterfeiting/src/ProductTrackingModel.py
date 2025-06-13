from Constants import connString
import pyodbc
import datetime
import uuid
import time    
from Constants import contract_address
from web3 import Web3, HTTPProvider
import json
import pprint

from ProductCounterfeiting.ProductCounterfeiting.src.ProductModel import ProductModel


class ProductTrackingModel:
    def __init__(self, uniqueID = '',productID = '',productUniqueIdentifier = 0,lotNumber = 0,isBlockChainGenerated = False,hash = '',prevHash = '',sequenceNumber = 0,productModel = None):
        self.uniqueID = uniqueID
        self.productID = productID
        self.productUniqueIdentifier = productUniqueIdentifier
        self.lotNumber = lotNumber
        self.isBlockChainGenerated = isBlockChainGenerated
        self.hash = hash
        self.prevHash = prevHash
        self.sequenceNumber = sequenceNumber
        self.productModel = productModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductTracking ORDER BY productID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductTrackingModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7])
            row.productModel = ProductModel.get_by_id(dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_top_10_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT TOP 10 * FROM ProductTracking ORDER BY sequenceNumber DESC"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductTrackingModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7])
            row.productModel = ProductModel.get_by_id(dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records



    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT uniqueID, productID FROM ProductTracking ORDER BY productID"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductTrackingModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductTracking WHERE uniqueID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = ProductTrackingModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.uniqueID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO ProductTracking (uniqueID,productID,lotNumber,isBlockChainGenerated,hash,prevHash,sequenceNumber) VALUES(?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.uniqueID,obj.productID,obj.lotNumber,obj.isBlockChainGenerated,obj.hash,obj.prevHash,obj.sequenceNumber))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../ProductCounterfeiting-Truffle/build/contracts/ProductTrackingContract.json'
        deployed_contract_address = contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.uniqueID, obj.productID, int(obj.productUniqueIdentifier), int(obj.lotNumber)).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE ProductTracking SET productID = ?,lotNumber = ?,isBlockChainGenerated = ?,hash = ?,prevHash = ?,sequenceNumber = ? WHERE uniqueID = ?"
        cursor.execute(sqlcmd1,  (obj.productID,obj.lotNumber,obj.isBlockChainGenerated,obj.hash,obj.prevHash,obj.sequenceNumber,obj.uniqueID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM ProductTracking WHERE uniqueID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

    @staticmethod
    def get_count():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT COUNT(*) FROM ProductTracking"
        cursor.execute(sqlcmd1)
        cnt = cursor.fetchval()
        cursor.close()
        conn.close()
        return cnt