from flask import *

import pymysql
import os

#initialize the app
app=Flask(__name__)
#create a folder
if not os.path.exists("static/images"):
    os.makedirs("static/images")
app.config["UPLOAD_FOLDER"]="static/images"

@app.route("/api/signup",methods=["POST"])
def signup():
    #request user inputs
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]
    phone=request.form["phone"]

    #create a connection to mysql
    connection=pymysql.connect(host="localhost",user="root",password="",database="paa_sokogarden_elias")

    #create a cursor
    cursor=connection.cursor()

    #SQL statement to insert the users
    sql="insert into users(username,email,password,phone)values(%s,%s,%s,%s)"

    #prepare data
    data=(username,email,password,phone)

    #execute/run
    cursor.execute(sql,data)

    #commit/save
    connection.commit()

    #return a response
    return jsonify({"Message":"Thank you for joining"})

#create sign in  api
#create the route
@app.route("/api/signin",methods=["POST"])
def signin():
    #request user input
    email=request.form["email"]
    password=request.form["password"]

    #create connection
    connection=pymysql.connect(host="localhost",user="root", password="",database="paa_sokogarden_elias")

    #create cursor
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    #sql statement to select
    sql="select * from users where email=%s and password=%s"

    #prepare data
    data=(email,password)

    #execute/run
    cursor.execute(sql,data)

    #response
    if cursor.rowcount==0:
        return jsonify({"Message":"Login failed"})
    else:
        user=cursor.fetchone()
        user.pop("password",None)
        return jsonify({"Message":"Login success","user":user})
    

#add product route
@app.route("/api/add_product", methods=["POST"])
def add_product():
    #request user input
    product_name=request.form["product_name"]
    product_description=request.form["product_description"]
    product_cost=request.form["product_cost"]
    product_photo=request.files["product_photo"]

    #extract filename
    filename=product_photo.filename
    photo_path=os.path.join(app.config["UPLOAD_FOLDER"],filename)
    product_photo.save(photo_path)

   #connect to database
    connection=pymysql.connect(host="localhost",user="root",password="",database="paa_sokogarden_elias")

    #create cursor
    cursor=connection.cursor()

    #sql statement
    sql="insert into products_details(product_name,product_description,product_cost,product_photo)values(%s,%s,%s,%s)"

    #prepare data
    data=(product_name,product_description,product_cost,filename)

    #execute/run
    cursor.execute(sql,data)

    #commit/save
    connection.commit()

    #response
    return jsonify({"Message":"Product details are added succesfuly"})


#get product API
#get product route/endpoint
@app.route("/api/get_product")
def get_product():

    #create connecion to mysql database
    connection=pymysql.connect(host="localhost",user="root",password="",database="paa_sokogarden_elias")
     
    #create cursor
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    #sql statement to retrieve data from mysql database
    sql="select * from products_details"

    #execute/run
    cursor.execute(sql)

    #fetch the data from mysql database to flask
    product=cursor.fetchall()

    #response
    return jsonify(product)

# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})





































#run the app
app.run(debug=True)