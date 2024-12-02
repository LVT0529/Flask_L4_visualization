import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User
from pybo.static.slb_views.f5_bigip import get_bigip_conf, remove_passphrase
from pybo.static.slb_views.f5_virtual import compare_virtual_configs, get_f5_virtual_config 
from pybo.static.slb_views.f5_pool import compare_pool_configs, get_f5_pool_config
from pybo.static.slb_views.f5_node import compare_node_configs, get_f5_node_config
import requests
from requests.auth import HTTPBasicAuth
import json
import time

bp = Blueprint('slb', __name__, url_prefix='/') #폴더
@bp.route('/sync/', methods=('GET', 'POST')) #html
def sync():  # 처음 실행시 보여지는 HTML 화면
    
    return render_template('slb/sync.html') #'(폴터)/"해당 html"


@bp.route('/sync/result', methods=('GET', 'POST')) #html
def _sync_result():
    device = request.form.get('slbip')
    print(device)


    f5_device1_username = "admin"
    f5_device2_username = "admin"
    if device == "118.217.182.253" or device == "118.217.182.254": #afreecaslb1-2
        f5_device1_url = "https://118.217.182.253"
        f5_device2_url = "https://118.217.182.254"
        f5_device1_password = "#ngkqns^ks5fm$lb"
        f5_device2_password = "#ngkqns^ks5fm$lb"
        SLBname = "afreecaslb1-2"
    elif device == "118.218.124.251" or device == "118.218.124.252": #afmainslb1-2
        f5_device1_url = "https://118.218.124.251"
        f5_device2_url = "https://118.218.124.252"
        f5_device1_password = "#ngkqns^ks5fm$lb"
        f5_device2_password = "#ngkqns^ks5fm$lb"
        SLBname = "afmainslb1-2"
    elif device == "121.125.76.125" or device == "121.125.76.125": #nowlximgslb1-2
        f5_device1_url = "https://121.125.76.125"
        f5_device2_url = "https://121.125.76.126"
        f5_device1_password = "#ngkqns^ks5fi$lb"
        f5_device2_password = "#ngkqns^ks5fi$lb"
        SLBname = "nowlximgslb1-2"
    elif device == "211.49.227.251" or device == "211.49.227.252": #AFAHVSLB1-2
        f5_device1_url = "https://211.49.227.251"
        f5_device2_url = "https://211.49.227.252"
        f5_device1_password = "#ngkqns^ksAHV$lb"
        f5_device2_password = "#ngkqns^ksAHV$lb"
        SLBname = "AFAHVSLB1-2"
    elif device == "211.49.227.249" or device == "211.49.227.250": #AFAHVSLB3-4
        f5_device1_url = "https://211.49.227.249"
        f5_device2_url = "https://211.49.227.250"
        f5_device1_password = "#ngkqns^ksAHV$lb"
        f5_device2_password = "#ngkqns^ksAHV$lb"
        SLBname = "AFAHVSLB3-4"

    elif device == "175.126.72.123" or device == "175.126.72.124": #AFAHVSLB5-6
        f5_device1_url = "https://175.126.72.123"
        f5_device2_url = "https://175.126.72.124"
        f5_device1_password = "#ngkqns^ksAHV$lb"
        f5_device2_password = "#ngkqns^ksAHV$lb"
        SLBname = "AFAHVSLB5-6"

    elif device == "211.110.224.123" or device == "211.110.224.124": #afreecahadslb1-2
        f5_device1_url = "https://211.110.224.123"
        f5_device2_url = "https://211.110.224.124"
        f5_device1_password = "#ngkqns^kshad$lb"
        f5_device2_password = "#ngkqns^kshad$lb"
        SLBname = "afreecahadslb1-2"

    elif device == "58.229.161.251" or device == "58.229.161.252":  #afreecahaddevSLB1-2
        f5_device1_url = "https://58.229.161.251"
        f5_device2_url = "https://58.229.161.252"
        f5_device1_password = "#ngkqns^kshad$lb"
        f5_device2_password = "#ngkqns^kshad$lb"
        SLBname = "afreecahaddevSLB1-2"

    elif device == "218.38.31.251" or device == "218.38.31.252":  #AFWebSLB1-2
        f5_device1_url = "https://218.38.31.251"
        f5_device2_url = "https://218.38.31.252"
        f5_device1_password = "#ngkqns^ksb2fi$lb"
        f5_device2_password = "#ngkqns^ksb2fi$lb"
        SLBname = "AFWebSLB1-2"

    elif device == "203.238.140.253" or device == "203.238.140.254":  #KIDC-SLB1-2
        f5_device1_url = "https://203.238.140.253"
        f5_device2_url = "https://203.238.140.254"
        f5_device1_password = "#ngkqns^ksb2n$lb"
        f5_device2_password = "#ngkqns^ksb2n$lb"
        SLBname = "KIDC-SLB1-2"

    elif device == "1.234.43.189" or device == "1.234.43.190":  #Nliveimgslb_1-2
        f5_device1_url = "https://1.234.43.189"
        f5_device2_url = "https://1.234.43.190"
        f5_device1_password = "#ngkqns^ksTjaspdlf$lb"
        f5_device2_password = "#ngkqns^ksTjaspdlf$lb"
        SLBname = "Nliveimgslb_1-2"


    elif device == "218.38.31.251" or device == "218.38.31.252":  #Nliveimgslb_1-2
        f5_device1_url = "https://218.38.31.251"
        f5_device2_url = "https://218.38.31.252"
        f5_device1_password = "#ngkqns^ksb2fi$lb"
        f5_device2_password = "#ngkqns^ksb2fi$lb"
        SLBname = "AFimgSLB1-2"    

    elif device == "61.253.211.253" or device == "61.253.211.254":  #spdbslb_1-2
        f5_device1_url = "https://61.253.211.253"
        f5_device2_url = "https://61.253.211.254"
        f5_device1_password = "#ngkqns^ksdb$lb"
        f5_device2_password = "#ngkqns^ksdb$lb"
        SLBname = "spdbSLB1-2"



    time.sleep(1)

    get_bigip1_confing = get_bigip_conf(f5_device1_url, f5_device1_username, f5_device1_password)
    get_bigip2_confing = get_bigip_conf(f5_device2_url, f5_device2_username, f5_device2_password)

    get_bigip1_confing = remove_passphrase(get_bigip1_confing) #간혹 SLB Conf 파일에 ssl (passphrase) 값이 있어 해당 행 제거 해주기 위한 문구
    get_bigip2_confing = remove_passphrase(get_bigip2_confing) #간혹 SLB Conf 파일에 ssl (passphrase) 값이 있어 해당 행 제거 해주기 위한 문구

    if get_bigip1_confing != get_bigip2_confing : 
        # 각 장비의 virtual 설정 정보 가져오기
        f5_device1_virtual_config = get_f5_virtual_config(f5_device1_url, f5_device1_username, f5_device1_password)
        f5_device2_virtual_config = get_f5_virtual_config(f5_device2_url, f5_device2_username, f5_device2_password)

        # 설정 정보 비교
        virtual_num, virtual_result = compare_virtual_configs(f5_device1_virtual_config, f5_device2_virtual_config,f5_device1_url, f5_device2_url, f5_device1_username, f5_device1_password)

        
        f = open("SLB Comparison.txt", "a")
        if virtual_num > 0 : #num 0 보다 크면 virtual 서버가 서로 다른게 있다는 뜻으로 아래 문구 출
           virtual_text = (" %d개의 %s Virtual Server 설정값이 같지 않음 확인 필요!!! \n" %(virtual_num, SLBname))
            
        elif virtual_num == 0: #num 값이 0이면 변화가 없다는 뜻으로 같다는뜻 아래 문구 출력
            virtual_text =  (" %s Virtual Server 설정값이 같음 \n" %SLBname)
            virtual_result.append(" %s 특이사항 없음 \n" %SLBname )

        elif virtual_num < 0 : #num 0 보다 작으면 num 값이 -1이므로 아래 문구 출력
            virtual_text = (" %s Virtual Server 수가 같지 않음 확인 필요!!! \n" )
            1


    #######################################################################################################################

        f5_device1_pool_config = get_f5_pool_config(f5_device1_url, f5_device1_username, f5_device1_password)
        f5_device2_pool_config = get_f5_pool_config(f5_device2_url, f5_device2_username, f5_device2_password)

        # 설정 정보 비교
        pool_num, pool_result = compare_pool_configs(f5_device1_pool_config, f5_device2_pool_config,f5_device1_url, f5_device2_url, f5_device1_username, f5_device1_password)
        
        f = open("SLB Comparison.txt", "a")
        if pool_num > 0 : #num 0 보다 크면 virtual 서버가 서로 다른게 있다는 뜻으로 아래 문구 출
            pool_text = ("%d개의 %s pool 설정값이 같지 않음 확인 필요!!! \n" %(pool_num, SLBname))
            
        elif pool_num == 0: #num 값이 0이면 변화가 없다는 뜻으로 같다는뜻 아래 문구 출력
            pool_text = (" %s pool 설정값이 같음 \n" %SLBname)
            pool_result.append(" %s 특이사항 없음 \n" %SLBname )

        elif pool_num < 0 : #num 0 보다 작으면 num 값이 -1이므로 아래 문구 출력
            pool_text = (" %s pool 수가 같지 않음 확인 필요!!! \n" %SLBname)
            


        
    #######################################################################################################################    
        f5_device1_node_config = get_f5_node_config(f5_device1_url, f5_device1_username, f5_device1_password)
        f5_device2_node_config = get_f5_node_config(f5_device2_url, f5_device2_username, f5_device2_password)

        node_num, node_result = compare_node_configs(f5_device1_node_config, f5_device2_node_config)
            
        if node_num > 0 : #num 0 보다 크면 virtual 서버가 서로 다른게 있다는 뜻으로 아래 문구 출
            node_text = (" %d개의 %s node 설정값이 같지 않음 확인 필요!!! \n" %(node_num, SLBname))
            
        elif node_num == 0: #num 값이 0이면 변화가 없다는 뜻으로 같다는뜻 아래 문구 출력
            node_text = (" %s node 설정값이 같음 \n" %SLBname)
            node_result.append(" %s 특이사항 없음 \n" %SLBname )

        elif node_num < 0 : #num 0 보다 작으면 num 값이 -1이므로 아래 문구 출력
            node_text = (" %s node 수가 같지 않음 확인 필요!!! \n" %SLBname)
            
    elif get_bigip1_confing == get_bigip2_confing : 
        virtual_text =  (" %s Virtual Server 설정값이 같음 \n" %SLBname)
        virtual_result = []
        virtual_result.append (" %s bigip.conf 특이사항 없음 " %SLBname )
        pool_text = (" %s pool 설정값이 같음 \n" %SLBname)
        pool_result = []
        pool_result.append (" %s bigip.conf 특이사항 없음 " %SLBname )
        node_text = (" %s node 설정값이 같음 \n" %SLBname)
        node_result = []
        node_result.append (" %s bigip.conf 특이사항 없음 " %SLBname )

    return render_template('slb/sync_result.html', virtual_result = virtual_result, virtual_text = virtual_text, 
                           pool_result = pool_result, pool_text = pool_text,
                           node_result = node_result, node_text = node_text, 
                           f5_link = f5_device1_url) #'(폴터)/"해당 html"
    
