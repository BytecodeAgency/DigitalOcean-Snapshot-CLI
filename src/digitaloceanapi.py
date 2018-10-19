########################################################################
# Note: this is not a complete API, just an interface to centralize
#       requests made by the API to keep everything neat and organized
########################################################################

from datetime import date
import os
import json
import requests

DO_API_BASE_URL = 'https://api.digitalocean.com/v2/'
AUTO_SNAPSHOT_IDENTIFIER = 'auto-snapshot'


def generateSnapshotName(dropletName):
    dateToday = date.today()
    snapshotName = f'{AUTO_SNAPSHOT_IDENTIFIER} of {dropletName} on {dateToday}'
    return snapshotName

class RequestsError(BaseException):
    pass


class ResponseError(BaseException):
    pass


class BaseDigitalOceanAPI():
    def __init__(self, digitaloceanApiKey):
        self.digitaloceanApiKey = digitaloceanApiKey

    def getDoSnapshotIdentifier(self):
        return AUTO_SNAPSHOT_IDENTIFIER

    def generateUrl(self, endpoint):
        return DO_API_BASE_URL + endpoint

    def getRequestHeaders(self, method):
        requestHeaders = {
            'Authorization': f'Bearer {self.digitaloceanApiKey}',
            'Content-type': 'application/json',
        }
        return requestHeaders

    def doRequest(self, requestUrl, method, jsonBody, headers):
        response = None
        if method == 'GET':
            response = requests.get(requestUrl, headers=headers)
        elif method == 'POST':
            response = requests.post(requestUrl, jsonBody, headers=headers)
        elif method == 'PUT':
            response = requests.put(requestUrl, jsonBody, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(requestUrl, headers=headers)
        else:
            raise RequestsError('Request invalid')
        return response

    def dealWithPagination(self, url, method, body, data)

    def performRequest(self, url, method, body=None):
        requestUrl = self.generateUrl(url)
        headers = self.getRequestHeaders(method)
        jsonBody = json.dumps(body)
        response = self.doRequest(requestUrl, method, jsonBody, headers)
        jsonResponse = json.loads(response.content)
        if not self.validateResponse(response):
            raise ResponseError('Something went wrong while making the request')

        try:
            if jsonResponse['links']['pages']['next']:
                # Recursion to deal with pagination
                jsonResponse.update(self.performRequest(url, method, body))
        except:
            return jsonResponse
        return jsonResponse

    def getRequest(self, url):
        return self.performRequest(url, 'GET')

    def postRequest(self, url, body):
        return self.performRequest(url, 'POST', body)

    def putRequest(self, url, body):
        return self.performRequest(url, 'PUT', body)

    def deleteRequest(self, url):
        return self.performRequest(url, 'DELETE')

    def validateResponse(self, response):
        httpStatusRange = int(str(response.status_code)[0])
        if httpStatusRange == 2:
            return True
        elif httpStatusRange == 4:
            return False
        elif httpStatusRange == 5:
            return False
        else:
            raise ResponseError('Response has an incorrect status code')


class DigitalOceanAPI(BaseDigitalOceanAPI):
    def __init__(self, digitaloceanApiKey):
        super()
        self.digitaloceanApiKey = digitaloceanApiKey

    def getAllDroplets(self):
        requestUrl = 'droplets'
        return self.getRequest(requestUrl)['droplets']

    def getAllDropletsBasicData(self):
        allDroplets = self.getAllDroplets()
        allDropletsBasicData = []
        for droplet in allDroplets:
            singleDropletBasicData = {
                'id': droplet['id'],
                'name': droplet['name'],
                'status': droplet['status'],
            }
            allDropletsBasicData.append(singleDropletBasicData)
        return allDropletsBasicData

    def getDropletById(self, dropetId):
        requestUrl = f'droplets/{dropetId}'
        return self.getRequest(requestUrl)['droplet']

    def getAllSnapshots(self):
        requestUrl = 'snapshots?resource_type=droplet'
        return self.getRequest(requestUrl)['snapshots']

    def createDropletSnapshot(self, dropletId, dropletName):
        requestUrl = f'droplets/{dropletId}/actions'
        body = {'type': 'snapshot', 'name': generateSnapshotName(dropletName)}
        rawResponse = self.postRequest(requestUrl, body)
        responseStatus = rawResponse['action']['status']
        return responseStatus
