import requests, json
import os
import sys

from flask import request


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

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.35') # pool_monitor
    pool_monitor = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.11.1.2.1.21') # vs_monitor
    vs_monitor = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.9.1.2.1.19') # vs_monitor
    s_monitor = stdout.read().decode()







    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.9.1.2.1.1') # vs_monitor
    server = stdout.read().decode()


    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.6.1.2.1.1') # pool_list
    pool = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.3.11.1.2.1.4') # virtualserver_list
    vs = stdout.read().decode()



    pool_monitor = pool_monitor.split("\n")
    vs_monitor = vs_monitor.split("\n")
    s_monitor = s_monitor.split("\n")
    pool = pool.split("\n")
    vs = vs.split("\n")
    server = server.split("\n")

    pool_mapp = []
    vs_mapp = []
    s_mapp = []
    result = []
    temp = []

    for i in range(len(pool)-1):
        pool_monitor_temp = pool_monitor[i].split("STRING: ")
        pool_temp = pool[i].split("STRING: /Common/")

        pool_monitor_temp = pool_monitor_temp[1].split("_")

        for k in range(len(pool_monitor_temp)):
            tem_split = pool_monitor_temp[k].split(" ")
            if(tem_split[0].isdigit() or tem_split[0] == "gwicmp"):
                temp.append(tem_split[0])

        result.append(pool_temp[1])
        result.append(temp)

        pool_mapp.append(result)
        #print(result)

        result = []
        temp = []

    for i in range(len(vs)-1):
        vs_monitor_temp = vs_monitor[i].split("STRING: ")
        vs_temp = vs[i].split("STRING: ")

        vs_monitor_temp = vs_monitor_temp[1].split("_")


        for k in range(len(vs_monitor_temp)):
            tem_split = vs_monitor_temp[k].split(" ")
            if(tem_split[0].isdigit() or tem_split[0] == "gwicmp"):
                temp.append(tem_split[0])

        result.append(vs_temp[1])
        result.append(temp)

        #print(result)

        vs_mapp.append(result)

        result = []
        temp = []

    for i in range(len(server)-1):
        s_monitor_temp = s_monitor[i].split("STRING:")
        server_temp = server[i].split("STRING: /Common/")

        s_monitor_temp = s_monitor_temp[1].split("_")

        for k in range(len(s_monitor_temp)):
            tem_split = s_monitor_temp[k].split(" ")
            if(tem_split[0].isdigit() or tem_split[0] == "gwicmp"):
                temp.append(tem_split[0])

        result.append(server_temp[1])
        result.append(temp)

        s_mapp.append(result)
        #print(result)
        result = []
        temp = []

    #print(s_mapp)

    result = []
    poolpoolmbr_mapp = []

    pool_list = pool_list.split("\n")
    pool_mbr = pool_mbr.split("\n")
    pool_mbr_ratio = pool_mbr_ratio.split("\n")
    pool_mbr_order = pool_mbr_order.split("\n")
    pool_mbr_status = pool_mbr_status.split("\n")

    monitor_temp = []


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


                if( 'aflxchatbmtrds' in pool_mbr_p[1]):
                    for l in range(len(s_mapp)):
                        if('aflxchatbmtrds' in s_mapp[l][0]):
                            monitor_temp = s_mapp[l][1]

                    result.append(pool_mbr_temp[6])
                    pool_mbr_ip = pool_mbr_temp[6].split("_")
                    result.append(pool_mbr_ip[len(pool_mbr_ip) - 1])

                else:
                    result.append(pool_mbr_p[1])
                    pool_mbr_ip = pool_mbr_p[1].split("_")
                    result.append(pool_mbr_ip[len(pool_mbr_ip) - 1])

                for k in range(len(vs_mapp)):
                    if( ((pool_mbr_temp[6] or pool_mbr_p[1])in vs_mapp[k] ) and (len(monitor_temp) == 0)):
                        monitor_temp = vs_mapp[k][1]


            elif(pool_mbr_temp[1] == '.cname.'):
                result.append(pool_mbr_temp[4])

                result.append("")
                monitor_temp = ""

            if(len(monitor_temp) == 0 ):
                for k in range(len(pool_mapp)):
                    if(pool_list_temp[0] in pool_mapp[k]):
                        monitor_temp = pool_mapp[k][1]


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
            result.append(monitor_temp)

            print(result)

            poolpoolmbr_mapp.append(result)

            result = []
            monitor_temp = ""
    

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

