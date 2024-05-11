from . import restclient
from . import customthreat
from . import ztna
from . import uemc
import logging



class JSC:
    def __init__(self, host, username, password, loglevel = logging.critical):
        self.host = host
        self.username = username
        self.password = password
        self.creds = restclient.get_radar_auth(host, username, password)
        self.customThreatLists = self.ctclass(self.creds)
        self.ztna = self.ztnaclass(self.creds)
        self.uemc = self.uemcclass(self.creds)
        logging.basicConfig(level=loglevel, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logging = logging.getLogger(__name__)
        self.logging.info  ("auth completed")
        
    class uemcclass:
        def __init__(self, creds) -> None:
            self.creds = creds
            self.uemcimport = uemc
        def create(self, domain, clientId, clientSecret):
            return(self.uemcimport.create_uemc(domain, clientId, clientSecret, self.creds))
        def sync(self):
            return(self.uemcimport.sync_uemc(self.creds))

    
    class ztnaclass:
        def __init__(self, creds) -> None:
            self.creds = creds
            self.ztnamimport = ztna
        def listRoutes(self):
            return(self.ztnamimport.list_routes(self.creds))
        def createApp(self, appname, domains, routeid):
            return(self.ztnamimport.create_app(appname, domains, routeid, self.creds))
        def validateHostname(self, domain):
            return(self.ztnamimport.validate_hostname(domain, self.creds))
        def listApps(self):
            return(self.ztnamimport.list_apps(self.creds))
        def delApp(self, appId, appName):
            return(self.ztnamimport.delete_app(appId, appName, self.creds))
                   


    class ctclass:
        def __init__(self, creds) -> None:
            self.customthreat = customthreat
            self.creds = creds
        def replace(self, domains, action, threat_type):
            return(self.customthreat.replaceCustomThreats(domains, action, threat_type, self.creds))
        def get(self):
            return (self.customthreat.getCustomThreats(self.creds))



#just for local testing
if __name__ == "__main__":
    client = JSC("radar.wandera.com", "auth@myauth.com", "mypass")
    print (client.customThreatLists.replaceCustomThreats(['www.secondclass.com', 'nick321.com', "newdomain.com"], 'Block', 'Phishing'))
    hold = client.customThreatLists.getCustomThreats()
    print (hold)
    print (client.ztna.listRoutes())
    holdroutes = client.ztna.listRoutes()
    for route in holdroutes:
        print (route["id"])

    print (client.ztna.createApp("classApptest", ["www.testclass.com"], "889d"))





