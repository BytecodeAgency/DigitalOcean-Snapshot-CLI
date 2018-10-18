from dotenv import load_dotenv
import os
import digitalocean
import requests
import json
import csv

load_dotenv()
DO_TOKEN = os.environ['DO_TOKEN']
MATTERMOST_WEBHOOK_URL = os.environ['MATTERMOST_WEBHOOK_URL']

class DropletUtils():
    def __init__(self, do_token, mattermost_webhook_url):
        self.manager = digitalocean.Manager(token=do_token)
        self.all_droplets = self.manager.get_all_droplets()
        self.notifier = MattermostNotifier(mattermost_webhook_url)

    def get_manager(self):
        return self.manager

    def get_droplet_from_id(self, droplet_id):
        droplet = self.manager.get_droplet(droplet_id)
        return droplet

    def get_all_droplets(self):
        return self.all_droplets

    def get_all_droplet_ids(self):
        droplets = self.get_all_droplets()
        droplet_ids = []
        for droplet in droplets:
            droplet_ids.append(droplet.id)
        return droplet_ids

    def create_snapshot_of_droplet(self, droplet_id):
        droplet = self.manager.get_droplet(droplet_id)
        print(f'Creating snapshot for {droplet.name} ({droplet.id})')
        try:
            droplet.take_snapshot(droplet.name)
            print(f'Snapshot for {droplet.name} ({droplet.id}) started')
            return True
        except:
            print(f'Snapshot for {droplet.name} ({droplet.id}) failed')
            return False

    def create_snapshot_of_droplets(self, droplets):
        droplet_statusses = {}
        for droplet in droplets:
            snapshot_success = self.create_snapshot_of_droplet(droplet.id)
            droplet_statusses[f'{droplet.name (droplet.id)}'] = snapshot_success
        self.notify_statusses(droplet_statusses)

    # TODO: Add time started and time completed
    def notify_statusses(self, droplet_statusses):
        notification_message = '''
            Snapshot report:\n\n
            | Droplet name (id) | Status |
            | ----------------- | ------ |
        '''
        for droplet_status in droplet_statusses:
            notification_message += f'''
                | {droplet_status} | {droplet_statusses[droplet_status]} |
            '''
        self.notifier.send_mattermost_notification(notification_message)

class DropletCliTools():
    def __init__(self, do_token, mattermost_webhook_url):
        self.dropletUtils = DropletUtils(do_token, mattermost_webhook_url)

    def save_droplets_to_file(self):
        droplets = self.dropletUtils.get_all_droplets()
        droplets_file = open('droplets.csv','w')
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
        droplet_ids.pop(0) # Delete 'id' from list
        return droplet_ids

    def create_droplet_list_from_file(self, filename):
        droplet_ids = self.create_droplet_ids_from_file(filename)
        droplets = self.create_droplet_list(droplet_ids)
        return droplets

    def create_snapshot_for_droplets_in_csv(self, filename):
        droplets = self.create_droplet_list_from_file(filename)
        self.dropletUtils.create_snapshot_of_droplets(droplets)

class MattermostNotifier():
    def __init__(self, mattermost_webhook_url):
        self.mattermost_webhook_url = mattermost_webhook_url

    def generate_mattermost_payload(self, message):
        payload_data = { 'text': message }
        payload_json = json.dumps(payload_data)
        return payload_json

    def send_mattermost_notification(self, message):
        payload = self.generate_mattermost_payload(message)
        try:
            response = requests.post(self.mattermost_webhook_url, payload)
            print(f'Mattermost notification sent successfully: {response}')
        except:
            print('Mattermost notification errored')