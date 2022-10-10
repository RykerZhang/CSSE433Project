from urllib import response
from pymongo import MongoClient
import pymongo
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
client = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")

IMAGE_FOLDER = os.path.join('static', 'images')
CSS_FOLDER = os.path.join('static', 'styles')
SCRIPT_FOLDER = os.path.join('static', 'scripts')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['CSS_FOLDER'] = CSS_FOLDER
app.config["SCRIPT_FOLDER"] = SCRIPT_FOLDER


@app.route('/login', methods=["GET", "POST"])
def loginPage():
    if (request.methods == "GET"):
        LoginUsername = request.form.get('LoginUsername')
        LoginPassword = request.form.get('LoginPassword')
        NewUsername = request.form.get('NewUsername')
        NewPassword = request.form.get('NewPassword')
        print("LoginUsername is ", LoginUsername)
        print("LoginPassword is ", LoginPassword)
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def indexPage():
    elep = os.path.join(app.config['IMAGE_FOLDER'], 'elep.png')
    css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
    js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
    return render_template("index.html", logo=elep, style=css, script=js)


@app.route('/main', methods=["GET", "POST"])
def mainPage():
    elep = os.path.join(app.config['IMAGE_FOLDER'], 'elep.png')
    css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
    js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
    return render_template("main.html", logo=elep, style=css, script=js)

# It's implemented by default


@app.route('/favicon.ico', methods=["GET"])
def icon():
    return ''

    # @app.route('/', methods=["GET", "POST"])
    # def home():
    #     return 'Welcome o the Home Page'
if __name__ == "__main__":
    app.run()
