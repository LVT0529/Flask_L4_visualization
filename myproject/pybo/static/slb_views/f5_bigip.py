import requests
from requests.auth import HTTPBasicAuth
import json
import time


def get_bigip_conf(base_url, username, password):
    # Authenticate and obtain a token
    auth_url = f'{base_url}/mgmt/shared/authn/login'
    auth_payload = {
        "username": username,
        "password": password,
        "loginProviderName": "tmos"
    }

    response = requests.post(auth_url, json=auth_payload, verify=False)
    response.raise_for_status()
    token = response.json()['token']['token']

    # Define headers with the obtained token
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }

    # Execute the bash command to fetch the bigip.conf content
    bash_url = f'{base_url}/mgmt/tm/util/bash'
    bash_payload = {
        "command": "run",
        "utilCmdArgs": "-c 'cat /config/bigip.conf'"
    }

    response = requests.post(bash_url, headers=headers, json=bash_payload, verify=False)
    response.raise_for_status()
    bigip_conf_content = response.json()['commandResult']

    return bigip_conf_content

def remove_passphrase(data): #간혹 SLB Conf 파일에 ssl (passphrase) 값이 있어 해당 행 제거 해주기 위한 문구
    lines = data.split('\n')
    filtered_lines = [line for line in lines if 'passphrase' not in line]
    return '\n'.join(filtered_lines)


