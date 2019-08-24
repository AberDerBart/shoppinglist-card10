import copy
import json
from pprint import pprint

import requests
from shoppinglist.config import config

from cpard10 import readFrom, writeTo

device = '/dev/tty.usbmodem14401'
url = f'{config["server"]}/api/{config["list"]}/sync'


def initial_sync():
    return requests.get(url, params={'includeInResponse': ['categories']})


def sync(card10_list):
    return requests.post(url, json={
        'previousSync': card10_list['previousSync'],
        'currentState': card10_list['currentState'],
        'includeInResponse': ['categories']
    })


print("\nREAD1")

card10_list_json = readFrom('shoppinglist.json', device, encoding='latin1')
pprint(card10_list_json)


print("\nSYNC")
try:
    card10_list = json.loads(card10_list_json)
    req_sync_response = sync(card10_list)
    if req_sync_response.status_code != 200:
        raise Exception(req_sync_response.json())
    sync_response = req_sync_response.json()
except Exception as e:
    pprint(e)
    sync_response = initial_sync().json()


print("\nWRITE")
current_state = copy.copy(sync_response['list'])
del current_state['token']
del current_state['changeId']
new_card10_list = {
    'previousSync': sync_response['list'],
    'currentState': current_state,
    'categories': sync_response['categories']
}

new_card10_list_json = json.dumps(new_card10_list)#, indent=True)
print(new_card10_list_json)
writeTo('shoppinglist.json', new_card10_list_json, device, encoding='latin1')


print("\nREAD2")

pprint(readFrom('shoppinglist.json', device, encoding='latin1'))

