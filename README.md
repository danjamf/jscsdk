Just a quick test on JSC automation

Usage `git clone https://github.com/danjamf/jscsdk.git`

Example usage

```
import jscsdk

client = jscsdk.client("radar.wandera.com", "myuser@company.com", "mypassword")

print (client.uemc.sync())
print (client.idp.add("OKTA", "testname", "0oaal7sr2ZeAQVEji5d6", "www.test.com"))


print (client.customThreatLists.get())
print (client.customThreatLists.replace(['www.changed.com', 'nick321.com', "newdomain.com"], 'Block', 'Phishing'))

holdapps =  (client.ztna.listApps())
for app in holdapps:
    if "name" in app:
        print (app["id"] + " " + app["categoryName"] + " " + app["type"] + " " + app["name"])
    else:
        print (app["id"] + " " + app["categoryName"] + " " + app["type"])

holdroutes = client.ztna.listRoutes()
cfrouteid = ""
for route in holdroutes:
    print (route["id"] + " " + route["name"])
    if (route["name"] == "CF"):
        cfrouteid = route["id"]
print (client.ztna.createApp("classApptest123", ["www.testclass123.com"], cfrouteid).text)
```
