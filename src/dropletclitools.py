from src.dropletutils import DropletUtils
import csv

class DropletCliTools():
    def __init__(self, do_token, mattermost_webhook_url):
        self.dropletUtils = DropletUtils(do_token, mattermost_webhook_url)

    def save_droplets_to_file(self):
        droplets = self.dropletUtils.get_all_droplets()
        droplets_file = open('droplets.csv', 'w')
        droplets_file.write(f'id,name,tags\n')
        try:
            for droplet in droplets:
                droplets_file.write(
                    f'{droplet.id},{droplet.name},{droplet.tags}\n'
                )
            print('Successfully wrote droplets to file droplets.csv')
        except:
            print('Failed to write droplets to file')

    def create_droplet_list(self, droplet_ids):
        droplets = []
        for droplet_id in droplet_ids:
            droplet_from_id = self.dropletUtils.get_droplet_from_id(droplet_id)
            droplets.append(droplet_from_id)
        return droplets

    def create_droplet_ids_from_file(self, filename):
        droplet_ids = []
        csv_file = csv.reader(open(filename, 'r'))
        for line in csv_file:
            droplet_ids.append(line[0])
        droplet_ids.pop(0)  # Delete 'id' from list
        return droplet_ids

    def create_droplet_list_from_file(self, filename):
        droplet_ids = self.create_droplet_ids_from_file(filename)
        droplets = self.create_droplet_list(droplet_ids)
        return droplets

    def create_snapshot_for_droplets_in_csv(self, filename):
        droplets = self.create_droplet_list_from_file(filename)
        self.dropletUtils.create_snapshot_of_droplets(droplets)