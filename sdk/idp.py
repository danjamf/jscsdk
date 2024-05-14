from . import restclient


def addIDP(type, name, clientId, orgDomain, creds):
    # to do - only Okta supported rn
    # rint ("Attempting to add IDP")
    postpayload = '{"name":"'+name+'","orgDomain":"'+orgDomain+'","clientId":"'+clientId+'","type":"'+type+'"}'
    creds['payload'] = postpayload
    # postresponse = requests.post('https://' + creds['domain'] + '/gate/identity-service/v1/connections?customerId='+creds['customerid'], data = postpayload, headers=creds['headers'], cookies = creds['cookie'])
    restclient.sendRest("POST", "/gate/identity-service/v1/connections?customerId=", "", creds)
    # print (postresponse)
