from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")


@app.route('/')
def home():
    return 'Welcome to the Home Page'


@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
