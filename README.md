# This repo has a collection of scripts that creates Kong consumers, plugins and key-auth

## Before running 
- set some env
```bash
foo@bar:~ export KONG_ADMIN_API=http://localhost:8001
foo@bar:~ export KONG_ADMIN_TOKEN=teste
foo@bar:~ export KONG_CONFIG_FILE=list.yml
```

- Install python requirements
```bash
foo@bar:~ pip3 install -r requirements.txt
```

## To run
```bash
foo@bar:~ python3 kong-automation.py
```