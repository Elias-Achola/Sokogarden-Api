from flask import *

import pymysql

#initialize the app
app=Flask(__name__)

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







































#run the app
app.run(debug=True)