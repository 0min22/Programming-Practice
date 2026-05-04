sentences = [
    "I love Machine Learning!",
    "Python is VERY fun!!!",
    "I want to study NLP.",
    "AI is the future :)"
]

#소문자 변환
for s in sentences:
    print(s.lower())
    
#단어 분리
for s in sentences:
    words = s.lower().split()
    print(words)
    
#단어 개수 세기
for s in sentences:
    words = s.lower().split()
    print("단어 개수:", len(words))
    
#특수문자 제거 조금
clear_sentences = []

for s in sentences:
    s = s.lower()
    s = s.replace("!", "")
    s = s.replace(".", "")
    s = s.replace(":", "")
    s = s.replace(")", "")
    clear_sentences.append(s)
print(clear_sentences)
    