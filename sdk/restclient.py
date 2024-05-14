import requests
import json
import logging


def getCookies(cookie_jar, domain):
    cookie_dict = cookie_jar.get_dict(domain=domain)
    found = ['%s' % (value) for (name, value) in cookie_dict.items()]
    return ';'.join(found)


def get_radar_auth(radar_domain, admin_email_formated, admin_pass):
    returnauth = dict()
    # print ("Start RADAR auth flow")
    loginpage = requests.get('https://' + radar_domain +
                             '/auth/v1/login-methods?email=' +
                             admin_email_formated)
    # print (loginpage.status_code)
    # print (loginpage.cookies)
    xsrftoken = (getCookies(loginpage.cookies, 'radar.wandera.com'))
    credheaders = {'X-Xsrf-Token': xsrftoken,
                   'Content-Type': 'application/json'}

    creddata = '{"username":"'+admin_email_formated + \
        '","password":"' + admin_pass + '","totp":"","backupCode":""}'
    try:
        credpage = requests.post('https://' + radar_domain +
                                 '/auth/v1/credentials',
                                 data=creddata,
                                 headers=credheaders,
                                 cookies=loginpage.cookies)
    except Exception as err:
        print("An error occurred with RADAR login")
    # print (credpage.cookies)
    loginpage.cookies.update(credpage.cookies)
    returnauth['cookie'] = loginpage.cookies
    try:
        mepage = requests.get('https://' + radar_domain +
                              '/auth/v1/me', cookies=loginpage.cookies)
    except Exception as err:
        print("An error occurred with RADAR me page")
    # print (mepage)
    if (mepage.status_code != 200):
        raise RuntimeError("Issue with RADAR auth user.")
    logging.info(mepage)
    x = json.loads(mepage.text)
    customerid = (x['admin']['entityId'])
    # print (customerid)
    returnauth['customerid'] = customerid
    returnauth['headers'] = credheaders
    returnauth['domain'] = radar_domain
    return returnauth


def sendRest(httpmethod, pathprefix, pathsuffix, creds):

    if (httpmethod == "GET"):
        logging.info("Attempting GET method")
        getresponse = requests.get('https://' + creds['domain'] + pathprefix +
                                   creds['customerid'] +
                                   pathsuffix,
                                   headers=creds['headers'],
                                   cookies=creds['cookie'])
        return (getresponse)
    elif (httpmethod == "POST"):
        logging.info("Attempting POST method")
        postresponse = requests.post('https://' + creds['domain'] +
                                     pathprefix + creds['customerid'] +
                                     pathsuffix,
                                     data=creds['payload'],
                                     headers=creds['headers'],
                                     cookies=creds['cookie'])
        return (postresponse)
    elif (httpmethod == "PATCH"):
        logging.info("Attempting PATCH method")
    elif (httpmethod == "PUT"):
        logging.info("Attempting PUT method")
        postresponse = requests.put('https://' + creds['domain'] +
                                    pathprefix + creds['customerid'] +
                                    pathsuffix, data=creds['payload'],
                                    headers=creds['headers'],
                                    cookies=creds['cookie'])
        return (postresponse)
    elif (httpmethod == "DELETE"):
        logging.info("Attempting DELETE method")
        delresponse = requests.delete('https://' + creds['domain'] +
                                      pathprefix + creds['customerid'] +
                                      pathsuffix, data=creds['payload'],
                                      headers=creds['headers'],
                                      cookies=creds['cookie'])
        return (delresponse)

    else:
        logging.error("Unknown or undefined HTTP method")


def sendRestUEMCendpoints(httpmethod, pathprefix, pathsuffix, creds):

    if (httpmethod == "GET"):
        logging.info("Attempting GET method")
        getresponse = requests.get('https://' + creds['domain'] + pathprefix +
                                   creds['customerid'] + pathsuffix,
                                   headers=creds['headers'],
                                   cookies=creds['cookie'])
        return (getresponse)
    elif (httpmethod == "POST"):
        logging.info("Attempting POST method")
        postresponse = requests.post('https://' + creds['domain'] +
                                     pathprefix + creds['customerid'] +
                                     pathsuffix +
                                     'customerId=' + creds['customerid'],
                                     data=creds['payload'],
                                     headers=creds['headers'],
                                     cookies=creds['cookie'])
        return (postresponse)
    elif (httpmethod == "PATCH"):
        logging.info("Attempting PATCH method")
    elif (httpmethod == "PUT"):
        logging.info("Attempting PUT method")
        postresponse = requests.put('https://' + creds['domain'] +
                                    pathprefix + creds['customerid'] +
                                    pathsuffix +
                                    'customerId=' + creds['customerid'],
                                    data=creds['payload'],
                                    headers=creds['headers'],
                                    cookies=creds['cookie'])
        return (postresponse)
    elif (httpmethod == "DELETE"):
        logging.info("Attempting DELETE method")
        delresponse = requests.delete('https://' + creds['domain'] +
                                      pathprefix + creds['customerid'] +
                                      pathsuffix, data=creds['payload'],
                                      headers=creds['headers'],
                                      cookies=creds['cookie'])
        return (delresponse)

    else:
        logging.error("Unknown or undefined HTTP method")
