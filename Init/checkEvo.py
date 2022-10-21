import pandas as pd
db = pd.read_csv('result.csv')
neo = pd.read_csv('neo.csv')
neo['Before_id'] = 0
for i in range(len(neo['Before'].tolist())):
    index = db['name-form'].tolist().index(neo['Before'][i])
    neo['Before_id'][i] = db['id_nb'][index].replace("#", "")

neo['Before_img'] = 0
for i in range(len(neo['Before'].tolist())):
    index = db['name-form'].tolist().index(neo['Before'][i])
    neo['Before_img'][i] = db['img'][index]

neo['After_id'] = 0
for i in range(len(neo['Before'].tolist())):
    index = db['name-form'].tolist().index(neo['After'][i])
    neo['After_id'][i] = db['id_nb'][index].replace("#", "")

neo['After_img'] = 0
for i in range(len(neo['Before'].tolist())):
    index = db['name-form'].tolist().index(neo['After'][i])
    neo['After_img'][i] = db['img'][index]

neo.to_csv('t.csv')
# print(0000 in neo['Before_id'])
# print('0' in neo['After_id'])
# print(db['name-form'][0])
# print(neo['Before'][0])
# print(type(db['name-form']))
# print(neo['Before'][0] in db['name-form'])
# print("done")
