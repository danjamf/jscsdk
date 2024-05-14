from . import restclient
import json
import logging


def replaceCustomThreats(domains, action, category, creds):
    logging.debug('attempting custom threat upload')
    payloadoutput = "Resource,Action,Threat category"

    for domain in domains:
        payloadoutput = payloadoutput + "\n" + domain + "," + action + "," + category
    creds['payload'] = payloadoutput

    response = restclient.sendRest("PUT", "/api/settings/custom_threat_intelligence/import?customerId=", "&importerId=admin@jscsdk.com", creds)
    if response.status_code == 200:
        return response
    else:
        logging.error("unable to replace custom threats " + response)


def appendCustomThreats(domains, action, category, creds):
    logging.debug("attempting custom threat upload with append")
    existingdomains = getCustomThreats(creds)
    payloadoutput = "Resource,Action,Threat category"
    for existingdomain in existingdomains:
        domains.append(existingdomain)
    for domain in domains:
        payloadoutput = payloadoutput + "\n" + domain + "," + action + "," + category
    creds['payload'] = payloadoutput
    logging.debug(payloadoutput)
    response = restclient.sendRest("PUT", "/api/settings/custom_threat_intelligence/import?customerId=", "&importerId=admin@jscsdk.com", creds)
    if response.status_code == 200:
        return response
    else:
        logging.error("unable to append custom threats " + response)


def getCustomThreats(creds):
    logging.debug("Attempting to get existing custom threats")
    output = restclient.sendRest("GET", "/api/settings/custom_threat_intelligence/resources?customerId=", "", creds)  # todo add pagination
    records = json.loads(output.text)
    outputlist = []
    for record in records["records"]:
        logging.debug("Found " + record["resource"])
        outputlist.append(record["resource"])
    return outputlist
