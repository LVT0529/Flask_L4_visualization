import requests
from requests.auth import HTTPBasicAuth
import json
import time


def get_f5_node_config(base_url, username, password):
    response = requests.get(

    url = f"{base_url}/mgmt/tm/ltm/node",
    auth = HTTPBasicAuth(username, password),
    headers = {'Content-Type': 'application/json'},
    verify=False # 라이브러리의 SSL/TLS 인증서 검증 비활성화 보통 reuests 문은 SSL/TLS 인증 검사하나 인증서 없을시 오류 발 #ㄱ#
    )
    response.raise_for_status()#reuests 문 성공 확인 (200~299) 범위면 정상동작 그이상일시 예외 처리 진행
    return response.json()


def compare_node_configs(config1, config2):
    node_result = []
    config1_items = config1['items']
    config2_items = config2['items']
    num = 0
    true = 0
    #virstual server 수량 확인 및 비교 위한
    countnode1 = 0
    countnode2 = 0
    for a in config1_items :
        if "name" in a:
            countnode1 += 1


    for b in config2_items :
        if "name" in b:
            countnode2 += 1


    if countnode1 == countnode2 : #두개 SLB Virtaul server 수가 다르면 바로 num = -1값으로 출력 후 확인 필요 결과 출력
        for item1 in config1_items: #SLB1 virtual 서버 딕셔너리 슬라이싱 -> 슬라이싱을 해야 분리하여 조건문 확인 가능
            for item2 in config2_items: #SLB2 virtual 서버 딕셔너리 슬라이싱 -> 슬라이싱을 해야 분리하여 조건문 확인 가능
                if  ((item1['name'] == item2['name'])  and (item1['address'] == item2['address']) and (item1['session'] == item2['session'])) : # 두개 SLB Virtual 서버 name 비교 -> 같으면 true 값 1부여
                    true += 1
            
            #if true == 1 :
                #node_result.append(f"Configuration for {item1['name']} is the same.")
            if true == 0 :
                node_result.append(f"Configuration for {item1['name']} is different.")
                num = num+1
            true = 0
            
    else: #다르면 num -1 값 부
        names_config1 = [item['name'] for item in config1_items if 'name' in item]

        # Extract names from config2_items
        names_config2 = [item['name'] for item in config2_items if 'name' in item]

        # Compare and add missing names from config1 to node_result
        for name in names_config1:
            if name not in names_config2:
                node_result.append(f"standby 장비에 {name} Node가 없음")
                
        # Compare and add missing names from config2 to node_result
        for name in names_config2:
            if name not in names_config1:
                node_result.append(f"active 장비에 {name} Node가 없음")
        num = -1
    
    return num, node_result
