import os
from dotenv import load_dotenv
import digitalocean

load_dotenv()
DO_TOKEN = os.environ['DO_TOKEN']

class DropletTools():
    def __init__(self, token):
        self.manager = digitalocean.Manager(token=token)
        self.my_droplets = self.manager.get_all_droplets()

    def get_droplets(self):
        return self.my_droplets

    def get_droplet_ids(self):
        droplets = self.get_droplets()
        droplet_ids = []
        for droplet in droplets:
            droplet_ids.append(droplet.id)
        return droplet_ids
