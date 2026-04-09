#1
numbers = [10, 20, 30, 40]
print(numbers[0])

#2
fruits =["apple", "banana", "grape"]
fruits[2] = "watermelon"
print(fruits)

#3
person = {
    "name" : "Tom",
    "age" : 25
}
print(person["name"])
print(person["age"])

#4
score = 55
if score >= 60:
    print("합격")
else:
    print("불합격")
 
#5  
numbers = [3, 6, 9, 12]
total = 0

for sum in numbers:
    total += sum
print(total)

#6
numbers = [1, 2, 3, 4, 5, 6]
for i in numbers:
    if (i % 2 == 0):
        print(i)
        
#7
student = {
    "name" : "Jane",
    "age" : 22
}

student["grade"] = "B"
print(student)

#8
def is_even(num):
    if(num % 2 == 0):
        print("짝수")
    else:
        print("홀수")
is_even(3)
is_even(10)

#9
def get_grade(score):
    if(score >= 90):
        print("A")
    elif(score >= 80):
        print("B")
    else:
        print("C")
get_grade(95)
get_grade(83)
get_grade(60)

#10
def total_sum(numbers):
    sum = 0
    for i in numbers:
        sum += i
    return sum
        
result = total_sum([1, 2, 3, 4])
print(result)

#test1
nums = [10, 20, 30, 40, 50]
total = 0
for i in nums:
    total += i
avg = total / len(nums)
print(avg)

#test2
num = int(input())
if(num % 2 == 0):
    print("짝수")
else:
    print("홀수")
    
#test3
text = input()
count = 0
for i in range(len(text)):
    count += 1
print(count)
