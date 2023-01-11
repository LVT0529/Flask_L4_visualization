import requests
import time



try:
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(
        url= 'https://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members',
        headers=headers,
        verify=False,
        timeout=5,
        auth=('admin', '#ngkqns^ksG$LB')
    )


    print("1")
except:

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(
        url= 'https://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members',
        headers=headers,
        verify=False,
        timeout=5,
        auth=('afguest', 'dk#mSLBguest')
    )
