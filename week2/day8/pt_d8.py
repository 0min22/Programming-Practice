#입력 받기
filename = input("파일 이름을 입력하세요: ")

#파일 읽기
with open(filename, "r") as f:
    for line in f:
        print(line.strip())

#딕셔너리
check = {"LOGIN": 0, "ERROR": 0, "FAIL": 0}
line_count = 0
fail_users = {}

with open(filename, "r") as f:
    for log in f:
        line = log.strip().split()
        
        if len(line) == 0:
            continue
        
        line_count += 1
        
        if line[0] == "LOGIN":
            check["LOGIN"] += 1
        elif line[0] == "ERROR":
            check["ERROR"] += 1
        elif line[0] == "FAIL":
            check["FAIL"] += 1
            
            user = line[1]
            
            if user in fail_users:
                fail_users[user] += 1
            else:
                fail_users[user] = 1

#가장 많이 나온 값 찾기
most_log = max(check, key=check.get)
print(most_log)

#결과를 파일에 저장하기
with open("result.txt", "w") as f:
    f.write("분석 결과\n")
    f.write("전체 줄 수: " + str(line_count) + "\n")
    f.write("로그 개수: " + str(check) + "\n")
    f.write("가장 많이 나온 로그: " + most_log + "\n")
    f.write("위험 사용자\n")
    
    for user in fail_users:
        if fail_users[user] >= 3:
            f.write(user + " : " + str(fail_users[user]) + "\n")