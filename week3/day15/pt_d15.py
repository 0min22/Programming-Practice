from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

#데이터 불러오기
data = load_iris()

#입력과 정답
X = data.data
y = data.target

#train / test 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

#확인
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)