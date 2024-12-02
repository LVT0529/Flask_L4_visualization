## 엑셀 관련 라이브러리
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill, Font
import openpyxl
import datetime
import operator
import time
import os
import re
import sys

def sconfig_report(file):

    sconfig = openpyxl.load_workbook(file)
    sconfig = sconfig.active

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'SLB config'

    sheet['A2'] = "monitor"

    skip_list = ['monitor', 'monitor 이름', 'node', 'node 이름', 'pool', 'pool 이름', 'virtual', 'virtual 이름']

    for i in range(1,200):
        if (sconfig['A' + str(i)].value == None):
            continue
        elif (sconfig['A' + str(i)].value in skip_list):
            if(sconfig['A' + str(i)].value == 'monitor'):
                session = 'monitor'
            elif(sconfig['A' + str(i)].value == 'node'):
                sheet['A' + str(i)] = "node"
                session = 'node'
            elif(sconfig['A' + str(i)].value == 'pool'):
                sheet['A' + str(i)] = "pool"
                session = 'pool'
            elif(sconfig['A' + str(i)].value == 'virtual'):
                sheet['A' + str(i)] = "virtual"
                session = 'virtual'
            continue
        else:
            temp = ""
            if(session == 'monitor'):
                monitor_name = sconfig['A' + str(i)].value
                s_port = sconfig['B' + str(i)].value
                vip = sconfig['C' + str(i)].value
                config = "create ltm monitor tcp-half-open " +  monitor_name + "_" + str(s_port) + \
                         "_half interval 5 timeout 16 transparent enabled destination " + str(vip) + ":" + str(s_port)

            elif(session == 'node'):
                node_name = sconfig['A' + str(i)].value
                ip = sconfig['B' + str(i)].value
                config = "create ltm node "+ node_name + " address " + str(ip) + " session user-disabled description " + node_name

            elif(session == 'pool'):
                pool_name = sconfig['A' + str(i)].value
                pool_member = sconfig['B' + str(i)].value
                monitor_name = sconfig['C' + str(i)].value
                s_port = sconfig['D' + str(i)].value

                pool_name_t = pool_name.split("_")
                pool_member = pool_member.split("~")
                start = re.sub(r'[^0-9]', "", pool_member[0])

                for k in range(int(start), int(pool_member[1])+1):
                    temp += pool_name_t[1] + str(k) + ":" + str(s_port) + " "

                config = "create ltm pool "+ pool_name + "_" + str(s_port) + " members add { " + \
                          temp + "} monitor " + monitor_name + "_" + str(s_port) + "_half and tcp_half_open load-balancing-mode round-robin"

            elif(session == 'virtual'):
                virtual_name = sconfig['A' + str(i)].value
                pool_member = sconfig['B' + str(i)].value
                vip = sconfig['C' + str(i)].value
                s_port = sconfig['D' + str(i)].value

                config = "create ltm virtual " + virtual_name + "_" + str(s_port) + "_vs destination " + str(vip) + ":" + str(s_port) + \
                         " ip-protocol tcp mirror enabled pool " + virtual_name + "_" + str(s_port) + " translate-address disabled " + \
                         "translate-port disabled description " + pool_member + " profiles add { fastL4_change }"

            sheet['A' + str(i-1)] = config

    nowdate = datetime.datetime.now()

    print("Make Max_sort Excel....... ")
    wb.save(nowdate.strftime("%m-%d") + ' CLI config Report.xlsx')

