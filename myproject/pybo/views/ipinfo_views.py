import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User
import requests
from requests.auth import HTTPBasicAuth
import json
import time

bp = Blueprint('ipinfo', __name__, url_prefix='/') #폴더
@bp.route('/ipinfo/', methods=('GET', 'POST'))
def ipinfo(): #ipinfo 처음 실행시 보여지는 HTML
    return render_template('ipinfo/ipinfo.html') #'(폴터)/"해당 html"


@bp.route('/ipinfo/result', methods=('GET', 'POST')) #html
def ipinfo_result():
    input_ip = request.form.get('IP')
    if input_ip:
        ip_list = input_ip.splitlines() 
        
    else:
         return 'no date'
    

    access_token = '9425a73b978934'
    ipinfo_url = 'https://ipinfo.io/'

    ip_company_list = []
    ip_domain_list = []
    ip_country_list = []
    ip_city_list = []

    all_data = []
    for ip_address in ip_list:
        response = requests.get(f"{ipinfo_url}{ip_address}/json?token={access_token}")
    
        try:

            details = response.json()
            
            company = details.get('company', {})
            ip_company = company.get('name', 'N/A')
            ip_domain = company.get('domain', 'N/A')
        except Exception as e:
            print(f"Error processing details for IP {ip_address}: {e}")
            print(f"Response content: {response.text}")
        
        ip_country = details.get('country', 'N/A')
        ip_city = details.get('city', 'N/A')


        ip_company_list.append(ip_company) 
        ip_domain_list.append(ip_domain)
        ip_country_list.append(ip_country)
        ip_city_list.append(ip_city)
    

    for i in range(len(ip_list)):
        single_entry = [ip_list[i], ip_company_list[i], ip_domain_list[i], ip_country_list[i], ip_city_list[i]]
        all_data.append(single_entry)
    numRows = len(ip_list)
    
    


    return render_template('ipinfo/ipinfo_result.html', ip=all_data, numRows=numRows)
