from email import message
from enum import auto
from pickle import FALSE
from pyexpat.errors import messages
from time import clock_getres
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

db = mclient['pokemon']

# Apach Ignite part
# create a attribute number map for storing the sequence of attributes. Key is the attribute name, value is No.
attributeNo = Iclient.get_or_create_cache("attributeNo")
# fill the attributeNo map.
attributeArray = ["id", "name-form", "type_1", "type_2", "data_species", "data_height", "data_weight", "first_ability", "second_ability", "hidden_ability" "training_catch_rate", "training_base_exp", "training_growth_rate", "breeding_gender_male",
                  "breeding_gender_male", "breeding_gender_female", "egg_group1", "egg_group2", "egg_cycle", "stats_hp", "stats_attack", "stats_defense", "stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total", "img"]
for i in range(len(attributeArray)):
    attributeNo.put(i, attributeArray[i])
# create a map for pokemon. Key is the id (without #) and the value is an array of attributes.
Ipokedex = Iclient.get_or_create_cache("Ipokedex")
INameAndId = Iclient.get_or_create_cache("INameAndId")

app.config['IMAGE_FOLDER'] = os.path.join('static', 'images')
app.config['CSS_FOLDER'] = os.path.join('static', 'styles')
app.config["SCRIPT_FOLDER"] = os.path.join('static', 'scripts')


@app.route('/favicon.ico', methods=["GET"])
def icon():
    return ''


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def indexPage():
    # fail = False
    elep = os.path.join(app.config['IMAGE_FOLDER'], 'elep.png')
    css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
    js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
    return render_template("index.html", logo=elep, style=css, script=js)


@app.route('/login', methods=["GET"])
def login():
    # data = json.loads(request.data.decode(utf-8"))
    username = request.args.get('username')
    password = request.args.get('password')
    print('username: ', username)
    print('password: ', password)
    # TODO: add authentication
    if username == "1":
        return redirect('/main')
    else:
        return "login failed"


@app.route('/main', methods=["GET"])
def mainPage():
    css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
    js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
    return render_template("main.html", style=css, script=js)

# detailPage return an array, in the sequence of ["id", "name", "type_1", "type_2", "link", "species", "height", "weight", "abilities", "training_catch_rate", "breeding_gender_male", "breeding_gender_male", "breeding_gender_female", "stats_hp", "stats_attack", "stats_defense", "stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total", "iamgeurl"]


@ app.route('/detail', methods=["GET", "POST"])
def detailPage():
    if (request.method == "GET"):
        id = request.args.get('id')
        output = Ipokedex.get(id)
        if (output != None):
            # print(output)
            css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
            js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
            return render_template("detail.html", style=css, script=js, pokemon=output)
    else:
        css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
        js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
        return render_template("detail.html", style=css, script=js)


@app.route('/getall', methods=["GET"])
def allPokemon():
    cursor = db.pokedex.find()
    re = {}
    for data in cursor:
        data.pop("_id")
        re[data['id']] = data
    return re

# insert part of data to mongodb and all the data to ignite


@app.route('/Insert/<id>/<name>', methods=["GET", "POST"])
@app.route('/insert', methods=["POST"])
def insertPokemon(id=0, name="-", type_1="-", type_2="-", species="-", height="0", weight="0", abilities="-", training_catch_rate="0", training_base_exp="0", training_growth_rate="0", breeding_gender_male="0", breeding_gender_female="0", stats_hp="0", stats_attack="0", stats_defense="0", stats_sp_atk="0", stats_sp_def="0", stats_speed="0", stats_total="0", img="-"):
    if request.method == "POST":
        data = request.data
        print(data)
        return data
    if request.method == "GET":
        # Ignite insert
        if Ipokedex.get(id) != None or len(list(db.pokedex.find({'id': id}))):
            print('already exists')
            return 'Insert failed, id already exists'
        else:
            INameAndId.put(name, id)
            Ipokedex.put(id, [name, type_1, type_2, species, height, weight, abilities, training_catch_rate, training_base_exp, training_growth_rate,
                              breeding_gender_male, breeding_gender_female, stats_hp, stats_attack, stats_defense, stats_sp_atk, stats_sp_def, stats_speed, stats_total, img])

            # Mongodb insert
            data = {
                'id': id,
                'name-form': name,
                'type_1': type_1,
                'type_2': type_2,
                'data_species': species,
                'img': img
            }
            db.pokedex.insert_one(data)
            cursor = db.pokedex.find({'name-form': name})
            x = {}
            for i in cursor:
                x.update(i)
            print(x)
            print(INameAndId.get(name))
            print(Ipokedex.get(id))
            return "insert succeed"
            # return json.loads(json_util.dumps(data))
    else:
        return ''

