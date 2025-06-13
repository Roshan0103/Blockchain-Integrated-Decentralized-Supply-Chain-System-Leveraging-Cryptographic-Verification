
from flask import Flask, request, render_template, redirect, url_for
import os
import pyodbc
import uuid
import time
from datetime import datetime
from Constants import connString

from DispatchModel import DispatchModel
from ManufacturerModel import ManufacturerModel
from ProductModel import ProductModel
from ProductionReceiptsModel import ProductionReceiptsModel
from ProductTrackingModel import ProductTrackingModel
from RoleModel import RoleModel
from TransporterModel import TransporterModel
from UsersModel import UsersModel
from VehicleModel import VehicleModel




app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
emailid = ""
role_object = None
message = ""
msgType = ""
uploaded_file_name = ""

def initialize():
    global message, msgType
    message = ""
    msgType = ""

def process_role(option_id):

    
    if option_id == 0:
        if role_object.canDispatch == False:
            return False
        
    if option_id == 1:
        if role_object.canManufacturer == False:
            return False
        
    if option_id == 2:
        if role_object.canProduct == False:
            return False
        
    if option_id == 3:
        if role_object.canProductionReceipts == False:
            return False
        
    if option_id == 4:
        if role_object.canProductTracking == False:
            return False
        
    if option_id == 5:
        if role_object.canRole == False:
            return False
        
    if option_id == 6:
        if role_object.canTransporter == False:
            return False
        
    if option_id == 7:
        if role_object.canUsers == False:
            return False
        
    if option_id == 8:
        if role_object.canVehicle == False:
            return False
        

    return True



@app.route("/")
def index():
    global user_id, emailid
    return render_template("Login.html")

def get_dashboard():
    product_count = ProductModel.get_count()
    manufacture_count = ManufacturerModel.get_count()
    vehicle_count = VehicleModel.get_count()
    tracking_count = ProductTrackingModel.get_count()
    top_10_records = ProductTrackingModel.get_top_10_all()
    return product_count, manufacture_count, vehicle_count, tracking_count, top_10_records
@app.route("/processLogin", methods=["POST"])
def processLogin():
    global user_id, emailid, role_object
    emailid = request.form["emailid"]
    password = request.form["password"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + password + "' AND isActive = 1";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()

    cur1.commit()
    if not row:
        return render_template("Login.html", processResult="Invalid Credentials")
    user_id = row[0]

    cur2 = conn1.cursor()
    sqlcmd2 = "SELECT * FROM Role WHERE RoleID = '" + str(row[6]) + "'"
    cur2.execute(sqlcmd2)
    row2 = cur2.fetchone()

    if not row2:
        return render_template("Login.html", processResult="Invalid Role")

    role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6], row2[7], row2[8], row2[9], row2[10])
    product_count, manufacture_count, vehicle_count, tracking_count, top_10_records = get_dashboard()
    return render_template("Dashboard.html", product_count=product_count, manufacture_count=manufacture_count, vehicle_count=vehicle_count, tracking_count=tracking_count, top_10_records=top_10_records)


@app.route("/ChangePassword")
def changePassword():
    global user_id, emailid
    return render_template("ChangePassword.html")


