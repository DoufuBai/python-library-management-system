import json

def  save_json(filename, data):
    with open(filename,'w',encoding = 'utf-8') as file:
        json.dump(data,file,ensure_ascii= False,indent = 4)
        

def load_json(filename, default_data):
    try:
        with open(filename,'r',encoding= 'utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        save_json(filename,default_data)
        return default_data
    except json.JSONDecodeError:
        save_json(filename,default_data)
        return default_data

        