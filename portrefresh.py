#/usr/bin/python

import argparse
import json
import requests

port_uuid_list = []
security_group_list = []

#Disable warning messages to prevent screen filling up
requests.packages.urllib3.disable_warnings()

class Auth:

    auth_url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    auth_headers = {'Content-type': 'application/json'}

    def __init__(self, user, api_key):
        self.user = user
        self.api_key = api_key

    def auth_call(self):
        self.auth_data = json.dumps({"auth": {'RAX-KSKEY:apiKeyCredentials': {'username': self.user, 'apiKey': self.api_key}}})
        self.auth_request = requests.post(self.auth_url, data=self.auth_data, headers=self.auth_headers)
        self.token_raw = self.auth_request.json()['access']['token']['id']
        self.token = str(self.token_raw)
        return self.token

#Find all port UUIDs so they can be filtered by security group id
def find_port_api(region, token):
    port_url = "https://%s.networks.api.rackspacecloud.com/v2.0/ports" % region
    port_request_headers = {'X-Auth-Token': token}
    port_get_request = requests.get(port_url, headers=port_request_headers)
    port_return = port_get_request.text
    port_parse = json.loads(port_return)['ports']
    for port_uuid in port_parse:
        if network_uuid in port_uuid['network_id']:
            port_uuid_list.append(port_uuid['id'])

#Find all ports associated with defined security group and update them            
def list_and_refresh_by_securitygroup(region, token):
    for port_uuid in port_uuid_list:
        port_url = "https://%s.networks.api.rackspacecloud.com/v2.0/ports/%s" % (region, port_uuid)
        port_request_headers = {'X-Auth-Token': token}
        port_get_request = requests.get(port_url, headers=port_request_headers)
        port_return = port_get_request.text
        port_parse_sg_id = json.loads(port_return)['port']['security_groups']
        if security_uuid in port_parse_sg_id:
            print "Refreshing port: "
            print port_uuid
            port_refresh_url = "https://%s.networks.api.rackspacecloud.com/v2.0/ports/%s" % (region, port_uuid)
            port_refresh_headers = {'X-Auth-Token': token}
            port_refresh_data = json.dumps({"port": {"security_groups": port_parse_sg_id}})
            port_put_request = requests.put(port_refresh_url, headers=port_refresh_headers, data=port_refresh_data)
            port_refresh_return = port_put_request.text
            print "Port Refresh Response: "
            print port_refresh_return
        

parser = argparse.ArgumentParser()

parser.add_argument('--securitygroup',
required=True,
default=None,
help='The security group UUID you want to refresh')

parser.add_argument('--region',
required=True,
default=None,
help='The region of the security group')

parser.add_argument('--ddi',
required=True,
default=None,
help='Your account number or DDI')

parser.add_argument('--user',
required=True,
default=None,
help='The username for your account')

parser.add_argument('--apikey',
required=True,
default=None,
help='Your account API key')

parser.add_argument('--network',
required=True,
default=None,
help='The network UUID of the private network')

args = parser.parse_args()

user = args.user
api_key = args.apikey
ddi = args.ddi
region = args.region
security_uuid = args.securitygroup
network_uuid = args.network

token_return = Auth(user,api_key)
token = token_return.auth_call()

find_port_api(region, token)
list_and_refresh_by_securitygroup(region, token)
