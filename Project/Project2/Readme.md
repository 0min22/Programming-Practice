# 전자상거래 구매 예측 및 추천 시스템

## 프로젝트 소개

전자상거래 사용자 데이터를 기반으로 사용자의 구매 여부를 예측하는 머신러닝 프로젝트이다.

사용자의 클릭 여부, 나이, 상품 가격, 상품 평점, 페이지 체류 시간, 상품 종류, 성별, 지역 등의 정보를 활용하여 구매 여부를 분류하고, 여러 머신러닝 모델의 성능을 비교하였다.

단순히 정확도(Accuracy)만 확인하는 것이 아니라 ROC Curve, AUC, Confusion Matrix, Classification Report를 함께 분석하여 불균형 데이터 환경에서 모델을 어떻게 평가해야 하는지 확인하는 데 중점을 두었다.

또한 Streamlit 기반 웹앱을 구현하여 실제 서비스 형태처럼 사용자가 정보를 입력하면 예상 구매 확률을 확인할 수 있도록 구성하였다.

---

# 사용 데이터

사용 데이터는 전자상거래 사용자 행동 데이터를 기반으로 구성되어 있다.

총 데이터 수:

* 6012개

주요 컬럼:

* click
* purchase
* user_age
* product_price
* product_rating
* time_on_page
* product_type
* user_gender
* user_location

데이터 확인 결과 결측치는 존재하지 않았다.

구매 데이터 비율은 약 19.8%, 비구매 데이터 비율은 약 80.2%로 불균형 데이터 형태를 보였다.

---

# 프로젝트 구조

```text
Project2
│
├── analysis
│   ├── feature_importance.csv
│   ├── feature_importance.png
│   ├── model_auc_comparison.png
│   ├── model_summary.csv
│   ├── purchase_analysis.png
│   ├── roc_decision_tree.png
│   ├── roc_knn.png
│   ├── roc_logistic.png
│   ├── roc_random_forest.png
│   └── roc_svm.png
│
├── data
│   └── Project2_data.csv
│
├── models
│   ├── best_model.pkl
│   ├── model_columns.pkl
│   ├── random_forest_model.pkl
│   └── scaler.pkl
│
├── Project2.py
├── Project2_upgrade.py
└── Project2_app.py
```

---

# 사용 라이브러리

```python
pandas
matplotlib
scikit-learn
joblib
streamlit
```

---

# 데이터 분석

프로젝트 시작 단계에서 데이터의 기본 구조와 분포를 확인하였다.

* 결측치 확인
* 구매 비율 분석
* 상품 종류별 구매율 확인
* 클릭 대비 구매율 분석
* 페이지 체류 시간과 구매 관계 시각화

체류 시간(time_on_page)에 대한 히스토그램을 통해 구매 사용자와 비구매 사용자의 분포를 비교하였다.

---

# 전처리 과정

모델 학습 전 다음과 같은 전처리를 수행하였다.

## One-Hot Encoding

문자형 데이터:

* product_type
* user_gender
* user_location

에 대해 `pd.get_dummies()`를 사용하여 One-Hot Encoding을 적용하였다.

## Train / Test Split

```python
test_size=0.2
random_state=42
stratify=y
```

를 사용하여 학습 데이터와 테스트 데이터를 분리하였다.

구매 데이터 비율이 불균형했기 때문에 stratify 옵션을 사용하여 train/test 데이터에서도 구매 비율이 유지되도록 구성하였다.

## Standard Scaling

Logistic Regression, KNN, SVM 모델에는 StandardScaler를 적용하였다.

---

# 사용 모델

프로젝트에서는 총 5개의 모델을 비교하였다.

## 1. Logistic Regression

선형 기반 분류 모델로, 가장 기본적인 이진 분류 모델이다.

## 2. Decision Tree

트리 구조를 기반으로 데이터를 분류하는 모델이다.

## 3. Random Forest

여러 개의 Decision Tree를 앙상블하여 사용하는 모델이다.

Feature Importance 분석에도 활용하였다.

## 4. KNN

가까운 이웃 데이터를 기반으로 분류하는 거리 기반 모델이다.

## 5. SVM

초평면을 기준으로 데이터를 분류하는 모델이다.

---

# 성능 평가 방법

다음 지표들을 사용하여 모델 성능을 평가하였다.

* Accuracy
* Confusion Matrix
* Precision
* Recall
* F1-score
* ROC Curve
* AUC

특히 데이터가 불균형했기 때문에 Accuracy만으로 모델을 평가하지 않고 AUC와 Recall을 함께 확인하였다.

---

# 실험 결과

모델 비교 결과 SVM 모델이 가장 높은 Accuracy를 기록하였다.

하지만 Confusion Matrix를 확인한 결과, 구매 데이터를 거의 예측하지 못하는 문제가 나타났다.

즉 Accuracy는 높았지만 실제 구매자를 분류하지 못했기 때문에 단순 Accuracy만으로 모델 성능을 평가하는 것은 적절하지 않다는 점을 확인할 수 있었다.

반면 Logistic Regression은 Accuracy는 낮았지만 구매 데이터를 일부 예측하는 모습을 보였다.

전체적으로 대부분 모델의 AUC가 0.5 근처로 나타났기 때문에 현재 feature만으로는 구매 여부를 강하게 설명하기 어렵다는 한계도 확인할 수 있었다.

---

# Feature Importance 분석

Random Forest 모델을 사용하여 변수 중요도를 분석하였다.

중요도가 높게 나타난 변수는 다음과 같다.

* product_price
* time_on_page
* user_age
* product_rating

이를 통해 상품 가격, 페이지 체류 시간, 사용자 나이, 상품 평점이 구매 여부 예측에 상대적으로 큰 영향을 주는 것을 확인하였다.

---

# Streamlit 웹앱

Streamlit을 사용하여 간단한 웹 서비스를 구현하였다.

사용자가 다음 정보를 입력하면:

* 클릭 여부
* 나이
* 상품 가격
* 상품 평점
* 페이지 체류 시간
* 상품 종류
* 성별
* 지역

예상 구매 확률을 출력하도록 구성하였다.

실제 서비스 형태의 추천 시스템 흐름을 간단하게 구현하는 것을 목표로 하였다.

---

# 프로젝트를 통해 배운 점

이번 프로젝트를 통해 단순히 모델 Accuracy만 확인하는 것이 아니라 데이터 분포와 불균형 문제를 함께 고려해야 한다는 점을 확인할 수 있었다.

또한 여러 모델을 직접 비교하고 ROC Curve, AUC, Confusion Matrix를 함께 분석하면서 머신러닝 모델 평가 방식에 대해 이해할 수 있었다.

Random Forest의 Feature Importance를 통해 어떤 feature가 모델에 영향을 주는지도 확인할 수 있었으며, Streamlit을 통해 머신러닝 모델을 간단한 서비스 형태로 연결하는 과정도 경험할 수 있었다.
