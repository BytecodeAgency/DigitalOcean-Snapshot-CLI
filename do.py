from dotenv import load_dotenv
import os
import digitalocean
import requests
import json

load_dotenv()
DO_TOKEN = os.environ['DO_TOKEN']
MATTERMOST_WEBHOOK_URL = os.environ['MATTERMOST_WEBHOOK_URL']

class DropletUtils():
    def __init__(self, do_token):
        self.manager = digitalocean.Manager(token=do_token)
        self.all_droplets = self.manager.get_all_droplets()

    def get_manager(self):
        return self.manager

    def get_all_droplets(self):
        return self.all_droplets

    def get_droplet_ids(self):
        droplets = self.get_all_droplets()
        droplet_ids = []
        for droplet in droplets:
            droplet_ids.append(droplet.id)
        return droplet_ids

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
