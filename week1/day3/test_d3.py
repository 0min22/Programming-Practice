#test1
with open("output.txt", "w") as f:
    f.write("Hello Python")

#test2
with open("output.txt", "r") as f:
    print(f.read())

#test3 \n 사용해서 줄바꿈
with open("output.txt", "w") as f:
    f.write("apple" + "\n" + "banana" + "\n" + "apple" + "\n" + "grape")
with open("output.txt", "r") as f:
    print(f.read())
count = 0
with open("output.txt", "r") as f:
    for line in f:
        count += 1
print(count)

#test4
count_apple = 0
with open("output.txt", "r") as f:
    for line in f:
        if line.strip() == "apple": #line.strip -> 앞뒤 공백 + \n 제거
            count_apple += 1
print(count_apple)

#한번만 열어도 괜찮다!
'''
with open("output.txt", "r") as f:
    lines = f.readlines()

# 출력
print("".join(lines))

# 줄 개수
print(len(lines))

# apple 개수
count_apple = 0
for line in lines:
    if line.strip() == "apple":
        count_apple += 1

print(count_apple)
'''