def slb_ssh(slb1, slb2, slb_pw):
    # SSH 클라이언트 생성
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # SSH 접속 정보 설정
    hostname = slb1
    port = 22
    username = 'root'
    password = slb_pw

    # SSH 연결
    client.connect(hostname, port=port, username=username, password=password)
    transport = client.get_transport()

    if transport.is_active():
        print('SSH connection established successfully!')
    else:
        print('Failed to establish SSH connection!')


    ##################Client 1#####################
    # SSH 클라이언트 생성
    client1 = paramiko.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # SSH 접속 정보 설정
    hostname = slb2
    port = 22
    username = 'root'
    password = slb_pw

    # SSH 연결
    client1.connect(hostname, port=port, username=username, password=password)
    transport = client1.get_transport()

    if transport.is_active():
        print('SSH connection established successfully!')
    else:
        print('Failed to establish SSH connection!')


    stdin, stdout, stderr = client.exec_command('snmpwalk -Os -c skdnzha -v 2c 127.0.0.1 1.3.6.1.4.1.3375.2.1.1.2.20.21') # pool list
    cpu1 = stdout.read().decode()



    stdin, stdout, stderr = client1.exec_command('snmpwalk -Os -c skdnzha -v 2c 127.0.0.1 1.3.6.1.4.1.3375.2.1.1.2.20.21') # pool list
    cpu2 = stdout.read().decode()

    cpu1 = cpu1.split("Gauge32: ")
    cpu2 = cpu2.split("Gauge32: ")

    print(cpu1)
    print(cpu2)


    cpu1 = int (cpu1[1])
    cpu2 = int (cpu2[1])
    low_cpu = 0

    if(cpu1 < cpu2):
        client1.close()
        low_cpu = cpu1
    else:
        client.close()
        client = client1
        low_cpu = cpu2

    if (low_cpu > 80):
        client.close()



    # pool 속성
    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.10.1.2.1.1') # pool list
    pool_list = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.10.13.2.1.2') # pool_mbr_list
    pool_status = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.10.1.2.1.3') # pool_mbr_ratio
    pool_vip = stdout.read().decode()




    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.5.3.2.1.1') # pool_mbr_order
    pool_node_list = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.5.3.2.1.19') # pool_mbr_status
    node_list = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.5.3.2.1.4') # pool_mbr_status
    node_port = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.5.3.2.1.3') # pool_mbr_status
    node_ip = stdout.read().decode()

    stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  .1.3.6.1.4.1.3375.2.2.5.6.2.1.5') # pool_mbr_status
    node_status = stdout.read().decode()



    #print (pool_mbr_status)


    result = []
    pool_mapp = []
    temp = []

    pool_list = pool_list.split("\n")
    pool_status = pool_status.split("\n")
    pool_vip = pool_vip.split("\n")


    for i in range(len(pool_list)-1):

        if(hostname in '121.125.76.126'):
            pool_list_temp = pool_list[i].split("STRING: ")
        else:
            pool_list_temp = pool_list[i].split("STRING: /Common/")
       
        #print(pool_list_temp) 


        pool_vip_temp = pool_vip[i].split("STRING: ")
        
    
        pool_status_temp = pool_status[i].split("INTEGER: ")
   

        dec_value = ""

        if(pool_list_temp[0] == ""):
            break
        else:
            pool_list_temp = pool_list_temp[1].split("_vs")

            if(hostname in '1.234.43.189' or hostname in '1.234.43.190'):
                temp = pool_list_temp[0].split("_")
                pool_list_temp[0] = temp[0] + "_" + temp[1] + "_" + temp[3]
                            

            pool_vip_temp = pool_vip_temp[1].split(" ")
            pool_status_temp = pool_status_temp[1].split("(")

            result.append(pool_list_temp[0])


            for k in range(len(pool_vip_temp)-1):
                dec_temp = int(pool_vip_temp[k], 16)
                dec_value += str(dec_temp)

                if( k < 3):
                    dec_value += "."

            result.append(dec_value)
            result.append(pool_status_temp[0])

            temp = pool_list_temp[0].split("_")
            print(temp)
            result.append(temp[0])
            result.append(temp[2])

            pool_mapp.append(result)
            result = []



    result = []
    pool_node_mapp = []

    pool_node_list = pool_node_list.split("\n")
    node_list = node_list.split("\n")
    node_port = node_port.split("\n")
    node_ip = node_ip.split("\n")
    node_status = node_status.split("\n")


    for i in range(len(pool_node_list)-1):

        if(hostname in '121.125.76.126'):
            pool_node_list_temp = pool_node_list[i].split("STRING: ")
            node_list_temp = node_list[i].split("STRING: ")
        else:
            pool_node_list_temp = pool_node_list[i].split("STRING: /Common/")
            node_list_temp = node_list[i].split("STRING: /Common/")

        #print(pool_node_list_temp)
        #print(node_list_temp)

        node_port_temp = node_port[i].split("Gauge32: ")
        node_ip_temp = node_ip[i].split("STRING: ")
        node_status_temp = node_status[i].split("INTEGER: ")

        

        dec_value = ""

        if(pool_node_list_temp[0] == ""):
            break
        else:
            node_ip_temp = node_ip_temp[1].split(" ")
            node_status_temp = node_status_temp[1].split("(")


            if(hostname in '1.234.43.189' or hostname in '1.234.43.190'):
                temp = pool_node_list_temp[1].split("_")
           
                if(temp[2] in "http"):
                    pool_node_list_temp[1] = temp[0] + "_" + temp[1] + "_" + "80"
                elif(temp[2] in "https"):
                    pool_node_list_temp[1] = temp[0] + "_" + temp[1] + "_" + "443"


            result.append(pool_node_list_temp[1])
            result.append(node_list_temp[1])
            result.append(node_port_temp[1])

            for k in range(len(node_ip_temp)-1):
                dec_temp = int(node_ip_temp[k], 16)
                dec_value += str(dec_temp)

                if( k < 3):
                    dec_value += "."

            result.append(dec_value)
            result.append(node_status_temp[0])

            #print(result)

            pool_node_mapp.append(result)
            result = []
            

    # SSH 연결 종료
    client.close()
    client1.close()
    
    #print(pool_mapp)
    #print(pool_node_mapp)

    return pool_mapp, pool_node_mapp

