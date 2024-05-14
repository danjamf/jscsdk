from . import restclient
import json
import logging


def create_uemc(domain, clientId, clientSecret, creds):
    baseconfig = '{"url":"domain","authStrategy":"JAMF_PRO_OAUTH","deviceSyncAuth":{"clientId":"clientid","clientSecret":"secret"},"isoCountry":"us","vendor":"JAMF_PRO"}'
    newconfig = json.loads(baseconfig)
    newconfig["url"] = domain
    newconfig["deviceSyncAuth"]["clientId"] = clientId
    newconfig["deviceSyncAuth"]["clientSecret"] = clientSecret
    creds["payload"] = json.dumps(newconfig)
    response = restclient.sendRestUEMCendpoints("PUT", "/gate/connector-service/v1/config/", "/emm-server?", creds)
    if response.status_code == 200:
        return response
    else:
        print(response.status_code)


def sync_uemc(creds):
    baseconfig = '{}'

    creds['payload'] = baseconfig
    response = restclient.sendRestUEMCendpoints("POST", "/gate/connector-service/v1/sync/", "?syncMode=FULL&", creds)
    if response.status_code == 202:
        return response
    else:
        print(response.status_code)
