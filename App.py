from email import message
from enum import auto
from pickle import FALSE
from pyexpat.errors import messages
from re import I
#from time import clock_getres
from pymongo import MongoClient
from pyignite import Client
from neo4j import GraphDatabase
import pymongo
import json
from bson import json_util
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
import os
import socket
import time
import threading
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

igniteDown = False

# MClient is for mongodb
Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = Mclient['pokemon']

# Iclient is for Ignite.
Iclient = Client()
Iclient.connect('433-34.csse.rose-hulman.edu', 10800)

# Nclient is for neo4j
driver = GraphDatabase.driver(
    'bolt://433-34.csse.rose-hulman.edu:7687', auth=('neo4j', 'neo4j'))
Nclient = driver.session()
# with Nclient.session() as session:
#     session.execute_write(
#         function, param1,param2,...)


# Apach Ignite part
# create a attribute number map for storing the sequence of attributes. Key is the attribute name, value is No.
attributeNo = Iclient.get_or_create_cache("attributeNo")
# fill the attributeNo map.
attributeArray = ["id", "name-from", "type_1", "type_2", "species", "height", "weight", "abilities", "training_catch_rate", "training_base_exp", "training_growth_rate",
                  "breeding_gender_male", "breeding_gender_female", "stats_hp", "stats_attack", "stats_defense", "stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total", "img"]
for i in range(len(attributeArray)):
    attributeNo.put(i, attributeArray[i])
# create a map for pokemon. Key is the id (without #) and the value is an array of attributes.
Ipokedex = Iclient.get_or_create_cache("Ipokedex")

# intermediate files pre setting
# generate a json file using dictionaries

# create node when pokemon added


def createNode(name, id, img):
    # check if the node exist:
    oldResult = Nclient.run("MATCH (p:Pokemon { id : $id }) "
                            "return p.id", id=id)
    for e in oldResult:
        if (e["p.id"] != None):
            print(oldResult)
            print("This node already exist")
            return "This node already exist"
    result = Nclient.run("CREATE (p:Pokemon { name: $name , id : $id, img : $img }) "
                         "RETURN p", name=name, id=id, img=img)
    print(result)
    return "Node created!"

# delete node when pokemon is deleted.


def deleteNode(id):
    result = Nclient.run("MATCH (p:Pokemon {id : $id}) "
                         "DETACH DELETE p", id=id)
    print(result)
    return "delete success"


