from . import restclient
import json
import logging


def validate_hostname(domain, creds):

    logging.debug('Attempting to validate domain '+domain)
    basevalidateconfig = '{"hostname":"'+domain+'"}'
    creds['payload'] = basevalidateconfig
    postresponse = restclient.sendRest(
        "POST", "/gate/traffic-routing-service/v2/apps/hostnames/validate?customerId=", "", creds)
    # print (postresponse.text)
    x = json.loads(postresponse.text)
    if (x['conflict'] == "NONE"):
        logging.info("No Conflict")
    else:
        logging.error("Possible domain conflict")
        logging.error(x['messageParams'])
    return postresponse


def list_routes(creds):
    logging.debug('Attempting to list all VPN Routes')
    routesresponse = restclient.sendRest(
        'GET', '/api/gateways/vpn-routes?customerId=', '&view=deployments_with_status', creds)

    # routesresponse = requests.get('https://' + radar_domain + '/api/gateways/vpn-routes?customerId='+customerid+'&view=deployments_with_status', headers=headers, cookies = cookies)
    logging.debug(routesresponse.text)
    routesjson = json.loads(routesresponse.text)
    logging.debug(len(routesjson))
    return (routesjson)


def list_apps(creds):
    logging.debug('Attempting to list all App ZTNA Routes')
    appsresponse = restclient.sendRest(
        'GET', '/api/app-definitions/list?customerId=', '', creds)
    logging.debug(appsresponse.text)
    appsjson = json.loads(appsresponse.text)
    logging.debug(len(appsjson))
    return (appsjson)


def find_routes(matchid, creds):
    logging.debug('Attempting to list all VPN Routes')
    routesresponse = restclient.sendRest(
        'GET', '/api/gateways/vpn-routes?customerId=', '&view=deployments_with_status', creds)

    # routesresponse = requests.get('https://' + radar_domain + '/api/gateways/vpn-routes?customerId='+customerid+'&view=deployments_with_status', headers=headers, cookies = cookies)
    logging.debug(routesresponse.text)
    routesjson = json.loads(routesresponse.text)
    logging.debug(len(routesjson))
    for x in routesjson:
        logging.debug(x['name'])
        if (matchid in (x['name'])):
            logging.debug('Found routeID: ' + x['id'])
            return x['id']


def delete_app(appid, appname, creds):
    logging.debug('Delete app id ' + appid)
    routesresponse = restclient.sendRest(
        'DELETE', '/api/app-definitions/' + appid + '?customerId=', '&appName=' + appname, creds)
    return (routesresponse)


def create_app(appname, domains, routeid, creds):
    logging.debug('Creating app config for domains on routeid ' + routeid)
    baseappconfig = json.loads('{"type":"ENTERPRISE","name":"'+appname +
                               '","categoryName":"Uncategorized","hostnames":["testetestset.com"],"bareIps":[],"routing":{"type":"CUSTOM","routeId":"b226","dnsIpResolutionType":"IPv6"},"assignments":{"inclusions":{"allUsers":true,"groups":[]}},"security":{"riskControls":{"enabled":false,"levelThreshold":"HIGH","notificationsEnabled":true},"dohIntegration":{"blocking":false,"notificationsEnabled":true},"deviceManagementBasedAccess":{"enabled":false,"notificationsEnabled":true}}}')
    logging.debug('attempting to modify: ' + baseappconfig['hostnames'][0])
    for index, domain in enumerate(domains):
        if index == 0:  # bit of a hack. Swap out the first one, but for any other we append
            baseappconfig['hostnames'][index] = domain
        else:
            baseappconfig['hostnames'].append(domain)
    logging.debug('attempting to modify: ' +
                  baseappconfig['routing']['routeId'])
    baseappconfig['routing']['routeId'] = routeid
    logging.debug('new config: ' + json.dumps(baseappconfig))
    baseappconfig = json.dumps(baseappconfig)
    creds['payload'] = baseappconfig
    postresponse = restclient.sendRest(
        'POST', '/api/app-definitions?customerId=', '&appName=' + appname, creds)

    logging.debug(postresponse.text)
    return (postresponse)


