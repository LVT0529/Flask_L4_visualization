import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import TRS01_SW, TRS02_SW, TRS03_SW, TRS04_SW, TRS05_SW, TRS06_SW, TRS07_SW, TRS08_SW, TRS09_SW, TRS10_SW, TRS11_SW, TRS12_SW, TRS13_SW, TRS14_SW, TRS15_SW, TRS16_SW, LastRefreshed
from pybo.static.sw_info import get_switch_info, get_switch_int_port_status, serialize_sw, get_gw_arp_info
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import requests
from datetime import datetime


bp = Blueprint('switch', __name__, url_prefix='/') #폴더
@bp.route('/info/', methods=('GET', 'POST'))
def info():  # 처음 실행시 보여지는 HTML 화면
    #DB 마지막 리프레쉬 시간 출력 문구
    last_refreshed = LastRefreshed.query.first()
    if last_refreshed:
        current_time = last_refreshed.time.strftime('%Y/%m/%d %H:%M')
    else:
        current_time = "Never"  
   
    return render_template('switch/info.html', current_time=current_time) #'(폴터)/"해당 html"



@bp.route('/info/DB', methods=('GET', 'POST'))
def _info_DB():
    #GW 장비에서 arp 정보 수집
    gw_username = "admin"
    gw_password = "^kavud1ekswl!@"
    TR_url = "https://175.126.72.254/ins"
    #test_url = "https://110.10.216.77/ins"
    
    TR_arp_data = get_gw_arp_info(TR_url, gw_username, gw_password)
    #test_arp_data = get_gw_arp_info(test_url, gw_username, gw_password)

    #TOR 장비에서 interface status, mac 정보 수집
    urlist = [
        ("https://175.126.72.241/ins", TRS01_SW),
        ("https://175.126.72.242/ins", TRS02_SW),
        ("https://175.126.72.243/ins", TRS03_SW),
        ("https://175.126.72.244/ins", TRS04_SW),
        ("https://175.126.72.245/ins", TRS05_SW),
        ("https://175.126.72.246/ins", TRS06_SW),
        ("https://175.126.72.247/ins", TRS07_SW),
        ("https://114.207.114.123/ins", TRS08_SW),
        ("https://114.207.114.124/ins", TRS09_SW),
        ("https://114.207.114.122/ins", TRS10_SW),
        ("https://175.126.72.248/ins", TRS11_SW),        
        ("https://175.126.72.249/ins", TRS12_SW),
        ("https://175.126.72.250/ins", TRS13_SW),
        ("https://175.126.72.251/ins", TRS14_SW),
        ("https://175.126.72.252/ins", TRS15_SW),
        ("https://211.33.88.245/ins", TRS16_SW),
        
    ]


    try:
        hosts_path = '/etc/hosts'  # 리눅스에서의 hosts 파일 위치
        with open(hosts_path, 'r') as f:
            lines = f.readlines()
            
            hosts_result = []
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:  # IP 주소와 호스트명 둘 다 있는 경우에만 처리
                    ip = parts[0]
                    hostname = parts[1]
                    hosts_result.append({ip: hostname})

            

    except Exception as e:
        print("Error:", str(e))


    for url, SwitchModel in urlist:
        username = "admin"
        password = "^kavud1ekswl!@"
        switch_interface_data, switch_mac_data, switch_description_data = get_switch_info(url, username, password)  # 스위치show int status 기준 json 파일 수집
        int_port, int_status, int_vlan, int_speed, int_type, int_mac, int_ip, int_Host = get_switch_int_port_status(switch_interface_data, switch_mac_data, switch_description_data, TR_arp_data, hosts_result)
        # NX-API로 데이터 수집 후 DB 데이터에 입력하는 과정
        for i in range(len(int_port)):
            sw_instance = SwitchModel.query.get(i + 1)

            if sw_instance:  # If record with id (i+1) exists, update it. 만약 DB에 데이터가 있으면 덮어쓰기
                sw_instance.Interface = int_port[i]
                sw_instance.Status = int_status[i]
                sw_instance.Vlan = int_vlan[i]
                sw_instance.Speed = int_speed[i]
                sw_instance.Type = int_type[i]
                sw_instance.Mac = int_mac[i]
                sw_instance.IP = int_ip[i]
                sw_instance.Host = int_Host[i]
                
            else: #DB 데이터 있을 경우 새로운 데이터로 덮어쓰기 코드
                comment = SwitchModel(
                    id=i + 1, Interface=int_port[i],Host= int_Host[i], IP=int_ip[i],Mac=int_mac[i] , Status=int_status[i], Vlan=int_vlan[i], Speed=int_speed[i], Type=int_type[i]
                )
                db.session.add(comment)
        
       
        current_time = datetime.now() #현재 DB 저장 데이터시간
        last_refreshed = LastRefreshed.query.first() #refresh된 시간 저장

        if last_refreshed:
            last_refreshed.time = current_time
        else:
            new_record = LastRefreshed(time=current_time)
            db.session.add(new_record)
        db.session.commit()
    return render_template('switch/info_DB.html')



@bp.route('/info/result', methods=('GET', 'POST'))
def _info_result(): #DB데이터를 받아서 리스트 딕셔너리 형태로 가공 함수 [{Key : value ....}]
    #DB 마지막 리프레쉬 시간 출력 문구
    last_refreshed = LastRefreshed.query.first()
    if last_refreshed:
        current_time = last_refreshed.time.strftime('%Y/%m/%d %H:%M')
    else:
        current_time = "Never"  

    #==========================================================================
    table_map = {
    'TRS01_SW': TRS01_SW,    
    'TRS02_SW': TRS02_SW,
    'TRS03_SW': TRS03_SW,   
    'TRS04_SW': TRS04_SW,
    'TRS05_SW': TRS05_SW,    
    'TRS06_SW': TRS06_SW,    
    'TRS07_SW': TRS07_SW,    
    'TRS08_SW': TRS08_SW,    
    'TRS09_SW': TRS09_SW,
    'TRS10_SW': TRS10_SW,   
    'TRS11_SW': TRS11_SW,  
    'TRS12_SW': TRS12_SW,
    'TRS13_SW': TRS13_SW,   
    'TRS14_SW': TRS14_SW,
    'TRS15_SW': TRS15_SW,
    'TRS16_SW': TRS16_SW
    # 추가적으로 다른 테이블들도 여기에 추가 가능
    }

    
    devices = []  
    if request.method == 'POST':
        devices = request.form.getlist('device')  # 체크박스의 값들을 가져옴

    all_sw_data = []
    numRows = []
    '''
    for sw_table_name in devices:
        sw_table = table_map.get(sw_table_name)
        if sw_table:
            all_sw_data.extend(sw_table.query.all())
    print(all_sw_data)
    
    for a in all_sw_data:
        print(a) 
    print(serialized_data)
    '''
    for sw_table_name in devices:
        sw_table = table_map.get(sw_table_name) 
        if sw_table:
            sw_data = sw_table.query.all() 
            row = len(sw_data)
            serialized_data = [serialize_sw(item) for item in sw_data]
            numRows.append(row)
            all_sw_data.append(serialized_data)  

    

    
    
    
    return render_template('switch/info_result.html', data=all_sw_data, numRows=numRows, devices_name = devices, current_time=current_time)
    

