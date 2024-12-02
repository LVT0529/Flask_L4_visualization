import requests
from requests.auth import HTTPBasicAuth
import json
import time
import requests
import re


def get_gw_arp_info(base_url, username, password):
    headers = {
    'Content-Type': 'application/json',
    }

    payload = {
        "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",  # Do not chunk results
        "sid": "1",   # Session ID
        "input": "show ip arp",
        "output_format" : "json"
    }
    }
    
    response = requests.post(base_url, headers=headers, data=json.dumps(payload), auth=(username, password), verify=False)
    sh_ip_arp_data = response.json()
    sh_ip_arp_data1 = sh_ip_arp_data['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['TABLE_adj']['ROW_adj'] # ins_api 안에 output 안에 ....ROW_interfect 정보만 가져오기 위한 코드
    return sh_ip_arp_data1



def get_switch_info(base_url, username, password):
    headers = {
    'Content-Type': 'application/json',
    }

    payload = {
        "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",  # Do not chunk results
        "sid": "1",   # Session ID
        "input": "show interface status",
        "output_format" : "json"
    }
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(payload), auth=(username, password), verify=False)
    sh_int_status_data = response.json()
    sh_int_status_data1 = sh_int_status_data['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface'] # ins_api 안에 output 안에 ....ROW_interfect 정보만 가져오기 위한 코드
    #print(sh_int_status_data1)

    payload = {
        "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",  # Do not chunk results
        "sid": "1",   # Session ID
        "input": "show interface description",
        "output_format" : "json"
    }
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(payload), auth=(username, password), verify=False)
    sh_int_description_data = response.json()
    sh_int_description_data1 = sh_int_description_data['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface'] # ins_api 안에 output 안에 ....ROW_interfect 정보만 가져오기 위한 코드
    #print(sh_int_description_data1)
    
    payload = {
        "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",  # Do not chunk results
        "sid": "1",   # Session ID
        "input": "show mac address-table ",
        "output_format" : "json"
    }
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(payload), auth=(username, password), verify=False)
    sh_mac_address_data = response.json()
    sh_mac_address_data1 = sh_mac_address_data['ins_api']['outputs']['output']['body']['TABLE_mac_address']['ROW_mac_address'] # ins_api 안에 output 안에 ....ROW_interfect 정보만 가져오기 위한 코드
    #print(sh_mac_address_data1)
    return sh_int_status_data1, sh_mac_address_data1, sh_int_description_data1





# JSONE 형태의 포트정보(sh int status), 포트 MAC 정보(sh mac address) 데이터 가공
def get_switch_int_port_status(int_status_data, int_mac_data, int_description_data, TR_arp_data, hosts_result):
    interface = []
    state =[] 
    vlan =[]
    speed =[]
    type =[]
    mac=[]
    ip=[]
    host=[]

    

    for item in int_status_data:
        
        interface.append(item.get('interface', ' ')) 
        state.append(item.get('state', ' ')) 
        vlan.append(item.get('vlan', ' ')) 
        speed.append(item.get('speed', ' '))
        type.append(item.get('type', ' ')) 
    
    words_to_filter = ["Vlan", "mgmt"] 

    removed_indices = [index for index, item in enumerate(interface) if any(word in item for word in words_to_filter)]#특정 단어 포함된 원소 위치 확인
    #print(f"Indices of elements that were removed: {removed_indices}")


    interface = [item for item in interface if not any(word in item for word in words_to_filter)] 
    state = [state[i] for i in range(len(state)) if i not in removed_indices] 
    vlan = [vlan[i] for i in range(len(vlan)) if i not in removed_indices] 
    speed = [speed[i] for i in range(len(speed)) if i not in removed_indices]
    type = [type[i] for i in range(len(type)) if i not in removed_indices] 
    
         
    for intf in interface:
        # 'Ethernet'을 '(Ethernet|Eth)'로, 'Port-channel'을 '(Port-channel|Po)'로 대체합니다. (import re)
        pattern = re.sub(r'Ethernet', r'(Ethernet|Eth)', intf)
        pattern = re.sub(r'port-channel', r'(Port-channel|port-channel|Po)', pattern)
        pattern += '$'
        mac_addr = next((item['disp_mac_addr'] for item in int_mac_data if re.match(pattern, item['disp_port'])), None)
        

        if mac_addr:
            mac.append(mac_addr)
        else:
            mac.append('')
        

    for mac_addr in mac:
        mac_addr_cleaned = mac_addr.strip()
        if mac_addr_cleaned:
            # TR_arp_data 또는 test_arp_data에서 일치하는 항목을 찾기 위해 제너레이터 표현식을 사용합니다.
            matching_entry = next((entry for entry in TR_arp_data if 'mac' in entry and entry['mac'] == mac_addr_cleaned), None)
            #if not matching_entry:
                #matching_entry = next((entry for entry in test_arp_data if 'mac' in entry and entry['mac'] == mac_addr_cleaned), None)
              
           
            if matching_entry:
                ip.append(matching_entry['ip-addr-out'])
            else:
                ip.append('')
        else:
            ip.append('')
          
        


    

    hosts_dict = {k: v for entry in hosts_result for k, v in entry.items()}


    for intf in interface:
        desc_data = next((item for item in int_description_data if item["interface"] == intf), None)
        if desc_data and "desc" in desc_data:
            host.append(desc_data["desc"])
        else:
            host.append("")
    # IP 리스트를 순회하며 각 IP에 대한 처리
    for idx, ip_temp in enumerate(ip):
        if ip_temp and host[idx] == "":  
            # IP에 해당하는 host 값을 찾아 hosts의 해당 인덱스에 저장
            host[idx] = hosts_dict.get(ip_temp, 'Gateway')
    #print(host)

    return interface, state, vlan, speed, type, mac, ip, host





def serialize_sw(sw_instance): 
    """Serialize a SW instance into a dictionary, using '-' for missing data."""

    return {
        'Interface': sw_instance.Interface or '-',
        'Mac': getattr(sw_instance, 'Mac', '-'), 
        'IP': getattr(sw_instance, 'IP', '-'),
        'Host': getattr(sw_instance, 'Host', '-'),
        'Status': sw_instance.Status or '-',
        'Vlan': sw_instance.Vlan or '-',
        'Speed': sw_instance.Speed or '-',
        'Type': sw_instance.Type or '-'
    }