''' the following need refactoring

def vpn_config_modify(deploymentcorejson):
    vpnjson = json.loads('{"deployment":{"datacenter":"us-west-2","enabled":true,"components":{"vpnLoadBalancer":{"deployment":[]},"vpnRouter":{"deployment":{"availabilityZones":["us-west-2a"],"publicNodes":{"enabled":false}},"tunnel":{"ipsec":{"keyExchange":"ikev2","ike":{"encryption":["aes256"],"integrity":["sha512"],"dhGroups":["modp2048"],"lifetimeInSec":28800},"esp":{"encryption":["aes256"],"integrity":["sha512"],"dhGroups":["modp2048"],"lifetimeInSec":28800},"left":{"id":"wpa.wandera.com","host":"%any","subnets":["192.168.253.0/24"],"auth":"psk"},"right":{"id":"%any","host":"1.2.3.2","subnets":["0.0.0.0/0"],"auth":"psk","vendor":"strongSwan"}}}}},"id":"1249b56c-ecec-4d13-ae4d-d642f91570b5","routeId":"889d","infraSpecHash":"rwm0kxmFqI","status":{"id":"e3ee298b-3c94-4120-9824-c034a2549744","routeId":"889d","datacenter":"us-west-2","status":"DOWN","infraStatus":"UP","tunnelStatus":"DOWN","infraSpecHash":"rwm0kxmFqI","timestampInMs":1712360149659},"createdAtInMs":1712164314318,"updatedAtInMs":1712360107617},"vpnRoute":{"contact":{"email":"none@none.com","name":"None"},"customerIds":["993ae0ee-4bd8-4325-bc5d-1db0ea45b4f6"],"name":"TF QC","shared":false}}')
    #print (vpnjson['deployment']['components']['vpnRouter']['tunnel']['ipsec']['right']['host'])
    print ("hello modifying vpn config")
    vpnjson['deployment'] = deploymentcorejson
    print (vpnjson['deployment']['components']['vpnRouter']['tunnel']['ipsec']['right']['host'])
    print (json.dumps(vpnjson))
    return json.dumps(vpnjson)






def load_vpn(customerid, cookies, headers): #not used
    vpnconfig = requests.get('https://' + radar_domain + '/api/gateways/vpn-routes/889d?customerId=993ae0ee-4bd8-4325-bc5d-1db0ea45b4f6&view=deployments_with_status', headers=headers, cookies=cookies)
    print("found vpn config")
    print (vpnconfig.text)




def update_vpn(customerid, cookies, headers):

    routeid = sys.argv[2]
    currentconfig = requests.get('https://' + radar_domain + '/api/gateways/vpn-routes/'+routeid+'?customerId='+customerid+'&view=deployments_with_status', headers=headers, cookies = cookies)
    print ('Here is the current returned ENTIRE config')
    print (currentconfig.text)
    x = json.loads(currentconfig.text)
    #templatevpnjson = json.loads('{"deployment":{"datacenter":"us-west-2","enabled":true,"components":{"vpnLoadBalancer":{"deployment":[]},"vpnRouter":{"deployment":{"availabilityZones":["us-west-2a"],"publicNodes":{"enabled":false}},"tunnel":{"ipsec":{"keyExchange":"ikev2","ike":{"encryption":["aes256"],"integrity":["sha512"],"dhGroups":["modp2048"],"lifetimeInSec":28800},"esp":{"encryption":["aes256"],"integrity":["sha512"],"dhGroups":["modp2048"],"lifetimeInSec":28800},"left":{"id":"wpa.wandera.com","host":"%any","subnets":["192.168.253.0/24"],"auth":"psk"},"right":{"id":"%any","host":"52.11.198.182","subnets":["0.0.0.0/0"],"auth":"psk","vendor":"strongSwan"}}}}},"id":"1249b56c-ecec-4d13-ae4d-d642f91570b5","routeId":"889d","infraSpecHash":"e3FNqcmBMT","status":{"id":"140df4cb-3dd6-4cca-8f27-163ed9579586","routeId":"889d","datacenter":"us-west-2","status":"DOWN","infraStatus":"UP","tunnelStatus":"DOWN","infraSpecHash":"e3FNqcmBMT","timestampInMs":1712351816043},"createdAtInMs":1712164314318,"updatedAtInMs":1712350482282},"vpnRoute":{"contact":{"email":"none@none.com","name":"None"},"customerIds":["993ae0ee-4bd8-4325-bc5d-1db0ea45b4f6"],"name":"TF QC","shared":false}}')
    print ('Here is the deployments[0] config with modificiation of IP')
    #print (x['deployments'][0])
    deploymentcorejson = x['deployments'][0]
    deploymentcorejson['components']['vpnRouter']['tunnel']['ipsec']['right']['host'] = sys.argv[1]
    print (deploymentcorejson)
    #print (vpn_config_modify(deploymentcorejson))
    print ('here is the extracted vpn-route ID:')
    print (deploymentcorejson['id'])
    updatevpnpage = requests.patch('https://' + radar_domain + '/api/gateways/vpn-routes/'+deploymentcorejson['id']+'?customerId=' + customerid, data = (vpn_config_modify(deploymentcorejson)), headers=headers, cookies = cookies)
    print (updatevpnpage)
'''
