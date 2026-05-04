# 1. 데이터
sentences = [
    "i love this movie",
    "this film is great",
    "i hate this movie",
    "this film is terrible"
]

labels = [1, 1, 0, 0]

# 2. 벡터화
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)

# 3. 데이터 분리
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42
)

# 4. 모델 학습
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

# 5. 예측
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)

print("예측:", y_pred)
print("정답:", y_test)
print("정확도:", accuracy_score(y_test, y_pred))