def write_to_log_Ignite(type, key, value):
    timestamp = time.time()
    tp = timestamp
    data_dict = {}
    print("test")
    data_dict = {"type": type, "key": key,
                 "value": value, "timestamp": timestamp}
    with open("IgniteLog/" + str(timestamp) + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
    return timestamp


def read_log_Ignite(file_name):
    f = open("IgniteLog/" + str(file_name), 'r', encoding='utf-8')
    data = json.load(f)
    tp = data['type']
    key = data['key']
    value = data['value']
    timestamp = data['timestamp']
    # print(tp)
    # print(fields)
    # print(timestamp)
    return tp, key, value, timestamp


def parse_command_Ignite(tp, key, value):
    if tp == "insert_Ipokedex":
        db = Ipokedex
        db.put(key, value)
        return "db.put(" + key + ","+str(value) + ")"
    if tp == "update_Ipokedex":
        db = Ipokedex
        db.put(key, value)
        return "ipokedex update"
    if tp == "delete_Ipokedex":
        db = Ipokedex
        db.remove_key(key)
        return "ipokedex remove"


def write_to_log(type, fields, fields2):
    timestamp = time.time()
    tp = timestamp
    data_dict = {}
    print("test")
    if fields2 is None:
        data_dict = {"type": type, "fields": fields, "timestamp": timestamp}
    if fields2 is not None:
        data_dict = {"type": type, "fields": fields,
                     "fields2": fields2, "timestamp": timestamp}
    with open("log/" + str(timestamp) + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
    return timestamp


# read a json log file
def read_log(file_name):
    f = open("log/" + str(file_name), 'r', encoding='utf-8')
    data = json.load(f)
    tp = data['type']
    fields = data['fields']
    timestamp = data['timestamp']
    # print(tp)
    # print(fields)
    # print(timestamp)
    if tp == "update":
        fields2 = data['fields2']
    else:
        fields2 = None
    return tp, fields, fields2, timestamp


# generate a command based on the fields
def parse_command(db, tp, fields, fields2):
    if tp == "insert":
        db.insert_one(fields)
        return "db.insert_one(" + str(fields) + ")"
    if tp == "update":
        db.update_one(fields, {'$set': fields2})
        return "db.update_one(" + str(fields) + "," + "{'$set':" + str(fields2) + "})"
    if tp == "delete":
        # check validation
        # if len(list(db.find({'id': id}))) == 0:
        #print("id not exists")
        # return "id not exists"
        # else:
        db.delete_one(fields)
        return "db.delete_one(" + str(fields) + ")"


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "."

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            # print("Watchdog received modified event - % s." % event.src_path)
            # print(event.src_path.split("/")
            # [-2]+"/"+event.src_path.split("/")[-1])
            print(" ")


def importToIgnite():
    client = Client()
    client.connect('433-34.csse.rose-hulman.edu', 10800)
    Ipokedex = client.get_or_create_cache("Ipokedex")

    db = pd.read_csv('./Init/ignite.csv')
    for tmp in db.iterrows():
        data = list(list(tmp)[1])
        id = str(data[0])
        for k in range(len(data)):
            data[k] = str(data[k])
            # print(type(data[k]))
        Ipokedex.put(id, data)


def pushToIgnite():
    ignite = isOpen("433-34.csse.rose-hulman.edu", 10800)
    global igniteDown
    if igniteDown and ignite:
        importToIgnite()
        # global igniteDown
        igniteDown = False
    if ignite:
        Iclient = Client()
        Iclient.connect('433-34.csse.rose-hulman.edu', 10800)

        Ipokedex = Iclient.get_or_create_cache("Ipokedex")

        path_list = os.listdir('IgniteLog/')
        path_list.sort()
        # read all files in the folder
        for dir in path_list:
            with open('IgniteLog/' + dir) as file:
                tp, key, value, timestamp = read_log_Ignite(dir)
                #parse_command_Ignite(tp, key, value)
                # parse_command_Ignite(tp, key, value):
                if tp == "insert_Ipokedex":
                    db = Ipokedex
                    db.put(key, value)
                    # return "db.put(" + key + ","+str(value) + ")"
                if tp == "update_Ipokedex":
                    db = Ipokedex
                    db.put(key, value)
                    # return "ipokedex update"
                if tp == "delete_Ipokedex":
                    db = Ipokedex
                    db.remove_key(key)
                    # return "ipokedex remove"

                # os.remove('IgniteLog/' + dir)


def pushToMongo():
    mongo = isOpen("433-34.csse.rose-hulman.edu", 27017)
    if mongo:
        Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
        db = Mclient['pokemon']
        testCol = db['pokedex']

        path_list = os.listdir('log/')
        path_list.sort()

        # read all files in the folder
        for dir in path_list:
            with open('log/' + dir) as file:
                tp, fields, fields2, timestamp = read_log(dir)
                cmd = parse_command(testCol, tp, fields, fields2)
                # print(cmd)
                # exec(cmd)
                os.remove('log/' + dir)
                #res = testCol.find({})
                # testing purposes: print out the data in the database
                print("New Data after restoring a log:")
                # for r in res:
                #     print(r)


def monitor_host():
    mongo = isOpen("433-34.csse.rose-hulman.edu", 27017)
    ignite = isOpen("433-34.csse.rose-hulman.edu", 10800)
    neo = isOpen("433-34.csse.rose-hulman.edu", 7474)
    p = ""
    if neo:
        p += "neo4j is running | "
    else:
        p += "neo4j is down | "
    if mongo:
        p += "mongo is running | "
    else:
        p += "mongo is down | "
    if ignite:
        p += "ignite is running"
    else:
        global igniteDown
        igniteDown = True
        p += "ignite is down"
    print(p)
    pushToIgnite()
    pushToMongo()

    # change first parameter to allow longer period
    threading.Timer(10, monitor_host).start()


app.config['IMAGE_FOLDER'] = os.path.join('static', 'images')
app.config['CSS_FOLDER'] = os.path.join('static', 'styles')
app.config["SCRIPT_FOLDER"] = os.path.join('static', 'scripts')


@app.route('/favicon.ico', methods=["GET"])
def icon():
    return ''


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
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
            css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
            js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
            return render_template("detail.html", style=css, script=js, pokemon=output)
        else:
            return redirect('/main')
    else:
        css = os.path.join(app.config['CSS_FOLDER'], 'main.css')
        js = os.path.join(app.config["SCRIPT_FOLDER"], 'main.js')
        return render_template("detail.html", style=css, script=js)


@app.route('/getall', methods=["GET"])
def allPokemon():
    if not isOpen("433-34.csse.rose-hulman.edu", 27017):
        print("down")
        return {"message": "down"}
    cursor = db.pokedex.find()
    re = {}
    for data in cursor:
        data.pop("_id")
        re[data['id']] = data
    # print(re)
    return re

# insert part of data to mongodb and all the data to ignite


@app.route('/insert', methods=["POST"])
def insertPokemon():
    if request.method == "POST":
        p = request.json
        # ignite insert
        tmp = [None]*21
        for t in range(len(p)):
            tmp[t] = str(p[t])
        print(tmp)

        #Ipokedex.put(p[0], tmp)
        write_to_log_Ignite("insert_Ipokedex", p[0], tmp)

        # neo4j add node
        createNode(p[1], p[0], p[20])

        data = {
            'id': p[0],
            'name-form': p[1],
            'type_1': p[2],
            'type_2': p[3],
            'data_species': p[4],
            'img': p[20]
        }
        print("write!!!\n")
        write_to_log("insert", data, None)
        # db.pokedex.insert_one(data)
        # log = "db.pokedex.insert_one("+str(data)+")"
        pushToIgnite()
        pushToMongo()
        return "insertion added to logs"

# search for the search page, use mongodb to search


@app.route('/HomeSearch/<InfoType>/<info>', methods=["GET"])
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


@app.route('/Update', methods=["POST"])
def Update():
    if (request.method == "POST"):
        p = request.json
        id = p[0]
       # print(Ipokedex.get(id))
       # print(len(list(db.pokedex.find({'id': id}))))
       # print(Ipokedex.get(id)[1])
       # if Ipokedex.get(id) == None or len(list(db.pokedex.find({'id': id}))) == 0:
        #    print("id not exists")
       #     return "id not exists"
       # else:
        #tmp = Ipokedex.get(id)[1]
        pokemon = [None]*21
        for t in range(len(p)):
            pokemon[t] = str(p[t])
        print(pokemon)
        #tmp = Ipokedex.get(id)[1]

        data1 = {"name-form": pokemon[1],
                 "type_1": pokemon[2],
                 "type_2": pokemon[3],
                 "data_species": pokemon[4],
                 "img": pokemon[20]}

        db.pokedex.update_one(
            {"id": pokemon[0]},
            {"$set": {"name-form": pokemon[1],
                      "type_1": pokemon[2],
                      "type_2": pokemon[3],
                      "data_species": pokemon[4],
                      "img": pokemon[20]}
             }
        )
        write_to_log("update", {"id": pokemon[0]}, data1)
        # ignite update
        write_to_log_Ignite("update_Ipokedex", pokemon[0], pokemon)
        #Ipokedex.put(pokemon[0], pokemon)
        # print(Ipokedex.get(pokemon[0]))
        pushToIgnite()
        pushToMongo()
        return "update succeed"


@ app.route('/Delete/<id>', methods=["DELETE"])
def Del(id=''):
    if request.method == "DELETE":
        # print(Ipokedex.get(id))
        if (id == ""):
            return 'id can not be empty'
        else:
            # if Ipokedex.get(id) == None:
            #     print("id not exists")
            #     # return "id not exists"
            # else:
            # name = Ipokedex.get(id)[1]
            # print(name)
            write_to_log_Ignite("delete_Ipokedex", id, None)
            # delete node
            deleteNode(id)
            print(id)
            # print(name)
            # if (not ismongo):
            # write to json, create fields
            write_to_log("delete", {"id": id}, None)
            print("write!!!\n")
            pushToIgnite()
            pushToMongo()
            # else:
            # print("aaaaa\n")
            # db.pokedex.delete_one({"id":id})


# neo4j detail page next evo check


@app.route('/detail/NEXTEVO/<id>', methods=["GET"])
def getNextEvo(id):
    # get name
    id = int(id)
    evo = Nclient.run(
        "MATCH ((n)-[r]->(m)) WHERE n.id = $id return m,r", id=id)
    evoNameArray = []
    evoImgArray = []
    evoIdArray = []
    methodArray = []

    for e in evo:
        evoIdArray.append(e[0]["id"])
        evoNameArray.append(e[0]['name'])
        evoImgArray.append(e[0]["img"])
        methodArray.append(e[1]['method'])
    dict = {}
    dict["name"] = evoNameArray
    dict["id"] = evoIdArray
    dict["img"] = evoImgArray
    dict['method'] = methodArray
    print(dict)
    return dict

# get previous Evo


@app.route('/detail/PREVEVO/<id>', methods=["GET"])
def getPrevEvo(id):
    id = int(id)
    evo = Nclient.run("MATCH ((n)-[r]->(m)) "
                      "WHERE m.id = $id "
                      "return n,r", id=id)
    evoNameArray = []
    evoIdArray = []
    evoImgArray = []
    methodArray = []
    for e in evo:
        evoIdArray.append(e[0]["id"])
        evoNameArray.append(e[0]['name'])
        evoImgArray.append(e[0]["img"])
        methodArray.append(e[1]['method'])
    dict = {}
    dict["name"] = evoNameArray
    dict["id"] = evoIdArray
    dict["img"] = evoImgArray
    dict['method'] = methodArray
    print(dict)
    return dict

# Function haven't been routed yet: (neo4j create node , relation and delete node with repetition check )


@app.route('/EVO/CREATE/<lowId>/<highId>/<way>', methods=["POST"])
def addEVO(lowId, highId, way):
    lowId = int(lowId)
    highId = int(highId)
    # check if the relationship exist:
    oldResult = Nclient.run("MATCH (low:Pokemon { id : $lowId }) "
                            "MATCH (high:Pokemon {id : $highId }) "
                            "WHERE (low)-[]->(high) "
                            "RETURN low", lowId=lowId, highId=highId)
    for e in oldResult:
        if (e[0] != None):
            print("Relation already exists")
            return "Relation already exists"
    result = Nclient.run("MATCH (low:Pokemon { id : $lowId }) "
                         "MATCH (high:Pokemon {id : $highId }) "
                         "CREATE (low)-[r:evolution]->(high) "
                         "set r.method = $way "
                         "return count(r)", lowId=lowId, highId=highId, way=way)
    for e in result:
        print(e[0])
    print(result)
    print("Relation created")
    return "Relation created"


@app.route('/EVO/DELETE/<lowId>/<highId>', methods=["POST"])
def delEvo(lowId, highId):
    lowId = int(lowId)
    highId = int(highId)
    # check if the relationship exist:
    oldResult = Nclient.run("MATCH (low:Pokemon { id : $lowId }) "
                            "MATCH (high:Pokemon {id : $highId }) "
                            "WHERE (low)-[]->(high) "
                            "RETURN count(low)", lowId=lowId, highId=highId)
    for e in oldResult:
        if (e[0] == 0):
            print("Relation doesn't exists")
            return "Relation doesn't exists"
    result = Nclient.run("MATCH (low:Pokemon { id : $lowId }) "
                         "MATCH (high:Pokemon {id : $highId }) "
                         "MATCH (low)-[r:evolution]->(high) "
                         "DELETE r "
                         "return count(r)", lowId=lowId, highId=highId)
    print(result)
    print("Relation deleted")
    return "Relation deleted"


if __name__ == "__main__":
    # watch = OnMyWatch()
    monitor = threading.Thread(target=monitor_host, args=())
    # watch1 = threading.Thread(target=watch.run, args=())
    monitor.start()
    # watch1.start()
    app.run(debug=True)
