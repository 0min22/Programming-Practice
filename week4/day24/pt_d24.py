sentences = [
    "i love machine learning",
    "python is very fun",
    "i want to study nlp",
    "ai is the future"
]

#단어 빈도수 세기
word_count = {}
for s in sentences:
    words = s.split()
    
    for w in words:
        if w in word_count:
            word_count[w] += 1
        else:
            word_count[w] = 1
print(word_count)

#가장 많이 나온 단어
most_word = max(word_count, key = word_count.get)
print("가장 많이 나온 단어:", most_word)
print("등장 횟수:", word_count[most_word])