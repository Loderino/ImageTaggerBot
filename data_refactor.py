import os
import json
from collections import OrderedDict
shift = 1800


class CustomEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, dict):
            return '{\n' + ','.join(f'"{k}":{self.encode(v)}' for k, v in obj.items()) + '}\n'
        elif isinstance(obj, list):
            return '[' + ','.join(f'"{item}"' if isinstance(item, str) else str(item) for item in obj) + ']\n'
        elif isinstance(obj, str):
            return f'"{obj}"'
        else:
            return json.JSONEncoder.encode(self, obj)

    def iterencode(self, obj, _one_shot=False):
        return self.encode(obj)
    

def update_descriptions():

    result_dict = {}

    with open ("images/descriptions.txt", "r") as f:
        while (line:=f.readline()):
            num, tags = line.split(":")
            num = int(num[1:-1])
            print(num)
            num += shift
            # print(tags[:-2])
            tags = json.loads(tags[:-2])

            lst = result_dict.get(num, [])
            if lst:
                for tag in tags:
                    if tag not in lst:
                        lst.insert(-2, tag)
            else:
                result_dict[num] = ["<start>", *tags, "<end>"]

    # Создаем новый OrderedDict с отсортированными ключами
    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda x: x[0]))

    # Теперь используем sorted_dict для записи в файл
    with open('output.json', 'w') as f:
        json.dump(sorted_dict, f, cls=CustomEncoder, indent=4)

def move_images():
    for i in range (1, 701):
        os.system(f"mv ./images/{i}.jpg /home/kirill/'Рабочий стол'/Диплом/image_tagger/images/{shift+i}.jpg")

#update_descriptions()
move_images()