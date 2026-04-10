#test1
student = {"name" : "Min", "score" : 95}
print(student["name"])
print(student["score"])

#test2
students = [
    {"name" : "Kim", "score" : 80},
    {"name" : "Lee", "score" : 92},
    {"name" : "Park", "score" : 88}
]
for i in students:
    print(i["name"] , i["score"])
    
#test3
total = 0
for i in students:
    total += i["score"]
avg = total / len(students)
print(avg)

#test4
top_student = students[0]

for i in students:
    if top_student["score"] < i["score"]:
        top_student = i
print(top_student["name"], top_student["score"])