from dotenv import load_dotenv
import os
import digitalocean
import requests
import json

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

    def get_all_droplets(self):
        return self.all_droplets

    def get_all_droplet_ids(self):
        droplets = self.get_all_droplets()
        droplet_ids = []
        for droplet in droplets:
            droplet_ids.append(droplet.id)
        return droplet_ids

    def save_droplets_to_file(self):
        droplets = self.get_all_droplets()
        droplets_file = open('droplets.csv','w')
        droplets_file.write(f'id,name,tags\n')
        try:
            for droplet in droplets:
                droplets_file.write(
                    f'{droplet.id},{droplet.name},{droplet.tags}\n'
                )
            print('Failed to write droplets to file')
        except:
            print('Successfully wrote droplets to file')

    def create_snapshot_of_droplet(self, droplet_id):
        droplet = self.manager.get_droplet(droplet_id)
        print(f'Creating snapshot for {droplet.name} ({droplet.id})')
        try:
            droplet.take_snapshot(droplet.name)
            print(f'Snapshot for {droplet.name} ({droplet.id}) successful')
            return True
        except:
            print(f'Snapshot for {droplet.name} ({droplet.id}) failed')
            return False

    def create_snapshot_of_droplets(self, droplets):
        droplet_statusses = {}
        for droplet in droplets:
            snapshot_success = self.create_snapshot_of_droplet(droplet.id)
            droplet_statusses[f'{droplet.name (droplet_id)}'] = snapshot_success
        self.notify_statusses(droplet_statusses)

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
