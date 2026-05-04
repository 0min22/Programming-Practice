#test1
text = "banana"
count = {}

for ch in text:
    if ch in count:
        count[ch] += 1
    else:
        count[ch] = 1
most_char = max(count, key=count.get)
print(most_char, count[most_char])

#test2
numbers = [1,2,2,3,1,4]
result = []

for num in numbers:
    if num not in result:
        result.append(num)
print(result)

#test3
value = {"a" : 3, "b" : 10, "c" : 5}
max_key = max(value, key=value.get)
print(max_key)