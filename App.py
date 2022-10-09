from flask import Flask, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")




@app.route('/login', methods = ["GET", "POST"])
def loginPage():
    if(request.methods == "GET"):
        LoginUsername = request.form.get('LoginUsername')
        LoginPassword = request.form.get('LoginPassword')
        NewUsername = request.form.get('NewUsername')
        NewPassword = request.form.get('NewPassword')
        print("LoginUsername is " , LoginUsername)
        print("LoginPassword is " , LoginPassword)
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/', methods = ["GET", "POST"])
def home():
    return 'Welcome to the Home Page'
app.run()

