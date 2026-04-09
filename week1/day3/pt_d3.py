f = open("test.txt", "w")
f.write("hello")
f.close()

f = open("test.txt", "r")
data = f.read()
print(data)
f.close()