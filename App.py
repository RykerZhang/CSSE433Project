from urllib import response
from pymongo import MongoClient
import pymongo
import json
from bson import json_util
from flask import Flask, render_template, request, redirect, url_for
import os

# import Router as router

app = Flask(__name__)
client = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = client['pokemon_test']


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


@app.route('/mInsert/<id>/<name>/<type_1>/<type_2>', methods=["GET", "POST"])
def insertPokemon(id=0, name=None, type_1=None, type_2=None, link=None, species=None, height=0, weight=0, abilities=None, training_catch_rate=0, training_base_exp=0, training_growth_rate=0, breeding_gender_male=0, breeding_gender_female=0, stats_hp=0, stats_attack=0, stats_defense=0, stats_sp_atk=0, stats_sp_def=0, stats_speed=0, stats_total=0):
    if request.method == "GET":
        data = {
            'id_nb': "#"+id,
            'name': name,
            'type_1': type_1,
            'type_2': type_2,
            'link': link,
            'species': species,
            'height': height,
            'weight': weight,
            'abilities': abilities,
            'training_catch_rate': training_catch_rate,
            'training_base_exp': training_base_exp,
            'training_growth_rate': training_growth_rate,
            'breeding_gender_male': breeding_gender_male,
            'breeding_gender_female': breeding_gender_female,
            'stats_hp': stats_hp,
            'stats_attack': stats_attack,
            'stats_defense': stats_defense,
            'stats_sp_atk': stats_sp_atk,
            'stats_sp_def': stats_sp_def,
            'stats_speed': stats_speed,
            'stats_total': stats_total
        }
        i = db.pokedex.find({'id_nb': "#"+id})
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


@app.route('/mDelete/<name>', methods=["DELETE"])
def mDel(name='a'):
    if request.method == "DELETE":
        if (name == None):
            return 'name can not be null'
        else:
            result = db.pokedex.delete_many({'name': name})
            if (result.deleted_count >= 1):
                print(name+' deleted')
                return 'deletion succeed'
            else:
                return 'deletion failed'


if __name__ == "__main__":
    app.run()
