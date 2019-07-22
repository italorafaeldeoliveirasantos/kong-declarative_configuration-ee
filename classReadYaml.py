import yaml
import os

configyaml = os.environ['KONG_CONFIG_FILE']

class jerryboure():
    with open(configyaml, 'r') as stream:
        data = yaml.load(stream)
