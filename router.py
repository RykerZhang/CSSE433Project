from pymongo import MongoClient
from pyignite import Client
from neo4j import GraphDatabase

# MClient is for mongodb
Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = Mclient['pokemon']

# Iclient is for Ignite.
Iclient = Client()
Iclient.connect('433-34.csse.rose-hulman.edu', 10800)

# Nclient is for neo4j
Nclient = GraphDatabase.driver(
    'bolt://433-34.csse.rose-hulman.edu:7687', auth=('neo4j', 'neo4j'))
