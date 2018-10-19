from src.dropletutils import DropletUtils
import csv

class DropletCliTools():
    def __init__(self, doToken, mattermostWebhookUrl):
        self.dropletUtils = DropletUtils(doToken, mattermostWebhookUrl)

    def getDropletUtils(self):
        return self.dropletUtils

    def saveDropletsToFile(self):
        droplets = self.dropletUtils.getAllDroplets()
        dropletsFile = open('droplets.csv', 'w')
        dropletsFile.write(f'id,name,tags\n')
        try:
            for droplet in droplets:
                dropletsFile.write(
                    f'{droplet.id},{droplet.name},{droplet.tags}\n'
                )
            print('Successfully wrote droplets to file droplets.csv')
        except:
            print('Failed to write droplets to file')

    def createDropletList(self, dropletIds):
        droplets = []
        for dropletId in dropletIds:
            dropletFromId = self.dropletUtils.getDropletFromId(dropletId)
            droplets.append(dropletFromId)
        return droplets

    def createDropletIdsFromFile(self, filename):
        dropletIds = []
        csvFile = csv.reader(open(filename, 'r'))
        for line in csvFile:
            dropletIds.append(line[0])
        dropletIds.pop(0)  # Delete 'id' from list
        return dropletIds

    def createDropletListFromFile(self, filename):
        dropletIds = self.createDropletIdsFromFile(filename)
        droplets = self.createDropletList(dropletIds)
        return droplets

    def createSnapshotForDropletsInCsv(self, filename):
        droplets = self.createDropletListFromFile(filename)
        self.dropletUtils.createSnapshotOfDroplets(droplets)

    # def deleteAutoSnapshotsBeforeDate(self, date):
