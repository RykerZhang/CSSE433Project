from tabnanny import check
from urllib import response
from pymongo import MongoClient
from pyignite import Client
import pymongo
import json
from bson import json_util
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo

import os

# import Router as router

app = Flask(__name__)
# MClient is for mongodb
mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
# Iclient is for neo4j.
Iclient = Client()
Iclient.connect('433-34.csse.rose-hulman.edu', 10800)

db = mclient['pokemon_test']

# Apach Ignite part
# create a attribute number map for storing the sequence of attributes. Key is the attribute name, value is No.
attributeNo = Iclient.get_or_create_cache("attributeNo")
# fill the attributeNo map.
attributeArray = ["id", "name", "type_1", "type_2", "link", "species", "height", "weight", "abilities", "training_catch_rate", "breeding_gender_male",
                  "breeding_gender_male", "breeding_gender_female", "stats_hp", "stats_attack", "stats_defense", "stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total", "imageurl"]
for i in range(len(attributeArray)):
    attributeNo.put(i, attributeArray[i])
# create a map for pokemon. Key is the id (without #) and the value is an array of attributes.
Ipokedex = Iclient.get_or_create_cache("Ipokedex")

app.config['IMAGE_FOLDER'] = os.path.join('static', 'images')
app.config['CSS_FOLDER'] = os.path.join('static', 'styles')
app.config["SCRIPT_FOLDER"] = os.path.join('static', 'scripts')

@app.route('/favicon.ico', methods=["GET"])
def icon():
    return ''


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def indexPage():
    elep = os.path.join(app.config['IMAGE_FOLDER'], 'elep.png')
    css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
    js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
    return render_template("index.html", logo=elep, style=css, script=js)


@app.route('/main', methods=["GET"])
def mainPage():
    elep = os.path.join(app.config['IMAGE_FOLDER'], 'elep.png')
    css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
    js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
    return render_template("main.html", logo=elep, style=css, script=js)


# insert part of data to mongodb and all the data to ignite
@app.route('/Insert/<id>/<name>/<type_1>/<type_2>', methods=["GET", "POST"])
def insertPokemon(id=0, name=None, type_1=None, type_2=None, link=None, species=None, height=0, weight=0, abilities=None, training_catch_rate=0, training_base_exp=0, training_growth_rate=0, breeding_gender_male=0, breeding_gender_female=0, stats_hp=0, stats_attack=0, stats_defense=0, stats_sp_atk=0, stats_sp_def=0, stats_speed=0, stats_total=0, imageurl=""):
    if request.method == "GET":
        #Ignite insert
        checkoutput = Ipokedex.get(id)
        if (checkoutput != None):
            return "id already exist."
        Ipokedex.put(id, [name, type_1, type_2, link, species, height, weight, abilities, training_catch_rate, training_base_exp, training_growth_rate, breeding_gender_male, breeding_gender_female, stats_hp, stats_attack, stats_defense, stats_sp_atk, stats_sp_def, stats_speed, stats_total, imageurl])
        #Mongodb insert
        data = {
            'id': id,
            'name': name,
            'type_1': type_1,
            'species': species,
            'imageurl': imageurl
        }
        i = db.pokedex.find({'id': id})
        n = db.pokedex.find({'name': name})
        if len(list(n)) > 0 or len(list(i)):
            print('already exists')
            return 'Insert failed, name already exists'
        db.pokedex.insert_one(data)
        cursor = db.pokedex.find({'name': name})
        x = {}
        for i in cursor:
            x.update(i)
        print(x)
        return json.loads(json_util.dumps(data))
    else:
        return ''

#search for the search page, use mongodb to search
@app.route('/HomeSearch/<InfoType>/<info>', methods = ["GET"])
# if the result is not found, it will return "No such result". If the result is found, it will return the result of the find_one function.
def Search(InfoType, info):
    output = db.pokedex.find({InfoType: info})
    if (output == None):
        return "No such result. Please search again"
    else:
        pokeDict = dict()
        for i in output:
            id = i.get("id")
            name = i.get("name")
            type_1 = i.get("type_1")
            species = i.get("species")
            imageurl = i.get("imageurl")
            pokeDict[i] = [id, name, type_1, species, imageurl]
        return pokeDict
 
# detailPage return an array, in the sequence of ["id", "name", "type_1", "type_2", "link", "species", "height", "weight", "abilities", "training_catch_rate", "breeding_gender_male", "breeding_gender_male", "breeding_gender_female", "stats_hp", "stats_attack", "stats_defense", "stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total", "iamgeurl"]
@app.route('/DetailSearch/<id>/<name>', methods = ["GET"])
def detailPage(id):
        if(request.method == "GET"):
            output = Ipokedex.get(id)
            return output

# mongodb and ignite update


@app.route('/Update', methods=["GET", "POST"])
def Update(id=0, name=None, type_1=None, type_2=None, link=None, species=None, height=0, weight=0, abilities=None, training_catch_rate=0, training_base_exp=0, training_growth_rate=0, breeding_gender_male=0, breeding_gender_female=0, stats_hp=0, stats_attack=0, stats_defense=0, stats_sp_atk=0, stats_sp_def=0, stats_speed=0, stats_total=0, imageurl=""):
    # Mongodb Update
    if (request.method == "POST"):
        db.Book.update_one(
            {"id": id},
            {"$set": {"name": name,
                      "type_1": type_1,
                      "species": species,
                      "imageurl": imageurl}
             }
        )
        n = db.pokedex.find({'name': name})
        if len(list(n) > 0):
            print('already exists')
            return 'Insert failed, name already exists'
    #ignite update
        checkoutput = Ipokedex.get(id)
        if(checkoutput!=None):
            Ipokedex.remove_key(id)
            Ipokedex.put(id, [name, type_1, type_2, link, species, height, weight, abilities, training_catch_rate, training_base_exp, training_growth_rate, breeding_gender_male, breeding_gender_female, stats_hp, stats_attack, stats_defense, stats_sp_atk, stats_sp_def, stats_speed, stats_total, imageurl])
        else:
            return "No such Id"
        

@app.route('/Delete/<name>', methods=["DELETE"])
def Del(name='a'):
    if request.method == "DELETE":
        if (name == None):
            return 'name can not be null'
        else:
            # Ignite delete
            checkoutput = Ipokedex.get(id)
            if (checkoutput != None):
                Ipokedex.remove_key(id)
            # Mongodb delete
            result = db.pokedex.delete_many({'name': name})
            if (result.deleted_count >= 1):
                print(name+' deleted')
                return 'deletion succeed'
            else:
                return 'deletion failed'

if __name__ == "__main__":
    app.run()
