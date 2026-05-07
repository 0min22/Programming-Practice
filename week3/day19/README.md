# Day19 Mini ML Project

## 목표
iris 데이터를 이용해 두 개의 분류 모델(KNN, Logistic Regression)을 비교한다.

## 사용한 내용
- train_test_split
- KNeighborsClassifier
- LogisticRegression
- accuracy_score

## 실험 방법
- iris 데이터 사용
- feature 2개만 사용
- train/test 분리 후 두 모델 학습
- 정확도 비교

## 결과
- KNN 정확도: 0.8166666666666667
- Logistic Regression 정확도: 0.85

## 해석
feature를 줄였을 때 Logistic Regression이 더 잘 나왔다.
데이터 구조에 따라 더 유리한 모델이 달라질 수 있음을 확인했다.