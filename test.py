import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io
import sys


def send_email(body, to_email):
    # 이메일 설정
    from_email = "dlqlrxh2@gmail.com"
    password = "yvlvbrjjsboarden"
    
    # 이메일 메시지 작성
    msg = MIMEMultipart()
    msg['From'] = 'cost'
    msg['To'] = 'victory@sooplive.com'
    msg['Subject'] = 'SKIDC 일일 비용'

    msg.attach(MIMEText(body, 'plain'))
    
    # SMTP 서버 연결 및 이메일 전송
    server = smtplib.SMTP('smtp.gmail.com', 587)  # 예: Gmail의 경우 smtp.gmail.com
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail("test@test", to_email, text)
    server.quit()

def main_script():
    # 출력 캡처
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        # 여기에 실행할 스크립트를 작성합니다.
        print("This is a test output")
        print("Another line of output")

    except Exception as e:
        print(f"An error occurred: {e}")

    # 출력 캡처 종료
    sys.stdout = old_stdout
    output = new_stdout.getvalue()

    # 캡처된 출력을 이메일로 전송
    send_email(body=output, to_email="victory@sooplive.com")

if __name__ == "__main__":
    main_script()
