import random
import os
from pathlib import Path

class Marker:
    def __init__(self):
        self.marked = set()
        self.description_file = Path("./images/descriptions.txt")
        if self.description_file.exists():
            with self.description_file.open("r") as f:
                while (line:=f.readline()):
                    num = int(line.split(":")[0][1:-1])
                    self.marked.add(num)
        else:
            with open(self.description_file,"w"):
                pass

    def new_description(self, image_number, list_of_tags):
        with self.description_file.open("a") as f:
            f.write(f'"{image_number}":{list_of_tags}\n')
        self.marked.add(image_number)

    def get_images_list(self):
        return [int(x.split(".")[0]) if x.endswith("jpg") else None for x in os.listdir("./images/")]        

    async def get_random_non_marked_image(self):
        images = self.get_images_list()
        random.shuffle(images)
        for image in images:
            if image not in self.marked and image is not None:
                return image