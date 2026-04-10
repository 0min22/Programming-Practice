#test1 파일 만들기
with open("log.txt", "w") as f:
    f.write("LOGIN")
    f.write("\n")
    f.write("ERROR")
    f.write("\n")
    f.write("LOGIN")
    f.write("\n")
    f.write("FAIL")
    f.write("\n")
    f.write("ERROR")
    f.write("\n")
    f.write("LOGIN")
    f.write("\n")
    f.write("FAIL")
    
#test2 전체 줄 수 출력
count = 0
with open("log.txt" , "r") as f:
    for log in f:
        count += 1
print(count)

#test3 ERROR 개수 출력
count_error = 0
with open("log.txt", "r") as f:
    for log in f:
        if log.strip() == "ERROR":
            count_error += 1
print(count_error)

#test4 각 로그 종류 개수 세기
counts = {"LOGIN" : 0, "ERROR" : 0, "FAIL" : 0}
with open("log.txt", "r") as f:
    for log in f:
        log = log.strip()
        if log == "LOGIN":      #if log in counts:
            counts[log] += 1        #counts[log] += 1 사용가능
                                    #-> counts와 log가 같은 것이 있다면 증가
        elif log == "ERROR":
            counts[log] += 1
            
        elif log == "FAIL":
            counts[log] += 1
print(counts)