@app.route("/ProcessChangePassword", methods=["POST"])
def processChangePassword():
    global user_id, emailid
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + oldPassword + "'";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()
    cur1.commit()
    if not row:
        return render_template("ChangePassword.html", msg="Invalid Old Password")

    if newPassword.strip() != confirmPassword.strip():
        return render_template("ChangePassword.html", msg="New Password and Confirm Password are NOT same")

    conn2 = pyodbc.connect(connString, autocommit=True)
    cur2 = conn2.cursor()
    sqlcmd2 = "UPDATE Users SET password = '" + newPassword + "' WHERE emailid = '" + emailid + "'";
    cur1.execute(sqlcmd2)
    cur2.commit()
    return render_template("ChangePassword.html", msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, emailid
    product_count, manufacture_count, vehicle_count, tracking_count, top_10_records = get_dashboard()
    return render_template("Dashboard.html", product_count=product_count, manufacture_count=manufacture_count,
                           vehicle_count=vehicle_count, tracking_count=tracking_count, top_10_records=top_10_records)


@app.route("/Information")
def Information():
    global message, msgType
    return render_template("Information.html", msgType=msgType, message=message)



@app.route("/DispatchListing")
def Dispatch_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canDispatch = process_role(0)

    if canDispatch == False:
        message = "You Don't Have Permission to Access Dispatch"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = DispatchModel.get_all()

    return render_template("DispatchListing.html", records=records)

@app.route("/DispatchOperation")
def Dispatch_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canDispatch = process_role(0)

    if not canDispatch:
        message = "You Don't Have Permission to Access Dispatch"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = DispatchModel("", "")

    Dispatch = DispatchModel.get_all()
    vehicle_list = VehicleModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = DispatchModel.get_by_id(unique_id)

    return render_template("DispatchOperation.html", row=row, operation=operation, Dispatch=Dispatch, vehicle_list = vehicle_list)

@app.route("/ProcessDispatchOperation", methods=["POST"])
def process_Dispatch_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canDispatch = process_role(0)
    if not canDispatch:
        message = "You Don't Have Permission to Access Dispatch"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = DispatchModel("", "")

    if operation != "Delete":
       obj.uniqueID = request.form['uniqueID']
       obj.dsipatchDate = request.form['dsipatchDate']
       obj.lotNumber = request.form['lotNumber']
       obj.vehicleID = request.form['vehicleID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.uniqueID = request.form["uniqueID"]
        obj.update(obj)

    if operation == "Delete":
        uniqueID = request.form["uniqueID"]
        obj.delete(uniqueID)


    return redirect(url_for("Dispatch_listing"))
                    
@app.route("/ManufacturerListing")
def Manufacturer_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canManufacturer = process_role(1)

    if canManufacturer == False:
        message = "You Don't Have Permission to Access Manufacturer"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ManufacturerModel.get_all()

    return render_template("ManufacturerListing.html", records=records)

@app.route("/ManufacturerOperation")
def Manufacturer_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canManufacturer = process_role(1)

    if not canManufacturer:
        message = "You Don't Have Permission to Access Manufacturer"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ManufacturerModel("", "")

    Manufacturer = ManufacturerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ManufacturerModel.get_by_id(unique_id)

    return render_template("ManufacturerOperation.html", row=row, operation=operation, Manufacturer=Manufacturer, )

@app.route("/ProcessManufacturerOperation", methods=["POST"])
def process_Manufacturer_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canManufacturer = process_role(1)
    if not canManufacturer:
        message = "You Don't Have Permission to Access Manufacturer"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ManufacturerModel("", "")

    if operation != "Delete":
       obj.manufacturerID = request.form['manufacturerID']
       obj.manufacturerName = request.form['manufacturerName']
       obj.address = request.form['address']
       obj.contactNbr = request.form['contactNbr']
       obj.email = request.form['email']
       obj.address1 = request.form['address1']
       obj.city = request.form['city']
       obj.county = request.form['county']
       obj.postcode = request.form['postcode']
       obj.country = request.form['country']
       obj.gstNumber = request.form['gstNumber']
       if len(request.files) != 0 :
        
                file = request.files['licenseFile']
                if file.filename != '':
                    licenseFile = file.filename
                    obj.licenseFile = licenseFile
                    f = os.path.join('static/UPLOADED_FILES', licenseFile)
                    file.save(f)
                else:
                    obj.licenseFile = request.form['hlicenseFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.manufacturerID = request.form["manufacturerID"]
        obj.update(obj)

    if operation == "Delete":
        manufacturerID = request.form["manufacturerID"]
        obj.delete(manufacturerID)


    return redirect(url_for("Manufacturer_listing"))
                    
@app.route("/ProductListing")
def Product_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProduct = process_role(2)

    if canProduct == False:
        message = "You Don't Have Permission to Access Product"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ProductModel.get_all()

    return render_template("ProductListing.html", records=records)

@app.route("/ProductOperation")
def Product_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProduct = process_role(2)

    if not canProduct:
        message = "You Don't Have Permission to Access Product"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ProductModel("", "")

    Product = ProductModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ProductModel.get_by_id(unique_id)

    return render_template("ProductOperation.html", row=row, operation=operation, Product=Product, )

@app.route("/ProcessProductOperation", methods=["POST"])
def process_Product_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canProduct = process_role(2)
    if not canProduct:
        message = "You Don't Have Permission to Access Product"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ProductModel("", "")

    if operation != "Delete":
       obj.productID = request.form['productID']
       obj.productName = request.form['productName']
       obj.packageSize = request.form['packageSize']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.productID = request.form["productID"]
        obj.update(obj)

    if operation == "Delete":
        productID = request.form["productID"]
        obj.delete(productID)


    return redirect(url_for("Product_listing"))
                    
@app.route("/ProductionReceiptsListing")
def ProductionReceipts_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductionReceipts = process_role(3)

    if canProductionReceipts == False:
        message = "You Don't Have Permission to Access ProductionReceipts"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ProductionReceiptsModel.get_all()

    return render_template("ProductionReceiptsListing.html", records=records)

@app.route("/ProductionReceiptsOperation")
def ProductionReceipts_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductionReceipts = process_role(3)

    if not canProductionReceipts:
        message = "You Don't Have Permission to Access ProductionReceipts"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ProductionReceiptsModel("", "")

    ProductionReceipts = ProductionReceiptsModel.get_all()
    manufacturer_list = ManufacturerModel.get_name_id()
    product_list = ProductModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ProductionReceiptsModel.get_by_id(unique_id)

    return render_template("ProductionReceiptsOperation.html", row=row, operation=operation, ProductionReceipts=ProductionReceipts, manufacturer_list = manufacturer_list,product_list = product_list)

@app.route("/ProcessProductionReceiptsOperation", methods=["POST"])
def process_ProductionReceipts_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canProductionReceipts = process_role(3)
    if not canProductionReceipts:
        message = "You Don't Have Permission to Access ProductionReceipts"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ProductionReceiptsModel("", "")

    if operation != "Delete":
       obj.uniqueID = request.form['uniqueID']
       obj.effDate = request.form['effDate']
       obj.manufacturerID = request.form['manufacturerID']
       obj.productID = request.form['productID']
       obj.lotNumber = request.form['lotNumber']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.uniqueID = request.form["uniqueID"]
        obj.update(obj)

    if operation == "Delete":
        uniqueID = request.form["uniqueID"]
        obj.delete(uniqueID)


    return redirect(url_for("ProductionReceipts_listing"))
                    
@app.route("/ProductTrackingListing")
def ProductTracking_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductTracking = process_role(4)

    if canProductTracking == False:
        message = "You Don't Have Permission to Access ProductTracking"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ProductTrackingModel.get_all()

    return render_template("ProductTrackingListing.html", records=records)

@app.route("/ProductTrackingOperation")
def ProductTracking_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductTracking = process_role(4)

    if not canProductTracking:
        message = "You Don't Have Permission to Access ProductTracking"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ProductTrackingModel("", "")

    ProductTracking = ProductTrackingModel.get_all()
    product_list = ProductModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ProductTrackingModel.get_by_id(unique_id)

    return render_template("ProductTrackingOperation.html", row=row, operation=operation, ProductTracking=ProductTracking, product_list = product_list)

@app.route("/ProcessProductTrackingOperation", methods=["POST"])
def process_ProductTracking_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canProductTracking = process_role(4)
    if not canProductTracking:
        message = "You Don't Have Permission to Access ProductTracking"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ProductTrackingModel("", "")

    if operation != "Delete":
       obj.uniqueID = request.form['uniqueID']
       obj.productID = request.form['productID']
       obj.productUniqueIdentifier = request.form['productUniqueIdentifier']
       obj.lotNumber = request.form['lotNumber']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.uniqueID = request.form["uniqueID"]
        obj.update(obj)

    if operation == "Delete":
        uniqueID = request.form["uniqueID"]
        obj.delete(uniqueID)


    return redirect(url_for("ProductTracking_listing"))
                    
@app.route("/RoleListing")
def Role_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(5)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RoleModel.get_all()

    return render_template("RoleListing.html", records=records)

@app.route("/RoleOperation")
def Role_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(5)

    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RoleModel("", "")

    Role = RoleModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RoleModel.get_by_id(unique_id)

    return render_template("RoleOperation.html", row=row, operation=operation, Role=Role, )

@app.route("/ProcessRoleOperation", methods=["POST"])
def process_Role_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRole = process_role(5)
    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RoleModel("", "")

    if operation != "Delete":
       obj.roleID = request.form['roleID']
       obj.roleName = request.form['roleName']
       obj.canRole = 0 
       if request.form.get("canRole") != None : 
              obj.canRole = 1       
       obj.canUsers = 0 
       if request.form.get("canUsers") != None : 
              obj.canUsers = 1       
       obj.canDispatch = 0 
       if request.form.get("canDispatch") != None : 
              obj.canDispatch = 1       
       obj.canManufacturer = 0 
       if request.form.get("canManufacturer") != None : 
              obj.canManufacturer = 1       
       obj.canProduct = 0 
       if request.form.get("canProduct") != None : 
              obj.canProduct = 1       
       obj.canProductionReceipts = 0 
       if request.form.get("canProductionReceipts") != None : 
              obj.canProductionReceipts = 1       
       obj.canProductTracking = 0 
       if request.form.get("canProductTracking") != None : 
              obj.canProductTracking = 1       
       obj.canTransporter = 0 
       if request.form.get("canTransporter") != None : 
              obj.canTransporter = 1       
       obj.canVehicle = 0 
       if request.form.get("canVehicle") != None : 
              obj.canVehicle = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.roleID = request.form["roleID"]
        obj.update(obj)

    if operation == "Delete":
        roleID = request.form["roleID"]
        obj.delete(roleID)


    return redirect(url_for("Role_listing"))
                    
@app.route("/TransporterListing")
def Transporter_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canTransporter = process_role(6)

    if canTransporter == False:
        message = "You Don't Have Permission to Access Transporter"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = TransporterModel.get_all()

    return render_template("TransporterListing.html", records=records)

@app.route("/TransporterOperation")
def Transporter_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canTransporter = process_role(6)

    if not canTransporter:
        message = "You Don't Have Permission to Access Transporter"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = TransporterModel("", "")

    Transporter = TransporterModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = TransporterModel.get_by_id(unique_id)

    return render_template("TransporterOperation.html", row=row, operation=operation, Transporter=Transporter, )

@app.route("/ProcessTransporterOperation", methods=["POST"])
def process_Transporter_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canTransporter = process_role(6)
    if not canTransporter:
        message = "You Don't Have Permission to Access Transporter"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = TransporterModel("", "")

    if operation != "Delete":
       obj.transporterID = request.form['transporterID']
       obj.transporterName = request.form['transporterName']
       obj.contactNbr = request.form['contactNbr']
       obj.gstNumber = request.form['gstNumber']
       if len(request.files) != 0 :
        
                file = request.files['gstCertificateFile']
                if file.filename != '':
                    gstCertificateFile = file.filename
                    obj.gstCertificateFile = gstCertificateFile
                    f = os.path.join('static/UPLOADED_FILES', gstCertificateFile)
                    file.save(f)
                else:
                    obj.gstCertificateFile = request.form['hgstCertificateFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.transporterID = request.form["transporterID"]
        obj.update(obj)

    if operation == "Delete":
        transporterID = request.form["transporterID"]
        obj.delete(transporterID)


    return redirect(url_for("Transporter_listing"))
                    
@app.route("/UsersListing")
def Users_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(7)

    if canUsers == False:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = UsersModel.get_all()

    return render_template("UsersListing.html", records=records)

@app.route("/UsersOperation")
def Users_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(7)

    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = UsersModel("", "")

    Users = UsersModel.get_all()
    role_list = RoleModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = UsersModel.get_by_id(unique_id)

    return render_template("UsersOperation.html", row=row, operation=operation, Users=Users, role_list = role_list)

@app.route("/ProcessUsersOperation", methods=["POST"])
def process_Users_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canUsers = process_role(7)
    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = UsersModel("", "")

    if operation != "Delete":
       obj.userID = request.form['userID']
       obj.userName = request.form['userName']
       obj.emailid = request.form['emailid']
       obj.password = request.form['password']
       obj.contactNo = request.form['contactNo']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       obj.roleID = request.form['roleID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.userID = request.form["userID"]
        obj.update(obj)

    if operation == "Delete":
        userID = request.form["userID"]
        obj.delete(userID)


    return redirect(url_for("Users_listing"))
                    
@app.route("/VehicleListing")
def Vehicle_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canVehicle = process_role(8)

    if canVehicle == False:
        message = "You Don't Have Permission to Access Vehicle"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = VehicleModel.get_all()

    return render_template("VehicleListing.html", records=records)

@app.route("/VehicleOperation")
def Vehicle_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canVehicle = process_role(8)

    if not canVehicle:
        message = "You Don't Have Permission to Access Vehicle"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = VehicleModel("", "")

    Vehicle = VehicleModel.get_all()
    transporter_list = TransporterModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = VehicleModel.get_by_id(unique_id)

    return render_template("VehicleOperation.html", row=row, operation=operation, Vehicle=Vehicle, transporter_list = transporter_list)

@app.route("/ProcessVehicleOperation", methods=["POST"])
def process_Vehicle_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canVehicle = process_role(8)
    if not canVehicle:
        message = "You Don't Have Permission to Access Vehicle"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = VehicleModel("", "")

    if operation != "Delete":
       obj.vehicleID = request.form['vehicleID']
       obj.vehicleNbr = request.form['vehicleNbr']
       obj.transporterID = request.form['transporterID']
       if len(request.files) != 0 :
        
                file = request.files['registrationCertifiateFile']
                if file.filename != '':
                    registrationCertifiateFile = file.filename
                    obj.registrationCertifiateFile = registrationCertifiateFile
                    f = os.path.join('static/UPLOADED_FILES', registrationCertifiateFile)
                    file.save(f)
                else:
                    obj.registrationCertifiateFile = request.form['hregistrationCertifiateFile']
                
                file = request.files['insuranceFile']
                if file.filename != '':
                    insuranceFile = file.filename
                    obj.insuranceFile = insuranceFile
                    f = os.path.join('static/UPLOADED_FILES', insuranceFile)
                    file.save(f)
                else:
                    obj.insuranceFile = request.form['hinsuranceFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.vehicleID = request.form["vehicleID"]
        obj.update(obj)

    if operation == "Delete":
        vehicleID = request.form["vehicleID"]
        obj.delete(vehicleID)


    return redirect(url_for("Vehicle_listing"))
                    


import hashlib
import json


@app.route("/BlockChainGeneration")
def BlockChainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM ProductTracking WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    sqlcmd = "SELECT COUNT(*) FROM ProductTracking WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksNotCreated = dbrow[0]
    return render_template('BlockChainGeneration.html', blocksCreated=blocksCreated, blocksNotCreated=blocksNotCreated)


@app.route("/ProcessBlockchainGeneration", methods=['POST'])
def ProcessBlockchainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM ProductTracking WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    blocksCreated = 0
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    prevHash = ""
    if blocksCreated != 0:
        connx = pyodbc.connect(connString, autocommit=True)
        cursorx = connx.cursor()
        sqlcmdx = "SELECT * FROM ProductTracking WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
        cursorx.execute(sqlcmdx)
        dbrowx = cursorx.fetchone()
        if dbrowx:
            uniqueID = dbrowx[7]
            conny = pyodbc.connect(connString, autocommit=True)
            cursory = conny.cursor()
            sqlcmdy = "SELECT hash FROM ProductTracking WHERE sequenceNumber < '" + str(uniqueID) + "' ORDER BY sequenceNumber DESC"
            cursory.execute(sqlcmdy)
            dbrowy = cursory.fetchone()
            if dbrowy:
                prevHash = dbrowy[0]
            cursory.close()
            conny.close()
        cursorx.close()
        connx.close()
    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT * FROM ProductTracking WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
    cursor.execute(sqlcmd)

    while True:
        sqlcmd1 = ""
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        unqid = str(dbrow[7])

        bdata = str(dbrow[1]) + str(dbrow[2]) + str(dbrow[3]) + str(dbrow[4])
        block_serialized = json.dumps(bdata, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()

        conn1 = pyodbc.connect(connString, autocommit=True)
        cursor1 = conn1.cursor()
        sqlcmd1 = "UPDATE ProductTracking SET isBlockChainGenerated = 1, hash = '" + block_hash + "', prevHash = '" + prevHash + "' WHERE sequenceNumber = '" + unqid + "'"
        cursor1.execute(sqlcmd1)
        cursor1.close()
        conn1.close()
        prevHash = block_hash
    return render_template('BlockchainGenerationResult.html')


@app.route("/BlockChainReport")
def BlockChainReport():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()

    sqlcmd1 = "SELECT * FROM ProductTracking WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd1)
    conn2 = pyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM ProductTracking ORDER BY sequenceNumber DESC"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        row = ProductTrackingModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7])
        records.append(row)
    return render_template('BlockChainReport.html', records=records)         

            

 
if __name__ == "__main__":
    app.run()

                    