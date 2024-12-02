import os
import string
import imghdr
from datetime import datetime, timedelta
import calendar
import MySQLdb
import csv

##########################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Select 함수 때 필요
from selenium.webdriver.support.ui import Select
import time
from PIL import Image
import pandas as pd

#엑셀 편집
from openpyxl import load_workbook, styles
from openpyxl.styles import Border, Side, PatternFill, Alignment, Color, Font
from google.cloud import vision
import numpy as np
import openpyxl

#메일 전달
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io
import sys



options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")



chromedriver_path = "/root/venv/chromedriver"


driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)


def login():
    elem = driver.find_element_by_id("captchaImg")
    captcha_png = elem.screenshot_as_png

    # 캡차 이미지 처리
    captcha_image = Image.open(io.BytesIO(captcha_png))
    #captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6')

    captcha_image.save("captcha.png")

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'rare-shuttle-431102-k5-c963d3310b29.json'#인증 키값
    client = vision.ImageAnnotatorClient()

    file_name = "captcha.png"
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    df = pd.DataFrame(columns=['locale', 'description'])

    for text in texts:
        df = df.append(
            dict(locale=text.locale, description = text.description
            ),
            ignore_index=True
        )

    return df['description'][0]

def close_popup_if_exists():
    try:
        # 버튼 존재 여부 확인
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-default')

        if buttons:
            driver.execute_script("arguments[0].click();", buttons[0])
            print("팝업 닫기 버튼 확인")
            return True  # 버튼이 있으면 예외를 발생시켜 except 블록으로 이동

        return False  # 버튼이 없으면 함수 종료
    except (NoSuchElementException) as e:
        print(f"팝업 닫기 버튼을 찾지 못했거나 클릭 중 오류 발생: {e}")
        return False

def check_and_create_excel(file_path):
    file_name = file_path.split("\\")
    if not os.path.exists(file_path):
        print(f"{file_name[4]} 파일이 존재하지 않습니다. 새 파일을 만듭니다.")

        # 새로운 워크북 생성
        wb = Workbook()

        # 기본 시트 선택
        ws = wb.active

        # 새로운 엑셀 파일 저장
        wb.save(file_path)
        print(f"{file_name[4]} 파일이 생성되었습니다.")

    else:
        print(f"{file_name[4]} 파일이 이미 존재합니다.")

def intput_data(traffic, cost, file_path, now_time):
    wb = openpyxl.load_workbook(file_path)

    sheet = wb.active

    sheet['A1'] = "날짜"
    sheet['B1'] = "트래픽"
    sheet['C1'] = "비용"

    count = 1

    while True:
        cell_value = sheet['A' + str(count + 1)].value

        if(cell_value):
            count += 1
        else:
            sheet['A' +str(count + 1)] = now_time
            sheet['B' +str(count + 1)] = traffic + "Gbps"
            sheet['C' +str(count + 1)] = str(format(cost,',')) + "원"
            print("데이터 입력 완료")
            wb.save(file_path)
            break

def get_days_in_month(year, month):
    """
    주어진 년도와 월의 일자 수를 반환합니다.

    :param year: 연도 (예: 2024)
    :param month: 월 (1부터 12까지의 정수)
    :return: 해당 월의 일자 수
    """
    if month < 1 or month > 12:
        raise ValueError("월은 1부터 12까지의 값이어야 합니다.")

    # calendar.monthrange() 함수는 (시작 요일, 일자 수)를 튜플로 반환합니다.
    _, num_days = calendar.monthrange(year, month)
    return num_days

def db_query(day, traffic, cost):

    conn = MySQLdb.connect(
        host='118.217.182.224',
        user='serv_etl',
        password='#tltmxpa2spxmdnjzm',
        database='dw_etl_db'
    )


    cursor = conn.cursor()

    query = "REPLACE INTO stats_sys_cost_per_person_idc_traffic(stats_ymd, idc_traffic, idc_traffic_cost) VALUES ('" + str(day) + "'," + str(traffic) + "," + str(cost) + ");"
    cursor.execute(query)
    print(query)
    print("query 전달 완료")    

    conn.commit()
    print("데이터가 성공적으로 삽입되었습니다.")


    # 결과 가져오기
    results = cursor.fetchall()

    for row in results:
        print(row)

    # 연결 종료
    cursor.close()
    conn.close()

