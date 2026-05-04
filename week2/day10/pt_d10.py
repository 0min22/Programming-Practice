#기존 코드 응용
def analyze_log():
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
            
            if len(line) < 2:
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
                f.write(user + " : " + str(fail_users[user]) + "회 실패\n")

#결과보기
def show_result():
    try:
        with open("result.txt" , "r") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("result.txt가 없습니다.")
            
#위험 사용자만 보기
def show_danger_users():
    try:
        with open("result.txt", "r") as f:
            print("위험 사용자 목록")
            for line in f:
                if "회 실패" in line:
                    print(line.strip())
    except FileNotFoundError:
        print("result.txt가 없습니다. 먼저 분석을 실행하세요.")
                
        
            
#메뉴 만들기
while True:
    print("1. 분석")
    print("2. 결과 보기")
    print("3. 위험 사용자 목록 보기")
    print("4. 종료")

    menu = input("선택: ")
    
    if menu == "1":
        analyze_log()
    elif menu == "2":
        show_result()
    elif menu == "3":
        show_danger_users()
    elif menu == "4":
        break
    else:
        print("잘못 된 입력입니다.")
    