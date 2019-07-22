import classReadYaml
import requests

def listConsumers():
    consumersNames = []
    
    for i in classReadYaml.jerryboure.data['entities']['consumers']:
      consumersNames.append(i)
    
    return consumersNames


def listConsumersWorkspace():
    consumersWorkspace = []

    for i in classReadYaml.jerryboure.data['entities']['consumers']:
        consumersWorkspace.append(classReadYaml.jerryboure.data['entities']['consumers'][i]['workspace'])

    return consumersWorkspace


def listConsumersApiKeyAuth():
    consumersApiKeyAuthNames = []
    consumers = classReadYaml.jerryboure.data['entities']['consumers']

    for i in consumers:
        if 'key-auth' in consumers[i]['authentication']['type']:
            consumersApiKeyAuthNames.append(i)

    return consumersApiKeyAuthNames

import requests


def checkIfUserExists(adminapi, admintoken, consumer, workspace):
    url = adminapi + '/' + workspace + '/consumers'
    r = requests.get(url, headers={'Kong-Admin-Token':admintoken}, verify=False)


    if 'anonymous' not in str(r.content):
        createConsumer(adminapi, admintoken, consumer='anonymous', workspace='globalsales')
    
    if  consumer not in str(r.content):
        print('This consumer dont exists!')
        createConsumer(adminapi, admintoken, consumer, workspace)

    else:
        print('This consumer already exists!')
        print(consumer)


def createConsumer(adminapi, admintoken, consumer, workspace):
    url =  adminapi + '/'  + workspace + '/consumers'
    payload = { 'username': consumer }
    r = requests.post(url, headers={'Kong-Admin-Token':admintoken}, data=payload, verify=False)

    return r.content

listConsumers()