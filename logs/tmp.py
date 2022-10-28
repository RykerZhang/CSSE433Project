from pymongo import MongoClient
data = {
    'a': 100,
    'b': 200
}

# log = "db.pokedex.insert_one("+str(data)+")"
# print(log)

Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = Mclient['pokemon']

# exec(log)
p = {
    'id': "10",
    'name-form': "Bulbasaur-Bulbasaur",
    'type_1': "Grass",
    'type_2': "Poison",
    'data_species': "Seed Pokémon",
    'img': "https://img.pokemondb.net/artwork/large/bulbasaur.jpg"
}
# print(type(p))
db.pokedex.insert_one(p)