# search for the search page, use mongodb to search


@ app.route('/HomeSearch/<InfoType>/<info>', methods=["GET"])
# if the result is not found, it will return "No such result". If the result is found, it will return the result of the find_one function.
def Search(InfoType, info):
    if InfoType == "type":
        output = db.pokedex.find({"$or": [{"type_1": info}, {"type_2": info}]})
    else:
        output = db.pokedex.find({InfoType: info})
    if (output == None):
        return "No such result. Please search again"
    else:
        re = {}
        for data in output:
            data.pop("_id")
            re[data['id']] = data
        return re


# mongodb and ignite update


@ app.route('/Update/<id>/<name>/<type_1>', methods=["GET", "POST", "PATCH"])
def Update(id="-", name="-", type_1="-", type_2="-", link="-", species="-", height="0", weight="0", abilities="0", training_catch_rate="0", training_base_exp="0", training_growth_rate="0", breeding_gender_male="0", breeding_gender_female="0", stats_hp="0", stats_attack="0", stats_defense="0", stats_sp_atk="0", stats_sp_def="0", stats_speed="0", stats_total="0", img="-"):
    # Mongodb Update
    if (request.method == "GET"):
        if Ipokedex.get(id) == None or len(list(db.pokedex.find({'id': id}))) == 0:
            print("id not exists")
            return "id not exists"
        else:
            tmp = Ipokedex.get(id)[0]
            if INameAndId.get(tmp) == None:
                print("id not exists")
                return "id not exists"
            else:
                db.pokedex.update_one(
                    {"id": id},
                    {"$set": {"name-form": name,
                              "type_1": type_1,
                              "type_2": type_2,
                              "data_species": species,
                              "img": img}
                     }
                )
                # ignite update
                INameAndId.remove_key(tmp)
                Ipokedex.put(id, [name, type_1, type_2, link, species, height, weight, abilities, training_catch_rate, training_base_exp, training_growth_rate,
                                  breeding_gender_male, breeding_gender_female, stats_hp, stats_attack, stats_defense, stats_sp_atk, stats_sp_def, stats_speed, stats_total, img])
                INameAndId.put(name, id)
                print(INameAndId.get(name))
                cursor = db.pokedex.find({'id': id})
                x = {}
                for i in cursor:
                    x.update(i)
                print(x)
                print(Ipokedex.get(id))
                print(INameAndId.get(name))
                return "update succeed"


@ app.route('/Delete/<id>', methods=["DELETE"])
def Del(id=''):
    if request.method == "DELETE":
        print(Ipokedex.get(id))
        if (id == ""):
            return 'id can not be empty'
        else:
            if Ipokedex.get(id) == None or len(list(db.pokedex.find({'id': id}))) == 0:
                print("id not exists")
                return "id not exists"
            else:
                name = Ipokedex.get(id)[0]
                print(name)
                if INameAndId.get(name) == None:
                    print("id not exists")
                    return "id not exists"
                else:
                    # Ignite delete
                    Ipokedex.remove_key(id)
                    INameAndId.remove_key(name)
                    # # Mongodb delete
                    result = db.pokedex.delete_one({'id': id})
                    if (result.deleted_count >= 1 and Ipokedex.get(id) == None and INameAndId.get(name) == None):
                        print(id+' deleted')
                        return 'deletion succeed'
                    else:
                        return 'deletion failed'


if __name__ == "__main__":
    app.run(debug=True)
