import requests
import json

class MattermostNotifier():
    def __init__(self, mattermost_webhook_url):
        self.mattermost_webhook_url = mattermost_webhook_url

    def generate_mattermost_payload(self, message):
        payload_data = {'text': message}
        payload_json = json.dumps(payload_data)
        return payload_json

    def send_mattermost_notification(self, message):
        payload = self.generate_mattermost_payload(message)
        try:
            response = requests.post(self.mattermost_webhook_url, payload)
            print(f'Mattermost notification sent successfully: {response}')
        except:
            print('Mattermost notification errored')