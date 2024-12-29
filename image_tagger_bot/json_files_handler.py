import json

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_json_file(file_path, data):
    old_data = read_json_file(file_path)
    old_data.update(data)
    write_json_file(file_path, old_data)