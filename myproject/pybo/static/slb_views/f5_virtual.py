import requests
from requests.auth import HTTPBasicAuth
import json
import time


def get_f5_virtual_config(base_url, username, password):
    response = requests.get(

    url = f"{base_url}/mgmt/tm/ltm/virtual",
    auth = HTTPBasicAuth(username, password),
    headers = {'Content-Type': 'application/json'},
    verify=False # 라이브러리의 SSL/TLS 인증서 검증 비활성화 보통 reuests 문은 SSL/TLS 인증 검사하나 인증서 없을시 오류 발 #ㄱ#
    )
    response.raise_for_status()#reuests 문 성공 확인 (200~299) 범위면 정상동작 그이상일시 예외 처리 진행
    return response.json()

def compare_virtual_configs(config1, config2, url1, url2, username, password):
    virtual_result = []
    config1_items = config1['items']
    config2_items = config2['items']
    num = 0
    true = 0
    #virstual server 수량 확인 및 비교 위한
    countvirtual1 = 0
    countvirtual2 = 0
    for a in config1_items :
        if "name" in a:
            countvirtual1 += 1


    for b in config2_items :
        if "name" in b:
            countvirtual2 += 1

    base_url1 = url1
    base_url2 = url2
    if countvirtual1 == countvirtual2 : #두개 SLB Virtaul server 수가 다르면 바로 num = -1값으로 출력 후 확인 필요 결과 출력
        for item1 in config1_items: #SLB1 virtual 서버 딕셔너리 슬라이싱 -> 슬라이싱을 해야 분리하여 조건문 확인 가능
            for item2 in config2_items: #SLB2 virtual 서버 딕셔너리 슬라이싱 -> 슬라이싱을 해야 분리하여 조건문 확인 가능
                if  (item1['name'] == item2['name']  and
                    ((("enabled" in item1) and ("enabled" in item2)) or (("disabled" in item1) and ("disabled" in item2))) and # virtaul서버 disable enabled 확
                    item1['destination'] == item2['destination'] and# VIP 및 포트 정보 비교
                    item1['poolReference'] == item2['poolReference'] and  # virtrual 서버 Default Pool 이 같은지 확인
                    item1['mirror'] == item2['mirror'] and # connection miiror 확인
                    item1['translateAddress'] == item2['translateAddress'] and # translateaddress 확
                    item1['translatePort'] == item2['translatePort'] #translateport 확인
                    ) : # 두개 SLB Virtual 서버 name 비교 같으면 Protocol Profile 비교
                    
                    def get_f5_virtual_profile(base_url, profilehost, username, password):
                        response = requests.get(
                        url = f"{base_url}/mgmt/tm/ltm/virtual/~Common~{profilehost}/profiles",
                        auth = HTTPBasicAuth(username, password),
                        headers = {'Content-Type': 'application/json'},
                        verify=False # 라이브러리의 SSL/TLS 인증서 검증 비활성화 보통 reuests 문은 SSL/TLS 인증 검사하나 인증서 없을시 오류 발 #ㄱ#
                        )
                        response.raise_for_status()#reuests 문 성공 확인 (200~299) 범위면 정상동작 그이상일시 예외 처리 진행
                        
                        return response.json()
                    virtual1_profile = get_f5_virtual_profile(base_url1, item1['name'], username, password)
                    virtual2_profile = get_f5_virtual_profile(base_url2, item2['name'], username, password)

                    def compare_virtual_profile(virtual1_profile, virtual2_profile):
                        profilecount = 0
                        profile_config1_items = virtual1_profile['items']
                        profile_config2_items = virtual2_profile['items']
                                              
                        
                        for item1 in profile_config1_items:
                            for item2 in profile_config2_items:
                                if item1['name'] == item2['name']:
                                    profilecount += 1
           
                        return profilecount


                    true = compare_virtual_profile(virtual1_profile, virtual2_profile)
            f = open("test.txt", "a")
            #if true == 1 :
                #virtual_result.append(f"Configuration for {item1['name']} is the same." )
            if true == 0 :
                virtual_result.append(f"Configuration for {item1['name']} is different.")
                num = num+1
            true = 0
            f.close()
            
    else: #다르면 num -1 값 부여
        # Extract names from config1_items
        names_config1 = [item['name'] for item in config1_items if 'name' in item]

        # Extract names from config2_items
        names_config2 = [item['name'] for item in config2_items if 'name' in item]

        # Compare and add missing names from config1 to virtual_result
        for name in names_config1:
            if name not in names_config2:
                virtual_result.append(f"standby 장비에 {name} Virtual Server가 없음")
                
        # Compare and add missing names from config2 to virtual_result
        for name in names_config2:
            if name not in names_config1:
                virtual_result.append(f"active 장비에 {name} Virtual Server가 없음")
        num = -1



    return num, virtual_result
