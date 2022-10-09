import pymongo
from pymongo import MongoClient
client = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = client['pokemon_test']


def insertPokemon(name=None, type_1=None, type_2=None, link=None, species=None, height=0, weight=0, abilities=None, training_catch_rate=0, training_base_exp=0, training_growth_rate=0, breeding_gender_male=0, breeding_gender_female=0, stats_hp=0, stats_attack=0, stats_defense=0, stats_sp_atk=0, stats_sp_def=0, stats_speed=0, stats_total=0):
    data = {
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
        'stats_total': stats_total,
    }
    print(data)


insertPokemon(name="aa", type_1="2")
