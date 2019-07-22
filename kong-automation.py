import os
import classReadYaml, consumers, plugins, key_auth


adminapi = os.environ['KONG_ADMIN_API']
admintoken = os.environ['KONG_ADMIN_TOKEN']

def main():
    apiKeys = key_auth.listApiKey()
    apiKeysWorkspaces = key_auth.listConsumersApiWorkspace()
    apiKeyConsumers = consumers.listConsumersApiKeyAuth()
    consumersNames = consumers.listConsumers()
    consumerWorkspaces = consumers.listConsumersWorkspace()
    pluginNames = plugins.listPlugins()
    pluginWorkspaces = plugins.listPluginsWorkspaces()

    for consumer, workspace in zip(consumersNames, consumerWorkspaces):
        consumers.createConsumer(adminapi, admintoken, consumer, workspace)

    for plugin, workspace in zip(pluginNames, pluginWorkspaces):
        anonymousid = plugins.getAnonymousId(adminapi, admintoken, workspace)
        plugins.createPlugins(adminapi, admintoken, plugin, workspace, anonymousid)

    for apikey, consumer, workspace in zip(apiKeys, apiKeyConsumers, apiKeysWorkspaces):
        key_auth.createKeys(adminapi, admintoken, apikey, workspace, consumer)

if __name__ == "__main__":
    main()