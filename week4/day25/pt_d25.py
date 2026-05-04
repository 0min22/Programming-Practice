from sklearn.feature_extraction.text import CountVectorizer

#문장 준비
sentences = [
    "i love machine learning",
    "python is very fun",
    "i want to study nlp",
    "ai is the future"
]

#벡터화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

#단어 목록 확인
print(vectorizer.get_feature_names_out())

#숫자 배열 확인
print(X.toarray())

#명확히 보기
print(vectorizer.vocabulary_)

