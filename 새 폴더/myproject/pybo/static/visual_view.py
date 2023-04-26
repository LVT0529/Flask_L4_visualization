import requests, json
import os
import sys


ASADMIN = 'asadmin'




if sys.argv[-1] != ASADMIN:
    url_test = 'https://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members'
    username = 'afguest'
    password = 'dk#mSLBguest'


    response = requests.get(url = url_test, verify = False, timeout=10, auth=(username, password) )

    sys.exit(0)
