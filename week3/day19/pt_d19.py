from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#데이터 불러오기
data = load_iris()
X = data.data
y = data.target

#각 모델 비교를 위해 feature 일부만 사용
X = X[:, :2]

#train / test 나누기
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.4, random_state = 42
)

#KNN 모델
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)
knn_acc = accuracy_score(y_test, knn_pred)

#Logistic Regression 모델
lr = LogisticRegression(max_iter=200)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
lr_acc = accuracy_score(y_test, lr_pred)

#결과 출력
print("KNN 정확도", knn_acc)
print("Logistic Regression 정확도:", lr_acc)