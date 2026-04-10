#로그 파일 안에 특정 단어 세기

#로그 파일 만들기 -> Day3 참고
with open("log.txt", "w") as f:
    f.write("INFO" + "\n" + "ERROR" + "\n" + "INFO" + "\n" + "WARNING" + "\n"
            + "ERROR" + "\n" + "ERROR" + "\n")


#한 줄씩 읽기
with open("log.txt", "r") as f:
    for log in f:
        print(log.strip())

#특정 단어 개수 세기
count_error = 0
with open("log.txt", "r") as f:
    for log in f:
        if log.strip() == "ERROR":
            count_error += 1
print(count_error)

#여러 종류 동시에 세기
count_info = 0
count_error1 = 0
with open("log.txt", "r") as f:
    for log in f:
        log = log.strip()
        
        if log == "INFO":
            count_info += 1
            
        elif log == "ERROR":
            count_error1 += 1
print(count_error1)
print(count_info)

#딕셔너리로 정리
counts = {"INFO" : 0, "ERROR" : 0, "WARNING" : 0}
with open("log.txt" , "r") as f:
    for log in f:
        log = log.strip()
        if log in counts:
            counts[log] += 1
print(counts)