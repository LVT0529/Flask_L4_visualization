import requests, json
import os
import sys

from flask import request

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.figure import Figure

import paramiko
import time
import re



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



    # wideip 속성
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
    wideippool_mapp = []



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

            if(wideip_lbmod_temp[0] == 'ga'):
                wideip_lbmod_temp[0] = 'global availability'

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

def widepool_ssh():
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


        # wideip, pool 맵핑
        stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.5.2.1.1') # wideip
        widepool_wideip = stdout.read().decode()

        stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.5.2.1.2') # pool
        widepool_pool = stdout.read().decode()

        stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.5.2.1.4') # ratio
        widepool_ratio = stdout.read().decode()

        stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.12.5.2.1.3') # pool_order
        widepool_order = stdout.read().decode()

        result = []
        wideippool_mapp = []



        widepool_wideip = widepool_wideip.split("\n")
        widepool_pool = widepool_pool.split("\n")
        widepool_ratio = widepool_ratio.split("\n")
        widepool_order = widepool_order.split("\n")


        for i in range(len(widepool_wideip)):
            widepool_wideip_temp = widepool_wideip[i].split("STRING: /Common/")
            widepool_pool_temp = widepool_pool[i].split("STRING: /Common/")
            widepool_ratio_temp = widepool_ratio[i].split("INTEGER: ")
            widepool_order_temp = widepool_order[i].split("INTEGER: ")

            if(widepool_wideip_temp[0] == ""):
                break
            else:
                widepool_wideip_temp = widepool_wideip_temp[1].split("(")
                widepool_pool_temp = widepool_pool_temp[1].split("(")
                widepool_ratio_temp = widepool_ratio_temp[1].split("(")
                widepool_order_temp = widepool_order_temp[1].split("(")

                result.append(widepool_wideip_temp[0])
                result.append(widepool_pool_temp[0])
                result.append(widepool_ratio_temp[0])
                result.append(widepool_order_temp[0])

                wideippool_mapp.append(result)

                result = []

        # SSH 연결 종료
        client.close()

        return wideippool_mapp

def pool_ssh():
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

    # pool 속성
    # wideip, pool 맵핑
    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.1') # pool list
    pool_list = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.2') # pool_ttl
    pool_ttl = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.3.2.1.2') # pool_status
    pool_status = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.3') # pool_enable
    pool_en = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.7') # pool_lbmod
    pool_lbmod = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.8') # pool_alternate
    pool_alter = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.9') # pool_fallback
    pool_fallback = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.4') # pool_availability check
    pool_avail = stdout.read().decode()

    result = []
    pool_mapp = []



    pool_list = pool_list.split("\n")
    pool_ttl = pool_ttl.split("\n")
    pool_status = pool_status.split("\n")
    pool_en = pool_en.split("\n")
    pool_lbmod = pool_lbmod.split("\n")
    pool_alter = pool_alter.split("\n")
    pool_fallback = pool_fallback.split("\n")
    pool_avail = pool_avail.split("\n")



    for i in range(len(pool_list)):
        pool_list_temp = pool_list[i].split("STRING: /Common/")
        pool_ttl_temp = pool_ttl[i].split("Gauge32: ")
        pool_status_temp = pool_status[i].split("INTEGER: ")
        pool_en_temp = pool_en[i].split("INTEGER: ")
        pool_lbmod_temp = pool_lbmod[i].split("INTEGER: ")
        pool_alter_temp = pool_alter[i].split("INTEGER: ")
        pool_fallback_temp = pool_fallback[i].split("INTEGER: ")
        pool_avail_temp = pool_avail[i].split("INTEGER: ")


        if(pool_list_temp[0] == ""):
            break
        else:
            pool_list_temp = pool_list_temp[1].split("(")
            pool_ttl_temp = pool_ttl_temp[1].split("(")
            pool_status_temp = pool_status_temp[1].split("(")
            pool_en_temp = pool_en_temp[1].split("(")
            pool_lbmod_temp = pool_lbmod_temp[1].split("(")
            pool_alter_temp = pool_alter_temp[1].split("(")
            pool_fallback_temp = pool_fallback_temp[1].split("(")
            pool_avail_temp = pool_avail_temp[1].split("(")

            result.append(pool_list_temp[0])
            result.append(pool_ttl_temp[0])
            result.append(pool_status_temp[0])
            result.append(pool_en_temp[0])
            result.append(pool_lbmod_temp[0])
            result.append(pool_alter_temp[0])
            result.append(pool_fallback_temp[0])
            result.append(pool_avail_temp[0])

            pool_mapp.append(result)

            result = []

    # SSH 연결 종료
    client.close()

    return pool_mapp

