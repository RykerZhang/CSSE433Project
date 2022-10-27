from py2neo import Graph

graph = Graph("bolt://433-34.csse.rose-hulman.edu:7687",
              auth=("neo4j", "neo4j"))

results = graph.run("MATCH (n:Pokemon) return n")
#results = graph.run(
    #"MATCH path=(b: Pokemon{b})-[e*] -> (a) WHERE b.id=10 AND WHERE ！(a)-->() return DISTINCT e")
# print(results)

#for e in results:
   # print("  ")
    #print(e)
   # print("  ")

def getEvo(id):
    #get name
    evoNameResult = graph.run("MATCH ((n)-[]->(m)) "
                          "WHERE n.id = $id " 
                          "return m.name", id=id)
    evoNameArray = []
    for e in evoNameResult:
        evoNameArray.append(e["m.name"])
    #get id
    evoIdResult = graph.run("MATCH ((n)-[]->(m)) "
                          "WHERE n.id = $id " 
                          "return m.id", id=id)
    evoIdArray = []
    for e in evoIdResult:
        evoIdArray.append(e["m.id"])
    #get img link string
    evoImgResult = graph.run("MATCH ((n)-[]->(m)) "
                          "WHERE n.id = $id " 
                          "return m.img", id=id)
    evoImgArray = []
    for e in evoImgResult:
        evoImgArray.append(e["m.img"])
    dict = {}
    dict["name"] = evoNameArray
    dict["id"] = evoIdArray
    dict["img"] = evoImgArray
    print(dict)
    
def getPrevEvo(id):
    #get name
    evoNameResult = graph.run("MATCH ((n)-[]->(m)) "
                          "WHERE m.id = $id " 
                          "return n.name", id=id)
    evoNameArray = []
    for e in evoNameResult:
        evoNameArray.append(e["n.name"])
    #get id
    evoIdResult = graph.run("MATCH ((n)-[]->(m)) "
                          "WHERE m.id = $id " 
                          "return n.id", id=id)
    evoIdArray = []
    for e in evoIdResult:
        evoIdArray.append(e["n.id"])
    #get img link string
    evoImgResult = graph.run("MATCH ((n)-[]->(m)) "
                          "WHERE m.id = $id " 
                          "return n.img", id=id)
    evoImgArray = []
    for e in evoImgResult:
        evoImgArray.append(e["n.img"])
    dict = {}
    dict["name"] = evoNameArray
    dict["id"] = evoIdArray
    dict["img"] = evoImgArray
    print(dict)
    
getPrevEvo(2970)