########################################################################
# Note: this is not a complete API, just an interface to centralize
#       requests made by the API to keep everything neat and organized
########################################################################

import os
import json
import requests

DO_API_BASE_URL = "https://api.digitalocean.com/v2/"


class RequestsError(BaseException):
    pass


class BaseDigitalOceanAPI():
    def __init__(self, digitaloceanApiKey):
        self.digitaloceanApiKey = digitaloceanApiKey

    def generateUrl(self, endpoint):
        return DO_API_BASE_URL + endpoint

    def getRequestHeaders(self, method):
        requestHeaders = {
            'Authorization': f'Bearer {self.digitaloceanApiKey}',
            'Content-type': 'application/json',
        }
        print(requestHeaders)
        return requestHeaders

    def performRequest(self, url, method, body=None, params=None):
        requestUrl = self.generateUrl(url)
        headers = self.getRequestHeaders(method)
        jsonBody = json.dumps(body)
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

    def getRequest(self, url, params=None):
        return self.performRequest(url, 'GET')

    def postRequest(self, url, body):
        return self.performRequest(url, 'POST', body)

    def putRequest(self, url, body):
        return self.performRequest(url, 'PUT', body)

    def deleteRequest(self, url):
        return self.performRequest(url, 'DELETE')

    def validateRequest(self, response):
        http_status_range = int(str(response.status_code)[0])
        if http_status_range == 2:
            print('2xx')
        elif http_status_range == 4:
            print('4xx')
        elif http_status_range == 5:
            print('5xx')
        else:
            print('Not 2xx, 4xx or 5xx')


