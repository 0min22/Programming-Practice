# 데이터 확인
import pandas as pd

df = pd.read_csv("data/Project2_data.csv")

print(df.info())
print(df.describe())
print(df.isnull().sum())

# 구매율 분석
print(df["purchase"].value_counts())

print(df["purchase"].value_counts(normalize=True))

# 상품 종류별 구매율
print(df.groupby("product_type")["purchase"].mean())
# 클릭 대비 구매율
print(df.groupby("click")["purchase"].mean())
# 체류 시간과 구매 관계
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

purchase_time = df[df["purchase"] == 1]["time_on_page"]
non_purchase_time = df[df["purchase"] == 0]["time_on_page"]

plt.hist(purchase_time, alpha=0.5, label="Purchase")
plt.hist(non_purchase_time, alpha=0.5, label="No Purchase")

plt.xlabel("Time on Page")
plt.ylabel("Count")

plt.legend()

plt.savefig("analysis/purchase_analysis.png")

plt.close()

# 구매 예측 모델

# 컬럼 선택
X = df[
    [
        "click",
        "user_age",
        "product_price",
        "product_rating",
        "time_on_page",
        "product_type",
        "user_gender",
        "user_location"
    ]
]
X = pd.get_dummies(X)

y = df["purchase"]

#train / test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# RF 모델 생성
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# ROC Curve / AUC
from sklearn.metrics import roc_curve, roc_auc_score

auc = roc_auc_score(y_test, y_prob)

print("AUC:", auc)

fpr, tpr, thresholds = roc_curve(y_test, y_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("analysis/roc_curve.png")
plt.close()

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print("정확도:", accuracy)

# confusion matrix
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print(cm)

# classification report
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

# feature importance
importance = model.feature_importances_

feature_names = X.columns

for name, score in zip(feature_names, importance):
    print(name, ":", score)

# 그래프로 시각화
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

plt.bar(feature_names, importance)

plt.xlabel("Features")
plt.ylabel("Importance")

plt.savefig("analysis/feature_importance.png")

plt.close()

# 상위 구매 사용자 확인
result_df = X_test.copy()

result_df["actual_purchase"] = y_test.values
result_df["purchase_probability"] = y_prob

print(
    result_df.sort_values(
        by="purchase_probability",
        ascending=False
    ).head(10)
)

# 추천 대상 추출
recommend_users = result_df[
    result_df["purchase_probability"] >= 0.45
]

print(recommend_users.head(10))

# 모델 저장
import joblib

joblib.dump(model, "models/random_forest_model.pkl")