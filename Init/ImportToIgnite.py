from pyignite import Client
import pandas as pd

# print(data)
client = Client()
client.connect('433-34.csse.rose-hulman.edu', 10800)

Ipokedex = client.get_or_create_cache("Ipokedex")
INameAndId = client.get_or_create_cache("INameAndId")

# INameAndId.remove_all()
# Ipokedex.remove_all()

db = pd.read_csv('./ignite.csv')
for tmp in db.iterrows():
    data = list(list(tmp)[1])
    id = str(data.pop(0))
    for k in range(len(data)):
        data[k] = str(data[k])
        # print(type(data[k]))
    Ipokedex.put(id, data)
    INameAndId.put(data[0], id)

print("done")
