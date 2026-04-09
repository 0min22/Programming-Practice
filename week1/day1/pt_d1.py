#리스트
fruits =["apple", "banana", "grape"]
print(fruits[0])

#수정
fruits[0] = "orange"
print(fruits)

#길이 구하기
print(len(fruits))

#딕셔너리
student = {
    "name": "Alice",
    "age": 20,
    "major": "Computer Science"
}
print(student["name"])
print(student["age"])

#딕셔너리 추가/변경
print(student)
student["grade"] = "A"
print("변경 후 : ", student)

#if문

age = 20

if age>= 19:
    print("성인입니다.")
else:
    print("미성년자입니다.")
    
#조건이 여러개 -> java에선 ;를 썼지만 파이썬에선 :를 사용, else if가 아닌 elif
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
    
#for문
#for문의 형태는 for 변수 in range(시작값, 종료값, 증가값):
for i in range(5):
    print(i)
    
#리스트와 함께 사용
for fruit in fruits:
    print(fruit)
    
#합계 구하기
numbers = [1, 2, 3, 4, 5]
total = 0
for sum in numbers: #끝에 : 꼭 넣기
    total += sum
print("합계 : ", total)

#함수 만들기
def greet(name):
    print(name + "님 안녕하세요")
    
greet("Alice")
greet("Bob")

def add(a, b):
    return a + b

result = add(3, 5)
print("합계 : ", result)
    
        

