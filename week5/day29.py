sentences = [
    "I love this movie!",
    "This film is great",
    "I hate this movie",
    "This film is terrible"
]

labels = [1, 1, 0, 0]

#전처리 함수 만들기
def preprocess_text(text):
    text = text.lower()
    text = text.replace("!", "")
    text = text.replace(".", "")
    
    return text

#문장 전체 전처리
clean_sentences = []
for s in sentences:
    clean_sentences.append(preprocess_text(s))

print(clean_sentences)

#벡터화 함수
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_text(sentences):
    vectorize = TfidfVectorizer()
    X = vectorize.fit_transform(sentences)
    
    return X, vectorize

#벡터화 함수 사용
X, vectorize = vectorize_text(clean_sentences)

print(vectorize.get_feature_names_out())
print(X.toarray())

#linear model
from sklearn.linear_model import LogisticRegression

def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    
    return model

#linear model 실행
model = train_model(X, labels)
pred = model.predict(X)

print("예측 결과: ", pred)