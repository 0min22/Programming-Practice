from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression

#데이터 불러오기
data = load_iris()

#입력과 정답
X = data.data
y = data.target

#train / test 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)

#확인
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

#모델 생성
model = KNeighborsClassifier()

#학습
model.fit(X_train, y_train)

#예측
pred = model.predict(X_test)

#결과 확인
print("예측 값:", pred[:10])
print("실제 값:", y_test[:10])

#정확도
acc = accuracy_score(y_test, pred)
print("정확도:", acc)

#혼동 행력
cm = confusion_matrix(y_test, pred)
print("혼동 행렬:\n", cm)

#KNN
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)

knn_acc = accuracy_score(y_test, knn_pred)
print("KNN 정확도:", knn_acc)

#Logistic Regression
lr = LogisticRegression(max_iter = 200)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

lr_acc = accuracy_score(y_test, lr_pred)
print("Logistic Regression 정확도:", lr_acc)