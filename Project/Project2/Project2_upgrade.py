# Project2_upgrade.py

# 데이터 확인
import pandas as pd

df = pd.read_csv("data/Project2_data.csv")

print(df.info())
print(df.describe())
print(df.isnull().sum())

print("구매 개수")
print(df["purchase"].value_counts())

print("구매 비율")
print(df["purchase"].value_counts(normalize=True))
print(df["purchase"].mean())

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

# train / test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 스케일링
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 평가에 필요한 도구
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# =========================
# 1. Logistic Regression
# =========================

from sklearn.linear_model import LogisticRegression

logistic_model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000
)

logistic_model.fit(X_train_scaled, y_train)

logistic_prob = logistic_model.predict_proba(X_test_scaled)[:, 1]
logistic_pred = (logistic_prob >= 0.5).astype(int)

logistic_accuracy = accuracy_score(y_test, logistic_pred)
logistic_auc = roc_auc_score(y_test, logistic_prob)

print("\n===== Logistic Regression =====")
print("Accuracy:", logistic_accuracy)
print("AUC:", logistic_auc)
print(confusion_matrix(y_test, logistic_pred))
print(classification_report(y_test, logistic_pred))

fpr, tpr, thresholds = roc_curve(y_test, logistic_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"Logistic AUC = {logistic_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Logistic Regression")
plt.legend()
plt.savefig("analysis/roc_logistic.png")
plt.close()


# =========================
# 2. Decision Tree
# =========================

from sklearn.tree import DecisionTreeClassifier

tree_model = DecisionTreeClassifier(
    random_state=42,
    class_weight="balanced",
    max_depth=5
)

tree_model.fit(X_train, y_train)

tree_prob = tree_model.predict_proba(X_test)[:, 1]
tree_pred = (tree_prob >= 0.5).astype(int)

tree_accuracy = accuracy_score(y_test, tree_pred)
tree_auc = roc_auc_score(y_test, tree_prob)

print("\n===== Decision Tree =====")
print("Accuracy:", tree_accuracy)
print("AUC:", tree_auc)
print(confusion_matrix(y_test, tree_pred))
print(classification_report(y_test, tree_pred))

fpr, tpr, thresholds = roc_curve(y_test, tree_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"Decision Tree AUC = {tree_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Decision Tree")
plt.legend()
plt.savefig("analysis/roc_decision_tree.png")
plt.close()


# =========================
# 3. Random Forest
# =========================

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    max_depth=10,
    min_samples_leaf=5
)

rf_model.fit(X_train, y_train)

rf_prob = rf_model.predict_proba(X_test)[:, 1]
rf_pred = (rf_prob >= 0.5).astype(int)

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_auc = roc_auc_score(y_test, rf_prob)

print("\n===== Random Forest =====")
print("Accuracy:", rf_accuracy)
print("AUC:", rf_auc)
print(confusion_matrix(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

fpr, tpr, thresholds = roc_curve(y_test, rf_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"Random Forest AUC = {rf_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Random Forest")
plt.legend()
plt.savefig("analysis/roc_random_forest.png")
plt.close()

# feature importance
importance = rf_model.feature_importances_

feature_names = X.columns

importance_df = pd.DataFrame(
    {
        "feature": feature_names,
        "importance": importance
    }
)

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print(importance_df)
importance_df.to_csv(
    "analysis/feature_importance.csv",
    index=False
)

plt.figure(figsize=(10, 5))

plt.bar(
    importance_df["feature"],
    importance_df["importance"]
)

plt.xticks(rotation=45)

plt.xlabel("Feature")
plt.ylabel("Importance")

plt.title("Random Forest Feature Importance")

plt.tight_layout()

plt.savefig("analysis/feature_importance.png")

plt.close()


# =========================
# 4. KNN
# =========================

from sklearn.neighbors import KNeighborsClassifier

knn_model = KNeighborsClassifier(
    n_neighbors=5
)

knn_model.fit(X_train_scaled, y_train)

knn_prob = knn_model.predict_proba(X_test_scaled)[:, 1]
knn_pred = (knn_prob >= 0.5).astype(int)

knn_accuracy = accuracy_score(y_test, knn_pred)
knn_auc = roc_auc_score(y_test, knn_prob)

print("\n===== KNN =====")
print("Accuracy:", knn_accuracy)
print("AUC:", knn_auc)
print(confusion_matrix(y_test, knn_pred))
print(classification_report(y_test, knn_pred))

fpr, tpr, thresholds = roc_curve(y_test, knn_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"KNN AUC = {knn_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - KNN")
plt.legend()
plt.savefig("analysis/roc_knn.png")
plt.close()


# =========================
# 5. SVM
# =========================

from sklearn.svm import SVC

svm_model = SVC(
    kernel="rbf",
    probability=True,
    class_weight="balanced",
    random_state=42
)

svm_model.fit(X_train_scaled, y_train)

svm_prob = svm_model.predict_proba(X_test_scaled)[:, 1]
svm_pred = (svm_prob >= 0.5).astype(int)

svm_accuracy = accuracy_score(y_test, svm_pred)
svm_auc = roc_auc_score(y_test, svm_prob)

print("\n===== SVM =====")
print("Accuracy:", svm_accuracy)
print("AUC:", svm_auc)
print(confusion_matrix(y_test, svm_pred))
print(classification_report(y_test, svm_pred))

fpr, tpr, thresholds = roc_curve(y_test, svm_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"SVM AUC = {svm_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - SVM")
plt.legend()
plt.savefig("analysis/roc_svm.png")
plt.close()


# =========================
# 모델 성능 요약
# =========================

summary = pd.DataFrame(
    {
        "model": [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "KNN",
            "SVM"
        ],
        "accuracy": [
            logistic_accuracy,
            tree_accuracy,
            rf_accuracy,
            knn_accuracy,
            svm_accuracy
        ],
        "auc": [
            logistic_auc,
            tree_auc,
            rf_auc,
            knn_auc,
            svm_auc
        ]
    }
)

print("\n===== Model Performance Summary =====")
print(summary)

summary.to_csv("analysis/model_summary.csv", index=False)

plt.figure()
plt.bar(summary["model"], summary["auc"])
plt.xlabel("Model")
plt.ylabel("AUC")
plt.title("Model AUC Comparison")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("analysis/model_auc_comparison.png")
plt.close()

# 가장 좋은 모델 저장
import joblib

best_index = summary["auc"].idxmax()
best_model_name = summary.loc[best_index, "model"]

print("\nBest Model:", best_model_name)

if best_model_name == "Logistic Regression":
    joblib.dump(logistic_model, "models/best_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

elif best_model_name == "Decision Tree":
    joblib.dump(tree_model, "models/best_model.pkl")

elif best_model_name == "Random Forest":
    joblib.dump(rf_model, "models/best_model.pkl")

elif best_model_name == "KNN":
    joblib.dump(knn_model, "models/best_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

elif best_model_name == "SVM":
    joblib.dump(svm_model, "models/best_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

joblib.dump(X.columns, "models/model_columns.pkl")