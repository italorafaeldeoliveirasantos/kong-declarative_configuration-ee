import classReadYaml
import requests


def listServices(configurationfile):
    serviceNames = []
    
    for i in classReadYaml.jerryboure.data['workspaces']['services']:
      serviceNames.append(i)
    
    return serviceNames


def createServices(workspace, serviceName):
    