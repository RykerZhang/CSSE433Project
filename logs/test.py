import socket
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pymongo import MongoClient
from pyignite import Client
from neo4j import GraphDatabase


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
    if (mongo):
        Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
        db = Mclient['test']
        with open('mongo.log') as f:
            lines = f.readlines()
            for command in lines:
                exec(command)
                # TODO: add code to remove command from mongo.log


# monitor_host()
# # print(isOpen("433-34.csse.rose-hulman.edu", 10800))
if __name__ == '__main__':
    watch = OnMyWatch()
    monitor = threading.Thread(target=monitor_host, args=())
    monitor.start()
    watch.run()
