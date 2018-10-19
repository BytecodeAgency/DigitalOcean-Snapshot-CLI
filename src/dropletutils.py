from src.mattermostnotifier import MattermostNotifier
from src.digitaloceanapi import DigitalOceanAPI
from datetime import date


class DropletUtils():
    def __init__(self, doToken, mattermostWebhookUrl):
        self.digitaloceanApi = DigitalOceanAPI(doToken)
        self.allDroplets = self.digitaloceanApi.getAllDroplets()
        self.notifier = MattermostNotifier(mattermostWebhookUrl)
        self.autoSnapshotIdentifier = self.digitaloceanApi.getDoSnapshotIdentifier()

    def getDigitaloceanApi(self):
        return self.digitaloceanApi

    def getDropletFromId(self, dropletId):
        droplet = self.digitaloceanApi.getDropletById(dropletId)
        return droplet

    def getAllDroplets(self):
        return self.allDroplets

    def getAllDropletIds(self):
        droplets = self.getAllDroplets()
        dropletIds = []
        for droplet in droplets:
            dropletIds.append(droplet.id)
        return dropletIds

    def getAllAutoSnapshots(self):
        snapshots = self.getDigitaloceanApi().getAllSnapshots()
        autoSnapshots = []
        for snapshot in snapshots:
            if self.autoSnapshotIdentifier in snapshot['name']:
                autoSnapshots.append(snapshot)
        return autoSnapshots

    def createSnapshotOfDroplet(self, dropletId):
        droplet = self.getDigitaloceanApi().getDropletById(dropletId)
        dropletName = droplet.name
        print(f'Creating snapshot for {droplet.name} ({droplet.id})')
        try:
            self.getDigitaloceanApi().createDropletSnapshot(dropletId, dropletName)
            print(f'Snapshot for {droplet.name} ({droplet.id}) started')
            return True
        except:
            print(f'Snapshot for {droplet.name} ({droplet.id}) failed')
            return False

    def createSnapshotOfDroplets(self, droplets):
        dropletStatusses = []
        for droplet in droplets:
            snapshotSuccess = self.createSnapshotOfDroplet(droplet.id)
            dropletIdentifier = f'{droplet.name} ({droplet.id})'
            dropletStatus = {
                'identifier': dropletIdentifier, 'status': snapshotSuccess
            }
            dropletStatusses.append(dropletStatus)
        self.notifyStatusses(dropletStatusses)

    def notifyStatusses(self, dropletStatusses):
        notificationMessage = ''
        notificationMessage += 'Snapshot report:'
        notificationMessage += '\n\n'
        notificationMessage += '| Droplet name (id) | Status |\n'
        notificationMessage += '| ----------------- | ------ |\n'
        for droplet in dropletStatusses:
            newRow = f"| {droplet['identifier']} | {droplet['status']} |\n"
            notificationMessage += newRow
        self.notifier.sendMattermostNotification(notificationMessage)
