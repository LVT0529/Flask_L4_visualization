import requests
from requests.auth import HTTPBasicAuth
import json
import time


def get_f5_pool_config(base_url, username, password):
    response = requests.get(

    url = f"{base_url}/mgmt/tm/ltm/pool",
    auth = HTTPBasicAuth(username, password),
    headers = {'Content-Type': 'application/json'},
    verify=False # 라이브러리의 SSL/TLS 인증서 검증 비활성화 보통 reuests 문은 SSL/TLS 인증 검사하나 인증서 없을시 오류 발 #ㄱ#
    )
    response.raise_for_status()#reuests 문 성공 확인 (200~299) 범위면 정상동작 그이상일시 예외 처리 진행
    return response.json()

def compare_pool_configs(config1, config2, base1_url, base2_url , username, password):
    pool_result = []
    config1_items = config1['items']
    config2_items = config2['items']
    num = 0
    true = 0
    #virstual server 수량 확인 및 비교 위한
    countpool1 = 0
    countpool2 = 0
    for a in config1_items :
        if "name" in a:
            countpool1 += 1


    for b in config2_items :
        if "name" in b:
            countpool2 += 1






    if countpool1 == countpool2 : #두개 SLB pool 수가 다르면 바로 num = -1값으로 출력 후 확인 필요 결과 출력
        for item1 in config1_items: #SLB1 virtual 서버 딕셔너리 슬라이싱 -> 슬라이싱을 해야 분리하여 조건문 확인 가능
            for item2 in config2_items: #SLB2 virtual 서버 딕셔너리 슬라이싱 -> 슬라이싱을 해야 분리하여 조건문 확인 가능
                if  ((item1['name'] == item2['name']) and 
                     (item1['loadBalancingMode'] == item2['loadBalancingMode']) and 
                     (item1['serviceDownAction'] == item2['serviceDownAction'])) : # 두개 SLB Virtual 서버 name 비교 -> 같으면 true 값 1부여
                    monitorcout1 = 0          
                    monitorcout2 = 0
                    #Health Monitors 유무 및 동일 한지 확인                                       
                    if "monitor" in item1:
                        monitorcout1 += 1

                    if "monitor" in item2:
                        monitorcout2 += 1
                    if ((((monitorcout1 == 1) and(monitorcout2 == 1)) and (item1['monitor'] == item2['monitor'])) or 
                       ((monitorcout1 == 0) and (monitorcout2 == 0))
                       ):
                        def get_f5_poolnode_config(base_url,username, password, pool_members): #pool members 확인을 위한 이중 함수
                            response = requests.get(

                            url = f"{base_url}/mgmt/tm/ltm/pool/{pool_members}/members",
                            auth = HTTPBasicAuth(username, password),
                            headers = {'Content-Type': 'application/json'},
                            verify=False # 라이브러리의 SSL/TLS 인증서 검증 비활성화 보통 reuests 문은 SSL/TLS 인증 검사하나 인증서 없을시 오류 발 #ㄱ#
                            )
                            response.raise_for_status()#reuests 문 성공 확인 (200~299) 범위면 정상동작 그이상일시 예외 처리 진행
                            return response.json()

                        pool1_node = get_f5_poolnode_config(base1_url,username, password,item1['name']) # https://211.33.123.75/mgmt/tm/ltm/pool/pool/members

                        pool2_node = get_f5_poolnode_config(base2_url,username, password,item2['name']) # https://211.33.123.75/mgmt/tm/ltm/pool/pool/members

                        def compare_poolnode_configs (config1_pool_node,config2_pool_node): #pool node member 설정값(ip, service port) 확인
                            config1_items = config1_pool_node['items']
                            config2_items = config2_pool_node['items']

                            membercount = 0
                            #virstual server 수량 확인 및 비교 위한
                            countpoolnode1 = 0
                            countpoolnode2 = 0
                            for a in config1_items :
                                if "name" in a:
                                    countpoolnode1 += 1
                            for b in config2_items :
                                if "name" in b:
                                    countpoolnode2 += 1

                            if (countpoolnode1 == 0) and (countpoolnode2 == 0) : #members 서로가 없는경우도 동일하다고 보기
                                membercount += 1

                            if countpoolnode1 == countpoolnode2 :
                                for item1 in config1_items:
                                    for item2 in config2_items:
                                        if item1['name'] == item2['name'] :
                                            membercount += 1
                            return membercount

                        true = compare_poolnode_configs (pool1_node, pool2_node)

            f = open("SLB Comparison.txt", "a")
            #if true >= 1 :
                #pool_result.append(f"Configuration for {item1['name']} is the same.")

            if true == 0 :
                pool_result.append(f"Configuration for {item1['name']} is different.")
                num = num+1
            true = 0
            f.close()
    else: #다르면 num -1 값 부
        # Extract names from config1_items
        names_config1 = [item['name'] for item in config1_items if 'name' in item]

        # Extract names from config2_items
        names_config2 = [item['name'] for item in config2_items if 'name' in item]

        # Compare and add missing names from config1 to pool_result
        for name in names_config1:
            if name not in names_config2:
                pool_result.append(f"standby 장비에 {name} Pool이 없음")
                
        # Compare and add missing names from config2 to pool_result
        for name in names_config2:
            if name not in names_config1:
                pool_result.append(f"active 장비에 {name} Pool이 없음")
        num = -1


    return num, pool_result
