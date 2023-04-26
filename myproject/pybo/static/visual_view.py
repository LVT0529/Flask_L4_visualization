import requests, json
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.figure import Figure

import paramiko
import time



def wideip():
    response = requests.get("http://localhost:5000/wideip/a")
    data = response.json()
    return data

def pool():
    list = []
    response = requests.get("http://localhost:5000/pool/a")

    data = json.loads(response.json())

    return data

def wideip_ssh():
    # SSH 클라이언트 생성
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # SSH 접속 정보 설정
    hostname = '203.238.150.185'
    port = 22
    username = 'root'
    password = '#ngkqns^ksG$LB'


    # SSH 연결
    client.connect(hostname, port=port, username=username, password=password)

    transport = client.get_transport()
    if transport.is_active():
        print('SSH connection established successfully!')
    else:
        print('Failed to establish SSH connection!')


    # 명령어 실행
    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.1.2.1.1') # wideip list
    wideip_text = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.3.2.1.6') # wideip record type
    wideip_record = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.3.2.1.2') # wideip status
    wideip_status = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.1.2.1.4') # wideip enable
    wideip_en = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.1.2.1.5') # wideip LB mode
    wideip_lbmod = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.1.2.1.8') # wideip return code on failure status
    wideip_rcof = stdout.read().decode()


    result = []
    wideip_list = []


    wideip = wideip_text.split("\n")
    wideip_record = wideip_record.split("\n")
    wideip_status = wideip_status.split("\n")
    wideip_en = wideip_en.split("\n")
    wideip_lbmod = wideip_lbmod.split("\n")
    wideip_rcof = wideip_rcof.split("\n")


    for i in range(len(wideip)) :
        wideip_temp = wideip[i].split("STRING: /Common/")
        wideip_record_temp = wideip_record[i].split("INTEGER: ")
        wideip_status_temp = wideip_status[i].split("INTEGER: ")
        wideip_en_temp = wideip_en[i].split("INTEGER: ")
        wideip_lbmod_temp = wideip_lbmod[i].split("INTEGER: ")
        wideip_rcof_temp = wideip_rcof[i].split("INTEGER: ")

        if(wideip_temp[0] == ""):
            break
        else:
            wideip_record_temp = wideip_record_temp[1].split("(")
            wideip_status_temp = wideip_status_temp[1].split("(")
            wideip_en_temp = wideip_en_temp[1].split("(")
            wideip_lbmod_temp = wideip_lbmod_temp[1].split("(")
            wideip_rcof_temp = wideip_rcof_temp[1].split("(")



            result.append(wideip_temp[1])
            result.append(wideip_record_temp[0])
            result.append(wideip_status_temp[0])
            result.append(wideip_en_temp[0])
            result.append(wideip_lbmod_temp[0])
            result.append(wideip_rcof_temp[0])



            wideip_list.append(result)

            result = []


    # SSH 연결 종료
    client.close()

    return wideip_list
