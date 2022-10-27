import json
import time

data_dict = {}

def write_to_log(type, fields):
    timestamp = time.time()
    tp = timestamp
    data_dict = {"type": type, "fields": fields, "timestamp": timestamp}
    with open("logs/" + str(timestamp) + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
    return timestamp


data = {'id': 9990, 'name-form': "New", 'type_1': "Grass", 'type_2': "Bug", 'data_species': "New Pokemon", 'img': "img"}


tp = write_to_log("insert", data)


def read_log(file_name):
    f = open("logs/" + str(file_name) + '.json', 'r', encoding='utf-8')
    data = json.load(f)
    tp = data['type']
    fields = data['fields']
    timestamp = data['timestamp']
    print(tp)
    print(fields)
    print(timestamp)
    return tp, fields, timestamp


read_log(tp)