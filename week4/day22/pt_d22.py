sentences = [
    "I love machine learning",
    "Python is very fun",
    "I want to study NLP",
    "AI is the future"
]

print(sentences)

#문장 길이 확인
for s in sentences:
    print(s, "-> 길이:", len(s))

#단어 개수 세기
for s in sentences:
    words = s.split()
    print(s)
    print("단어 개수:", len(words))
    
#가장 긴 문장 찾기
longest = ""
for s in sentences:
    if len(s) > len(longest):
        longest = s
print("가장 긴 문장:", longest)