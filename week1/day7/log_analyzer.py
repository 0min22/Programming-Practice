#파일 읽기
#전체 줄 수 출력
#로그 종류별 개수 출력
#FAIL이 3 이상이면 위험 사용자
#ERROR도 같이 분석해서 많으면 경고
line_count = 0
check = {"LOGIN": 0, "ERROR": 0, "FAIL": 0}
with open("log.txt" , "r") as f:
    for log in f:
        line_count += 1
        if log.strip() == "LOGIN":
            check["LOGIN"] += 1
        elif log.strip() == "ERROR":
            check["ERROR"] += 1
        elif log.strip() == "FAIL":
            check["FAIL"] += 1
            
print("전체 로그 수: ", line_count)

for i in check:
    print(i, ":", check[i])    
            
if check["FAIL"] >= 3:
    print("위험 사용자")
    
if check["ERROR"] >= 3:
    print("경고")
