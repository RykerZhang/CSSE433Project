import csv
import json
 
def csv_to_json(csv_file_path):
    #create a dictionary
    data_dict = {}
    cnt = 1
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for row in csv_reader:
            out = json.dumps(row, indent = 4, ensure_ascii = False)
            jsonoutput = open('json/Pokemon#' + str(cnt) + '.json', 'w')
            jsonoutput.write(out)
            cnt += 1
 
#driver code
#be careful while providing the path of the csv file
#provide the file path relative to your machine
 
#Step 1
csv_file_path = 'pokemon_db.csv'
 
csv_to_json(csv_file_path)
