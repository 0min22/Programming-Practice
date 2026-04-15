from sklearn.feature_extraction.text import TfidfVectorizer

#문장 생성
sentences = [
    "i love machine learning",
    "python is very fun",
    "i want to study nlp",
    "ai is the future"
]

#TF-IDF 적용
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)

#단어 목록
print(vectorizer.get_feature_names_out())

#결과 확인
print(X.toarray())