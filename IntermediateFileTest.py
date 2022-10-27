import socket
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pymongo import MongoClient
from pyignite import Client
from neo4j import GraphDatabase
import json
import os


#generate a json file using dictionaries
def write_to_log(type, fields, fields2):
    timestamp = time.time()
    tp = timestamp
    data_dict = {}
    if fields2 is None:
        data_dict = {"type": type, "fields": fields, "timestamp": timestamp}
    if fields2 is not None:
        data_dict = {"type": type, "fields": fields, "fields2": fields2, "timestamp": timestamp}
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
        db.delete_one(fields)
        return "db.delete_one(" + str(fields) + ")"


# testing purposes: generate some data when the mongodb server is down
def gen_commands():
    data1 = {'id': 9990, 'name-form': "New", 'type_1': "Grass", 'type_2': "Bug", 'data_species': "New Pokemon", 'img': ""}
    write_to_log("insert", data1, None)
    data2 = {'id': 9980, 'name-form': "New2", 'type_1': "Fire", 'type_2': "-", 'data_species': "New Pokemon2", 'img': ""}
    write_to_log("insert", data2, None)
    data3 = {'id': 9980}
    data4 = {'id': 9960, 'name-form': "New3", 'type_1': "Fire", 'type_2': "Poison", 'data_species': "New Pokemon3", 'img': ""}
    write_to_log("update", data3, data4)
    data5 = {'id': 9990}
    write_to_log("delete", data3, None)


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
            print(event.src_path.split("/")
                  [-2]+"/"+event.src_path.split("/")[-1])


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
        p += "ignite is down"
    print(p)
    # change first parameter to allow longer period
    threading.Timer(20, monitor_host).start()
    # TODO: add function to read and manipulate logs
    # testing purposes: generate some data when the mongodb server is down
    if (not mongo):
        gen_commands()
    if (mongo):
        Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
        db = Mclient['test']
        testCol = db['test']
        path_list = os.listdir('log/')
        #path_list.remove('.DS_Store')
        #sort to ensure that all json files are read by time order
        path_list.sort()
        #read all files in the folder
        for dir in path_list:
            #print(dir)
            with open('log/' + dir) as file:
                tp, fields, fields2, timestamp = read_log(dir)
                cmd = parse_command(testCol,tp,fields,fields2)
                #print(cmd)
                #exec(cmd)
                os.remove('log/' + dir)
                res = testCol.find({})
                #testing purposes: print out the data in the database
                print("New Data after restoring a log:")
                for r in res:
                    print(r)
        # with open('mongo.log') as f:
        #     lines = f.readlines()
        #     for command in lines:
        #         exec(command)
                # TODO: add code to remove command from mongo.log


# monitor_host()
# # print(isOpen("433-34.csse.rose-hulman.edu", 10800))
if __name__ == '__main__':
    watch = OnMyWatch()
    monitor = threading.Thread(target=monitor_host, args=())
    monitor.start()
    watch.run()
