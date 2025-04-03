import sys
import json
import requests
from requests.auth import HTTPBasicAuth
turbohost='turbo-dev.ikp103s.cloud.uk.hsbc'
# LOGIN
url=f'https://{turbohost}/vmturbo/rest/login'
data={'username': 'GB-svc-api', 'password': 'getDataFr0mMe!'}
r=requests.post(url,data=data,verify=False)
print(r.headers)
print(r.cookies)

cookie=r.headers['Set-Cookie'].split(';')[0]
print (cookie)

cursor='0'
# url=f'https://{turbohost}/api/v3/markets/Market'
url=f'https://{turbohost}/api/v3/settingspolicies'
headers = {"Content-Type": "application/json", "cookie":cookie}
r=requests.get(url,headers=headers,verify=False)
# print(r.text)
print(r)
poldata=json.loads(r.text)
for pol in poldata:
    print(f"POL {pol['uuid']},{pol['displayName']}")


url=f'https://{turbohost}/api/v3/groups'
headers = {"Content-Type": "application/json", "cookie":cookie}
r=requests.get(url,headers=headers,verify=False)
# print(r.text)
print(r)
grpdata=json.loads(r.text)
for grp in grpdata:
    print(f"GRP {grp['uuid']},{grp['displayName']}")

# while cursor != '':
#     payload={"cursor": cursor}
#     print(cursor)
#     a=requests.get(url,headers=headers,params=payload,verify=False)
#     cursor=a.headers['X-Next-Cursor']
#     print(a.text)
    # act=json.loads(a.text)
    # for obj in act:
    #     if obj['actionType']=='SCALE' and obj['target']['className'] != 'VirtualVolume':
    #         print(obj)
    #         quit()



# # url=f'https://{turbohost}/api/v3/search?types=VirtualMachine&entity_types=VirtualMachines'
# url=f'https://{turbohost}/api/v3/search'
# headers = {"Content-Type": "application/json", "cookie":cookie}
# payload={"types": "VirtualMachine", "entity_types": "VirtualMachines", "displayName": "hsbc-8578861-pdl-dev"}
# v=requests.get(url,headers=headers,params=payload,verify=False)
# print(v.text)
# vm=json.loads(v.text)
# # print(vm[0])




# uuid=75636714703111
# url=f'https://{turbohost}/api/entities/{uuid}/actions'
# headers = {"Content-Type": "application/json", "cookie":cookie}
# a=requests.get(url,headers=headers,verify=False)
# print(a.text)
# ac=json.loads(a.text)
# print(ac)

