from xml.dom import NoDataAllowedErr
from py2neo import Graph

graph = Graph("bolt://433-34.csse.rose-hulman.edu:7687",
              auth=("neo4j", "neo4j"))

results = graph.run("MATCH(n) return n")

k = "10"
results = graph.run(
    "MATCH ((n)-[]->(m)) WHERE n.id = $id return m", id=k)
# print(results)


for e in results:
    print(e[0]['img'])
    print(e[0]['id'])
    print(e[0]['name'])
