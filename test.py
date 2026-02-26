from flask import *

# initialize flask
app=Flask(__name__)

#create a route/end point
@app.route("/api/home")
def home():
    return jsonify({"Message":"Welcome to Home api"})

#create a route for products
@app.route("/api/product")
def product():
    return jsonify({"Message":"Welcome to products api"})

#create a practice route
@app.route("/api/services")
def services():
    return jsonify({"Message":"Welcome to our services api"})

#post method
@app.route("/api/calc",methods=["POST"])
def calc():
    #request user input
    num1=request.form["num1"]
    num2=request.form["num2"]

    sum=int(num1)+int(num2)
    return jsonify({"Answer":sum})

#multiplication
@app.route("/api/mult",methods=["POST"])
def mult():
    num1=request.form["num1"]
    num2=request.form["num2"]

    mult=int(num1)*int(num2)

    return jsonify({"Answer":mult})

@app.route("/api/message")
def message():
    return jsonify({"Message":"Welcome to MODCOM"})

@app.route("/api/rain")
def rain():
    return jsonify({"Message":"Its raining"})













app.run(debug=True)