def poolpoolmbr_ssh():
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

    # pool 속성
    # wideip, pool 맵핑
    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.7.2.1.1') # pool list
    pool_list = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.7.2.1.9') # pool_mbr_list
    pool_mbr = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.4.2.1.21') # pool_mbr_ratio
    pool_mbr_ratio = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.4.2.1.6') # pool_mbr_order
    pool_mbr_order = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  1.3.6.1.4.1.3375.2.3.6.7.2.1.8') # pool_mbr_status
    pool_mbr_status = stdout.read().decode()

    #print (pool_mbr_status)


    result = []
    poolpoolmbr_mapp = []

    pool_list = pool_list.split("\n")
    pool_mbr = pool_mbr.split("\n")
    pool_mbr_ratio = pool_mbr_ratio.split("\n")
    pool_mbr_order = pool_mbr_order.split("\n")
    pool_mbr_status = pool_mbr_status.split("\n")


    for i in range(len(pool_list)):
        pool_list_temp = pool_list[i].split("STRING: /Common/")
        pool_mbr_temp = re.split("gtmPoolMbrStatusVsName|\"", pool_mbr[i])
        pool_mbr_ratio_temp = pool_mbr_ratio[i].split("INTEGER: ")
        pool_mbr_order_temp = pool_mbr_order[i].split("INTEGER: ")
        pool_mbr_status_temp = pool_mbr_status[i].split("STRING: ")



        if(pool_list_temp[0] == ""):
            break
        else:
            pool_list_temp = pool_list_temp[1].split("(")
            pool_mbr_ratio_temp = pool_mbr_ratio_temp[1].split("(")
            pool_mbr_order_temp = pool_mbr_order_temp[1].split("(")

            result.append(pool_list_temp[0])

            if(pool_mbr_temp[1] == '.a.'):
                pool_mbr_p = pool_mbr_temp[7].split("STRING: ")
                if(pool_mbr_p[1] == 'aflxchatbmtrds'):
                    result.append(pool_mbr_temp[6])
                else:
                    result.append(pool_mbr_p[1])

            elif(pool_mbr_temp[1] == '.cname.'):
                result.append(pool_mbr_temp[4])


            result.append(pool_mbr_ratio_temp[0])
            result.append(pool_mbr_order_temp[0])
            if( " Monitor" in pool_mbr_status_temp[1]):
                pool_mbr_status_temp_p = re.split("\(|:", pool_mbr_status_temp[1])
                if("timed out" in pool_mbr_status_temp_p[2]):
                    result.append(pool_mbr_status_temp_p[3])
                else:
                    result.append(pool_mbr_status_temp_p[2])

            else:
                pool_mbr_status_temp_p = pool_mbr_status_temp[1].split(":")
                if(len(pool_mbr_status_temp_p) > 1):
                    result.append(pool_mbr_status_temp_p[1])
                else:
                    result.append(pool_mbr_status_temp[1])


            poolpoolmbr_mapp.append(result)

            result = []

    # SSH 연결 종료
    client.close()

    return poolpoolmbr_mapp

def poolmbr_ssh():
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



    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.7.2.1.10') # pool_mbr_list
    pool_mbr_list = stdout.read().decode()





    result = []
    pool_mbr_mapp = []

    pool_mbr_list = pool_mbr_list.split("\n")
    pool_mbr_status = pool_mbr_status.split("\n")



    for i in range(len(pool_mbr_list)):
        pool_mbr_list_temp = re.split("gtmPoolMbrStatusServerName|\"", pool_mbr_list[i])
        pool_mbr_status_temp = pool_mbr_status[i].split("INTEGER: ")



        if(pool_mbr_status_temp[0] == ""):
            break
        else:
            pool_mbr_status_temp = pool_mbr_status_temp[1].split("(")


            if(pool_mbr_list_temp[1] == '.a.'):
                pool_mbr = pool_mbr_list_temp[7].split("STRING: /Common/")
                if(pool_mbr[1] == 'aflxchatbmtrds'):
                    result.append(pool_mbr_list_temp[6])
                else:
                    result.append(pool_mbr[1])

            elif(pool_mbr_list_temp[1] == '.cname.'):
                result.append(pool_mbr_list_temp[4])

            result.append(pool_mbr_status_temp[0])

            pool_mbr_mapp.append(result)

            result = []

    # SSH 연결 종료
    client.close()

    return pool_mbr_mapp
