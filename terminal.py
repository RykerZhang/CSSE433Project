from pymongo import MongoClient
from pyignite import Client
import pymongo
import json
import os

#Mongo
Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = Mclient['pokemon']

#Ignite
Iclient = Client()
Iclient.connect('433-34.csse.rose-hulman.edu', 10800)

#Neo4J
Nclient = GraphDatabase.driver('bolt://433-34.csse.rose-hulman.edu:7687', auth=('neo4j', 'neo4j'))

attributeNo = Iclient.get_or_create_cache("attributeNo")

attributeArray = ["id", "name-from", "type_1", "type_2", "species", "height", "weight", "abilities", 
"training_catch_rate", "training_base_exp", "training_growth_rate",
"breeding_gender_male", "breeding_gender_female", "stats_hp", "stats_attack", "stats_defense", 
"stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total", "img"]

for i in range(len(attributeArray)):
    attributeNo.put(i, attributeArray[i])

Ipokedex = Iclient.get_or_create_cache("Ipokedex")
INameAndId = Iclient.get_or_create_cache("INameAndId")

def insertPokemon(id=0, name="-", type_1="-", type_2="-", species="-", height="0", weight="0", abilities="-", 
training_catch_rate="0", training_base_exp="0", training_growth_rate="0", breeding_gender_male="0", 
breeding_gender_female="0", stats_hp="0", stats_attack="0", stats_defense="0", stats_sp_atk="0", 
stats_sp_def="0", stats_speed="0", stats_total="0", img="-"):
    if Ipokedex.get(id) != None or len(list(db.pokedex.find({'id': id}))):
            print('already exists')
            return 'Insert failed, id already exists'
    else:
            INameAndId.put(name, id)
            Ipokedex.put(id, [name, type_1, type_2, species, height, weight, abilities, 
            training_catch_rate, training_base_exp, training_growth_rate, 
            breeding_gender_male, breeding_gender_female, stats_hp, stats_attack, 
            stats_defense, stats_sp_atk, stats_sp_def, stats_speed, stats_total, img])
    
    data = {
                'id': id,
                'name-form': name,
                'type_1': type_1,
                'type_2': type_2,
                'data_species': species,
                'img': img
            }
    
    db.pokedex.insert_one(data)


def Search(InfoType, info):
    if InfoType == "type":
        output = db.pokedex.find({"$or": [{"type_1": info}, {"type_2": info}]})