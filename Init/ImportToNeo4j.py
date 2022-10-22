from neo4j import GraphDatabase
import pandas as pd

# define function to build a evolution


def create_pokemon(tx, before_id, before_name, before_img, method, after_id, after_name, after_img):
    tx.run("MERGE (a:Pokemon{id:$before_id,name:$before_name,img:$before_img})"
           "MERGE (b:Pokemon{id:$after_id,name:$after_name,img:$after_img}) "
           "MERGE (a)-[:evolution{method:$method}]->(b)",
           before_id=before_id, before_name=before_name, before_img=before_img, method=method,
           after_id=after_id, after_name=after_name, after_img=after_img)


# get data from csv
db = pd.read_csv('./neo4j.csv')
# connect to db
# change "433-34.csse.rose-hulman.edu" for different host
driver = GraphDatabase.driver(
    'bolt://433-34.csse.rose-hulman.edu:7687', auth=('neo4j', 'neo4j'))

# iterate data
for tmp in db.iterrows():

    data = list(list(tmp)[1])
    before_name = data[0]
    method = data[1]
    after_name = data[2]
    before_id = data[3]
    before_img = data[4]
    after_id = data[5]
    after_img = data[6]

    # call the method to build a evolution
    with driver.session() as session:
        session.execute_write(
            create_pokemon, before_id, before_name, before_img, method, after_id, after_name, after_img)

# print completion
print("done")
