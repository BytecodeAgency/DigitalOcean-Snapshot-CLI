import requests
import json

class MattermostNotifier():
    def __init__(self, mattermostWebhookUrl = None):
        self.mattermostWebhookUrl = mattermostWebhookUrl

    def generateMattermostPayload(self, message):
        payloadData = {'text': message}
        payloadJson = json.dumps(payloadData)
        return payloadJson

    def sendMattermostNotification(self, message):
        if not self.mattermostWebhookUrl:
            print('No Mattermost webhook available. Not sending notification.')
        payload = self.generateMattermostPayload(message)
        try:
            response = requests.post(self.mattermostWebhookUrl, payload)
            print(f'Mattermost notification sent successfully: {response}')
        except:
            print('Mattermost notification errored')