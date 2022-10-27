from xml.dom import NoDataAllowedErr
from py2neo import Graph

graph = Graph("bolt://433-34.csse.rose-hulman.edu:7687",
              auth=("neo4j", "neo4j"))

results = graph.run("MATCH(n) return n")

#results = graph.run(
#   "MATCH path=(b: Pokemon{b})-[e*] -> (a)) WHERE b.id=10 AND WHERE NOT (a)-->() return DISTINCT e")
# print(results)


for e in results:
    # print(b)
    print("  ")
    print(e)
    print("  ")
    # print(a)
    print("  ")
    print("  ")
    print("  ")
