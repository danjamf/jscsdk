from . import restclient
import json
import logging


def delete_device(device_id, creds):
    print("starting device delete")
    baseconfig = "{\"guids\":[\""+device_id+"\"]}"
    creds["payload"] = baseconfig
    response = restclient.sendRestUEMCendpoints(
        "POST", "/gate/device-service/v1/", "/devices/purge?", creds)
    if response.status_code == 200:
        print("Device deleted " +
              creds['customerid'])
        return response
    else:
        print("Error device not deleted " +
              response.status_code + creds['customerid'])


def search_device(search_term, creds):
    print("searching for device " + search_term)
    querystring = "/api/devices?filter%5BfilterId%5D=&filter%5BshowDeleted%5D=false&filter%5BshowActive%5D=true&filter%5BreportingSimultaneously%5D=false&filter%5Bsearch%5D="+search_term + \
        "&filter%5Blocation%5D%5B%5D=domestic&filter%5Blocation%5D%5B%5D=roaming&filter%5BosType%5D%5B%5D=IOS&filter%5BosType%5D%5B%5D=ANDROID&filter%5BosType%5D%5B%5D=WINDOWS&filter%5BosType%5D%5B%5D=MAC_OS&filter%5BosType%5D%5B%5D=UNKNOWN&filter%5BosTypeCount%5D=5&filter%5Buem%5D%5B%5D=notConnected&filter%5Buem%5D%5B%5D=connected&filter%5Buem%5D%5B%5D=autoDeployed&filter%5Buem%5D%5B%5D=notInSyncGroup&filter%5Btethering%5D%5B%5D=tethered&filter%5Btethering%5D%5B%5D=untethered&filter%5BprofileType%5D%5B%5D=wifi&filter%5BprofileType%5D%5B%5D=cellular&filter%5BprofileType%5D%5B%5D=mtdOnly&filter%5BcarrierName%5D=&filter%5Brisk%5D%5B%5D=high&filter%5Brisk%5D%5B%5D=medium&filter%5Brisk%5D%5B%5D=low&filter%5Brisk%5D%5B%5D=secure&page=1&pageSize=50&sort=user&order=1&groupId=&customerId="
    search_response = restclient.sendRest(
        'GET', querystring, '', creds)
    # print(search_response.text)
    devicejson = json.loads(search_response.text)
    # print(len(devicejson))
    return (devicejson)
