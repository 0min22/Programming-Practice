#test1
user_password = input("비밀번호: ")
if len(user_password) >= 4 and user_password.isdigit():
    print("통과")
else:
    print("거부")
    
#test2
pw = input("비밀번호: ")
if pw.isdigit():
    print(int(pw))
else:
    print("ERROR")
    
#test3
strings = input("입력 :")
if "admin" in strings or "root" in strings or "hack" in strings:
    print("차단")
else:
    print("허용")
    
#test4
check_FAIL = 0

with open("log.txt", "r") as f:
    for log in f:
        if log.strip() == "FAIL":
            check_FAIL += 1
if check_FAIL >= 3:
    print("위험 사용자")
else:
    print("정상 사용자")

        
