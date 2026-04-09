#test1
numbers = []
total = 0
for i in range(5): #for문 입력 받아서 list에 집어넣기
    num = int(input("숫자 입력: "))
    numbers.append(num)
    total += num
ans = total / len(numbers)
print(ans) 

#test2
text = input()
print(text.upper())
print(len(text))

#test3
text3 = input()
ans = len(text3.replace(" ", ""))
print(ans)