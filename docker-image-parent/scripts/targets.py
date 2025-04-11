#!/usr/bin/python3

import requests
import re
import json
import sys
import urllib3
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


def get_hostname(file):
    hostfile=open(file,'r')
    for line in hostfile.read().splitlines():
        # print(f'LINE: {line}')
        if not re.match(r'^\s*#',line):
            return line
        

# LOGIN
def turbo_login(hostname,username,password):
    url=f'https://{hostname}/vmturbo/rest/login'
    # data={'username': 'Administrator', 'password': 'ta5t1c'}
    # data={'username': 'GB-svc-api', 'password': 'getDataFr0mMe!'}
    data={'username': username, 'password': password}

    # print (f'URL: {url}')
    r=requests.post(url,data=data,verify=False)
    if r.status_code != 200:
        print("Failed to log in to Turbonomic:")
        print(r.text)
        sys.exit(2)
    # head=json.loads(r.headers)
    # print(head)
    cookie=r.headers['Set-Cookie'].split(';')[0]
    return cookie


def get_targets(url, cookie):
    headers={
        "content-type": "application/json",
        "cookie": cookie
    }
    r=requests.get(
        url,
        headers=headers,
        verify=False
    )
    data=json.loads(r.text)
    datafile=open('targets.json','w')
    datafile.writelines(r.text)
    datafile.close()
    # print(r.text)
    return r.text


def list_bad_targets(targets):
    badTargets=[]
    for t in json.loads(targets):
        if t['healthSummary']['healthState'] == 'CRITICAL':
            badTarget={t['displayName']:(t['healthSummary']['healthState'],t['status'])}
            badTargets.append(t)
    # print(badTargets)
    if len(badTargets) != 0:
        print('<div><hr><h2 id="targets_status">Target Health</h2>')
        print(f'{len(badTargets)} targets have a bad status: <p>')
        print('    <table><tr>\
          <th>NAME</th>\
          <th>HEALTH</th></tr>')
        for t in badTargets:
            print(f"<tr>\
                <td><a href='#{t['displayName']}'>{t['displayName']}</td>\
                <td>{t['healthSummary']['healthState']}</td></tr>")
        print('</table></p>')

        for t in badTargets:
            print(f"<h4 id='{t['displayName']}'>{t['displayName']}</h4>")
            print(f"health: {t['healthSummary']['healthState'] }")
            print('<h5>Raw error message</h5>')
            print(f"{t['status']}")
        print('</div>')
        sys.exit(1)

    # ================================= MAIN =================================

hostname=sys.argv[1]
turbo_user=sys.argv[2]
turbo_pass=sys.argv[3]

cookie=turbo_login(hostname, turbo_user, turbo_pass)
url=f'https://{hostname}/api/v3/targets'
targets=get_targets(url=url,cookie=cookie)
list_bad_targets(targets)
