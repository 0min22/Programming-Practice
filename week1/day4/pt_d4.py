#딕셔너리
student = {"name" : "Kim", "score" : 90}
print(student["name"])

#리스트 안에 딕셔너리 넣기
students = [
    {"name" : "Kim", "score" : 90},
    {"name" : "Lee", "score" : 85},
    {"name" : "Park", "score" : 100}
]
for student in students:
    print(student["name"], student["score"])
    
#평균 구하기
total = 0
for student in students:
    total += student["score"]
print(total / len(students))

#최고 점수 찾기
max_score = 0
for student in students:
    if student["score"] >= max_score:
        max_score = student["score"]
print(max_score)

#최고 점수 학생까지 찾기
top_student = students[0]
for student in students:
    if student["score"] > top_student["score"]:
        top_student = student
print(top_student["name"], top_student["score"])