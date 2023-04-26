'''

import paramiko

# SSH 접속 정보 설정
hostname = '175.196.233.125'
port = 22222
username = 'mslee'
password = 'Itian12#$%'

# SSH 클라이언트 생성
ssh = paramiko.SSHClient()

# SSH 호스트 키 인증 무시
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# SSH 접속
ssh.connect(hostname=hostname, port=port, username=username, password=password)

# SSH 명령 실행
stdin, stdout, stderr = ssh.exec_command('snmpwalk -v 2c -Os -c test localhost .1.3.6.1.4.1.3375.2.100.1')


# 실행 결과 출력
print(stdout.read())

# SSH 세션 종료
ssh.close()
'''

import paramiko
import time


# SSH 클라이언트 생성
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# SSH 접속 정보 설정
hostname = '203.238.150.185'
port = 22
username = 'root'
password = '#ngkqns^ksG$LB'


# SSH 연결
client.connect(hostname, port=port, username=username, password=password)

transport = client.get_transport()
if transport.is_active():
    print('SSH connection established successfully!')
else:
    print('Failed to establish SSH connection!')


# 명령어 실행
stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c skdnzha localhost  1.3.6.1.4.1.3375.2.3.12.1.2.1.1')
#stdin, stdout, stderr = client.exec_command('snmpwalk -v 2c -Os -c test localhost .1.3.6.1.4.1.3375.2.3.6.7.2.1.5')


#time.sleep(10)


# 결과 출력
print(stdout.read().decode() + "\n")

# SSH 연결 종료
client.close()

