def send_email(date, body):
    # 이메일 설정
    from_email = "dlqlrxh2@gmail.com"
    password = "yvlvbrjjsboarden"
    
    # 이메일 메시지 작성
    msg = MIMEMultipart()
    msg['From'] = 'cost'
    msg['To'] = 'victory@sooplive.com'
    msg['Subject'] = date + ' SKIDC 일일 비용'

    msg.attach(MIMEText(body, 'plain'))
    
    # SMTP 서버 연결 및 이메일 전송
    server = smtplib.SMTP('smtp.gmail.com', 587)  # 예: Gmail의 경우 smtp.gmail.com
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()


    receiver = ['victory@sooplive.com']
    server.sendmail(from_email, receiver, text)
    server.quit()

def main():
    #driver = webdriver.Chrome()
    driver.get("https://my.skidc.net/my/logn/logn0101Page.do")

    #로그인
    username = "afreecatv"
    password = "dk#mflzkxlql1@"

    elem = driver.find_element_by_id('userId')
    elem.send_keys(username)
    elem = driver.find_element_by_id("passwd")
    elem.send_keys(password)


    try:
        captcha_num = login()

        elem = driver.find_element_by_id("answer")
        elem.send_keys(captcha_num)
        elem.send_keys(Keys.RETURN)

        print(captcha_num)

        login_button = driver.find_element_by_id("loginBtn")  # 실제 로그인 버튼의 ID로 교체
        login_button.click()
        time.sleep(2)

        if close_popup_if_exists():
            raise Exception("팝업 닫기 성공")

    except Exception as e:
        print(f"로그인 중 오류 발생: {e}")
        time.sleep(2)
        print("retry")
        captcha_num = login()

        elem = driver.find_element_by_id("answer")
        elem.send_keys(captcha_num)
        elem.send_keys(Keys.RETURN)

        print(captcha_num)

        login_button = driver.find_element_by_id("loginBtn")  # 실제 로그인 버튼의 ID로 교체
        login_button.click()

    time.sleep(5)

    # 팝업에서 닫기 버튼 찾기 및 클릭
    try:
        # iframe으로 전환
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "popupIframe1")))
        print("iframe 전환 성공")
        time.sleep(2)

        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="closePop"]')))
        print("팝업 닫기 버튼 확인")
        time.sleep(2)

        # JavaScript를 사용하여 요소가 화면에 보이도록 스크롤
        driver.execute_script("arguments[0].scrollIntoView(true);", close_button)

        time.sleep(1)  # 스크롤 후 잠시 대기

        # JavaScript를 사용하여 닫기 버튼 클릭
        driver.execute_script("arguments[0].click();", close_button)
        print("팝업 닫기 버튼 클릭 완료")
        time.sleep(2)


        # 기본 콘텐츠로 돌아가기
        driver.switch_to.default_content()
    except Exception as e:
        #print(f"팝업 닫기 버튼을 찾지 못했습니다: {e}")
        print("")

    # 팝업에서 닫기 버튼 찾기 및 클릭
    try:
        # iframe으로 전환
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "popupIframe0")))
        print("iframe 전환 성공")
        time.sleep(2)

        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="closePop"]')))
        print("팝업 닫기 버튼 확인")
        time.sleep(2)

        # JavaScript를 사용하여 요소가 화면에 보이도록 스크롤
        driver.execute_script("arguments[0].scrollIntoView(true);", close_button)

        time.sleep(1)  # 스크롤 후 잠시 대기

        # JavaScript를 사용하여 닫기 버튼 클릭
        driver.execute_script("arguments[0].click();", close_button)
        print("팝업 닫기 버튼 클릭 완료")
        time.sleep(2)


        # 기본 콘텐츠로 돌아가기
        driver.switch_to.default_content()
    except Exception as e:
        #print(f"팝업 닫기 버튼을 찾지 못했습니다: {e}")
        print("")




    traffic_view_button = driver.find_element_by_id("trafficBtn")
    traffic_view_button.click()

    time.sleep(5)

    # iframe 내부 체크박스 선택 및 버튼 클릭
    try:
        # iframe 전환 확인
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "popupIframe0")))  # iframe의 실제 ID로 교체
        print("iframe 전환 성공")
        time.sleep(2)
        # 체크박스 존재 확인
        checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "listTable1allCheckbox")))
        print("체크박스 존재 확인")
        time.sleep(2)
        # 체크박스 클릭
        driver.execute_script("arguments[0].click();", checkbox)
        print("체크박스 선택 완료")
        time.sleep(2)
        # 합산트래픽보기 버튼 존재 확인
        traffic_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "trafficAllBtn")))
        print("합산트래픽보기 버튼 존재 확인")
        time.sleep(2)
        # 합산트래픽보기 버튼 클릭
        driver.execute_script("arguments[0].click();", traffic_button)
        print("합산트래픽보기 버튼 클릭 완료")

        # 기본 콘텐츠로 돌아가기
        driver.switch_to.default_content()

    except Exception as e:
        print(f"체크박스 선택 또는 합산트래픽보기 버튼 클릭을 실패했습니다: {e}")
        driver.quit()

    time.sleep(5)

    
    try:
        # iframe 전환 확인
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "popupIframe1")))  # iframe의 실제 ID로 교체
        print("iframe 전환 성공")
        time.sleep(2)

         # CSV 다운로드 버튼 클릭
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'chartArea1CsvDownBtn'))  # 다운로드 버튼의 ID 사용하여 찾기
        )
        print("csv저장 버튼 존재 확인")
        time.sleep(2)

        # 합산트래픽보기 버튼 클릭
        download_button.click()
        print("csv저장 버튼 클릭 완료")

        # 기본 콘텐츠로 돌아가기
        driver.switch_to.default_content()

        driver.quit()


        time.sleep(2)

    except Exception as e:
        print(f"csv저장 버튼 클릭하는 데 실패했습니다: {e}")
        driver.quit()
    
    time.sleep(5)
    file_path = "일간그래프(5분평균).csv"

    try:
        count = 0
        values = []


        # CSV 파일 열기
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            # CSV 파일을 읽기 위한 객체 생성
            reader = csv.reader(file)

            # 데이터 읽기
            for row in reader:
                count += 1
                if( count <= 3):
                    continue
                elif( count >= 73):
                    values.append(float(row[1]))

        if values:
            traffic = round((max(values)/1000000),2)
            print(f"최고 값: {traffic}")
        else:
            print("열에서 유효한 숫자를 찾을 수 없습니다.")
    except Exception as e:
        print(f"최대 수신 값을 가져오는 데 실패했습니다: {e}")
        driver.quit()

    '''
    # CSV 파일 삭제
    try:
        os.remove(file_path)
        print(f"파일이 성공적으로 삭제되었습니다: {file_path}")
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except PermissionError:
        print(f"파일을 삭제할 권한이 없습니다: {file_path}")
    except Exception as e:
        print(f"파일 삭제 중 오류가 발생했습니다: {e}")
    '''

    '''
    # 최대 수신 값을 가져옵니다
    try:
        # iframe 전환 확인
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "popupIframe1")))  # iframe의 실제 ID로 교체
        print("iframe 전환 성공")
        time.sleep(7)

        max_receive_elem = driver.find_element(By.XPATH, '//*[@id="chartArea1InfoArea"]/div[1]/div[1]')
        max_receive_text = max_receive_elem.text
        print(f"최대 수신 값: {max_receive_text}")

        max_traffic = max_receive_text.split(" ")

        # 기본 콘텐츠로 돌아가기
        driver.switch_to.default_content()
    except Exception as e:
        print(f"최대 수신 값을 가져오는 데 실패했습니다: {e}")
        driver.quit()
    '''    


    now = datetime.now()
    yesterday = now - timedelta(days=1)
    now_time = yesterday.strftime('%m')

    year = yesterday.strftime('%Y')
    month = yesterday.strftime('%m')
    days = get_days_in_month(int(year), int(month))
    date = yesterday.strftime('%Y-%m-%d')

   
    cost = round(traffic / 1000 * 2900000/days)

    print("트래픽 최대값 : " +  str(format(traffic,',')) + "Mbps")
    print("트래픽 비용 : " + str(format(cost,',')) + "원")

    db_query(date, traffic, cost)


    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        # 여기에 실행할 스크립트를 작성합니다.

        print("트래픽 최대값 : " +  str(format(traffic,',')) + "Mbps")
        print("트래픽 비용 : " + str(format(cost,',')) + "원")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 출력 캡처 종료
    sys.stdout = old_stdout
    output = new_stdout.getvalue()

    # 캡처된 출력을 이메일로 전송
    send_email(date, body=output)



    #file_path = r"C:\Users\victory\Desktop\skidc_daily_cost.xlsx"

    #now = datetime.now()
    #yesterday = now - timedelta(days=1)
    #now_time = yesterday.strftime('%y-%m-%d')

    #check_and_create_excel(file_path)

    #intput_data(max_traffic[3], cost, file_path, now_time)

    driver.quit()


if __name__ == "__main__":
    main()
