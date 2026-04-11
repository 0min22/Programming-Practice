#위험한 코드 -> 단순해서 쉽게 뚫림
password = input("비밀번호: ")

if password == "1234":
    print("로그인 성공")
    
#입력 검증 없음
user_input = input("명령어: ")
print("실행:", user_input)

#문자열 길이 확인   len()
text = input()
if len(text) >= 4:
    print("통과")
    
#숫자인지 확인  isdigit()
text = input()
if text.isdigit():
    print("숫자임")
else:
    print("숫자 아님")
    
#특정 단어 포함 여부 if ~ 'in' ~:
text = input()
if "hack" in text:
    print("위험")
    
#조건 여러 개 같이 쓰기 and
pw = input()

if len(pw) >= 4 and pw.isdigit:
    print("올바름")
else:
    print("잘못됨")