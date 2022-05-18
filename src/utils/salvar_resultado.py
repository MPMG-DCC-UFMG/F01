import json

def abrir_existente(job_name):
    try:
        with open('results/' + job_name + '.json') as fp:
            result = json.load(fp)
    except:
        result = {}
    return result

def save_dict_in_json(job_name, result):
    with open('results/' + job_name + '.json', 'w') as json_file:
        json.dump(result, json_file, 
                            indent=4,  
                            separators=(',',': '))