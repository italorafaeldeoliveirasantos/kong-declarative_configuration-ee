import classReadYaml, consumers
import requests


def listPlugins():
    pluginsNames = []
    for i in classReadYaml.jerryboure.data['entities']['plugins']:
        pluginsNames.append(i)

    return pluginsNames


def listPluginsWorkspaces():
    pluginsWorkspaces = []

	for i in classReadYaml.jerryboure.data['entities']['plugins']:
		pluginsWorkspaces.append(classReadYaml.jerryboure.data['entities']['plugins'][i]['workspace'])

	return pluginsWorkspaces
listPlugins()
listPluginsWorkspaces()


def getAnonymousId(adminapi, admintoken, workspace):
    url = adminapi + '/' + workspace + '/consumers' + '/anonymous'
    r = requests.get(url, headers={'Kong-Admin-Token':admintoken}, verify=False)
    
    if r.status_code == 200:
        data = r.json()
        kongConsumerAnonymousId = data['id']

        return kongConsumerAnonymousId

    else:
        workspaceName = workspace
        print('anonymous dont exist!')
        consumers.createConsumer(adminapi, admintoken, consumer='anonymous', workspace=workspaceName)
        getAnonymousId(adminapi, admintoken, workspace)


def checkIfPluginExists(adminapi, admintoken, plugin, workspace):
    url = adminapi + '/' + workspace + '/plugins'
    r = requests.get(url, headers={'Kong-Admin-Token':admintoken}, verify=False)

    if  plugin not in str(r.content):
        print('This plugin dont exists!')
        kongConsumerAnonymousId = getAnonymousId(adminapi, admintoken, workspace)
        createPlugins(adminapi, admintoken, plugin, workspace, kongConsumerAnonymousId)


    else:
        print('This plugin already exists!')
        print(plugin)
        

def createPlugins(adminapi, admintoken, plugin, workspace, anonymousId):
    url = adminapi + '/' + workspace + '/plugins'

    if plugin == 'prometheus':
        payload = { 'name': plugin }
        r = requests.post(url, headers={'Kong-Admin-Token':admintoken}, data=payload, verify=False)

        return r.status_code

    if plugin == 'key-auth':
        payload = { 'name': plugin, 'config.anonymous': anonymousId, 'config.key_names': 'x-api-key', 'config.hide_credentials': 'true' }
        r = requests.post(url, headers={'Kong-Admin-Token':admintoken}, data=payload, verify=False)

        return r.status_code

    if plugin == 'request-termination':
        payload = { 'name': plugin, 'consumer_id': anonymousId, 'config.body': '{"error": "Authentication required"}', 'config.content_type': 'application/json; charset=utf-8', 'config.status_code': '401' }
        r = requests.post(url, headers={'Kong-Admin-Token':admintoken}, data=payload, verify=False)

        return r.status_code


    if plugin == 'openid-connect':
        openidConfig = []

        for i in classReadYaml.jerryboure.data['entities']['plugins']['openid-connect']:
            if i != 'workspace':
                openidConfig.append(classReadYaml.jerryboure.data['entities']['plugins']['openid-connect'][i])

        payload = { 'name': plugin, 'config.anonymous': anonymousId, 'config.audience_claim': 'aud', 'config.auth_methods': 'introspection', 'config.authorization_cookie_httponly': 'false', 'config.authorization_cookie_lifetime': '10', 'config.bearer_token_param_type': 'header', 'config.cache_ttl': '60', 'config.client_credentials_param_type': 'header', 'config.client_id': 'kong', 'config.client_secret': openidConfig[0], 'config.consumer_by': 'username', 'config.consumer_claim': 'azp', 'config.id_token_param_type': 'header', 'config.introspect_jwt_tokens': 'true', 'config.introspection_endpoint': openidConfig[1], 'config.introspection_hint': 'access_token', 'config.issuer': openidConfig[2], 'config.login_action': 'upstream', 'config.login_methods': 'authorization_code, bearer, introspection', 'config.login_tokens': 'access_token', 'config.max_age': '60', 'config.password_param_type': 'header', 'config.refresh_token_param_type': 'header', 'config.session_cookie_lifetime': '30', 'config.timeout': '300000', 'config.token_endpoint_auth_method': 'client_secret_basic', 'config.token_headers_grants': 'client_credentials', 'config.upstream_access_token_header': 'Authorization', 'config.cache_introspection': 'false', 'config.cache_token_exchange': 'false', 'config.cache_tokens': 'false', 'config.cache_user_info': 'false', 'config.logout_revoke_access_token': 'false', 'config.refresh_tokens': 'false', 'config.run_on_preflight': 'false', 'config.session_cookie_httponly': 'false' }
            
        r = requests.post(url, headers={'Kong-Admin-Token':admintoken}, data=payload, verify=False)

        return r.status_code
