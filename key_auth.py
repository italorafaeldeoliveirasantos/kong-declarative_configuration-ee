import classReadYaml, consumers
import requests

def listApiKey():
    apiKeyConsumerNames = consumers.listConsumersApiKeyAuth()
    consumersName = classReadYaml.jerryboure.data['entities']['consumers']
    apiKey = []

    for i in apiKeyConsumerNames:
        apiKey.append(consumersName[i]['authentication']['key'])

    return apiKey


def listConsumersApiWorkspace():
    consumersApiKeyAuthWorkspaces = []
    consumers = classReadYaml.jerryboure.data['entities']['consumers']

    for i in consumers:
        if 'key-auth' in consumers[i]['authentication']['type']:
            consumersApiKeyAuthWorkspaces.append(classReadYaml.jerryboure.data['entities']['consumers'][i]['workspace'])

    return consumersApiKeyAuthWorkspaces


def checkIfKeyExists(adminapi, admintoken, apikey, workspace, consumer):
    url = adminapi + '/'  + workspace + '/consumers/' + consumer + '/key-auth'
    r = requests.get(url, headers={'Kong-Admin-Token':admintoken}, verify=False)
    data = r.json()

    if  apikey not in data['data'][0]['key']:
        print('This apikey dont exists!')
        createKeys(adminapi, admintoken, apikey, workspace, consumer)


    else:
        print('This key already exists!')
        return


def createKeys(adminapi, admintoken, apikey, workspace, consumer):
    url = adminapi + '/'  + workspace + '/consumers/' + consumer + '/key-auth'

    if consumer != 'anonymous':
        payload = { 'key': apikey }
        r = requests.post(url, headers={'Kong-Admin-Token':admintoken}, data=payload, verify=False)

        return r.json()
    
    else:

        return
