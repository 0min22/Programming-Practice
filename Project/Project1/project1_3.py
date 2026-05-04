import cv2
import numpy as np
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression


# =========================
# 1. 경로 설정
# =========================

base_path = "wzt_data"
os.makedirs(base_path + "/class_0", exist_ok=True)
os.makedirs(base_path + "/class_1", exist_ok=True)
os.makedirs("results", exist_ok=True)


# =========================
# 2. WZT-like 이미지 생성
# =========================

def create_wzt_template():
    img = np.ones((256, 256), dtype=np.uint8) * 255

    # 4 x 4 grid
    for i in range(1, 4):
        cv2.line(img, (0, i * 64), (256, i * 64), 0, 1)
    for j in range(1, 4):
        cv2.line(img, (j * 64, 0), (j * 64, 256), 0, 1)

    return img


def draw_realistic_wzt_pattern(img, label):
    """
    더 어려운 WZT-like synthetic data 생성.
    class_0과 class_1이 완전히 다르지 않고 일부 feature가 겹치도록 설계.
    """

    # 두 class 모두 비슷한 개수의 cell 사용
    used_cells = random.sample(range(16), random.randint(6, 11))

    for cell in used_cells:
        row = cell // 4
        col = cell % 4

        x_base = col * 64
        y_base = row * 64

        cx = x_base + random.randint(15, 49)
        cy = y_base + random.randint(15, 49)

        # class 차이를 약하게 둠
        if label == 0:
            stroke_count = random.randint(1, 3)
            shift_strength = random.randint(0, 8)
            break_prob = 0.15
        else:
            stroke_count = random.randint(2, 4)
            shift_strength = random.randint(4, 14)
            break_prob = 0.35

        for _ in range(stroke_count):
            shape_type = random.choice(["line", "circle", "curve"])

            dx = random.randint(-shift_strength, shift_strength)
            dy = random.randint(-shift_strength, shift_strength)

            if shape_type == "line":
                x1 = np.clip(cx - random.randint(8, 22) + dx, x_base + 3, x_base + 61)
                y1 = np.clip(cy - random.randint(8, 22) + dy, y_base + 3, y_base + 61)
                x2 = np.clip(cx + random.randint(8, 22) + dx, x_base + 3, x_base + 61)
                y2 = np.clip(cy + random.randint(8, 22) + dy, y_base + 3, y_base + 61)

                if random.random() < break_prob:
                    mx = (x1 + x2) // 2
                    my = (y1 + y2) // 2
                    cv2.line(img, (int(x1), int(y1)), (int(mx - 3), int(my - 3)), 0, 1)
                    cv2.line(img, (int(mx + 3), int(my + 3)), (int(x2), int(y2)), 0, 1)
                else:
                    cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), 0, random.choice([1, 2]))

            elif shape_type == "circle":
                radius = random.randint(5, 13)
                cv2.circle(img, (int(cx + dx), int(cy + dy)), radius, 0, random.choice([1, 2]))

            else:
                pts = np.array([
                    [cx - 15 + dx, cy + random.randint(-10, 10) + dy],
                    [cx + dx, cy + random.randint(-15, 15) + dy],
                    [cx + 15 + dx, cy + random.randint(-10, 10) + dy]
                ], np.int32)
                cv2.polylines(img, [pts], False, 0, random.choice([1, 2]))

    # 공통 noise: 두 class 모두에 들어감
    for _ in range(random.randint(3, 8)):
        x1, y1 = random.randint(0, 255), random.randint(0, 255)
        x2, y2 = x1 + random.randint(-15, 15), y1 + random.randint(-15, 15)
        cv2.line(img, (x1, y1), (np.clip(x2, 0, 255), np.clip(y2, 0, 255)), 0, 1)

    # blur 또는 erosion/dilation 랜덤 적용
    if random.random() < 0.3:
        img = cv2.GaussianBlur(img, (3, 3), 0)

    if random.random() < 0.25:
        kernel = np.ones((2, 2), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)

    if random.random() < 0.25:
        kernel = np.ones((2, 2), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)

    return img

def generate_data(n=150):
    for i in range(n):
        img0 = create_wzt_template()
        img0 = draw_realistic_wzt_pattern(img0, label=0)
        cv2.imwrite(f"{base_path}/class_0/img_{i}.png", img0)

        img1 = create_wzt_template()
        img1 = draw_realistic_wzt_pattern(img1, label=1)
        cv2.imwrite(f"{base_path}/class_1/img_{i}.png", img1)

    print("어려운 데이터 생성 완료")


# =========================
# 3. Feature Extraction
# =========================

def extract_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))

    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    black_ratio = np.sum(thresh == 255) / (128 * 128)

    edges = cv2.Canny(img, 50, 150)
    edge_ratio = np.sum(edges > 0) / (128 * 128)

    mean_intensity = np.mean(img)
    std_intensity = np.std(img)

    coords = np.column_stack(np.where(thresh == 255))

    if len(coords) > 0:
        center_y, center_x = np.mean(coords, axis=0)
        center_x = center_x / 128
        center_y = center_y / 128

        x_min, y_min = np.min(coords[:, 1]), np.min(coords[:, 0])
        x_max, y_max = np.max(coords[:, 1]), np.max(coords[:, 0])

        bbox_area = ((x_max - x_min + 1) * (y_max - y_min + 1)) / (128 * 128)
        aspect_ratio = (x_max - x_min + 1) / (y_max - y_min + 1)
    else:
        center_x, center_y = 0, 0
        bbox_area = 0
        aspect_ratio = 0

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_count = len(contours)

    # horizontal / vertical density
    horizontal_density = np.sum(thresh == 255, axis=1)
    vertical_density = np.sum(thresh == 255, axis=0)

    horizontal_density_std = np.std(horizontal_density)
    vertical_density_std = np.std(vertical_density)

    # cell occupancy: 4 x 4 grid 중 그림이 들어간 칸 개수
    cell_count = 0
    cell_ratios = []

    for r in range(4):
        for c in range(4):
            cell = thresh[r * 32:(r + 1) * 32, c * 32:(c + 1) * 32]
            ratio = np.sum(cell == 255) / (32 * 32)
            cell_ratios.append(ratio)
            if ratio > 0.01:
                cell_count += 1

    cell_occupancy_count = cell_count
    cell_density_std = np.std(cell_ratios)

    # symmetry score: 좌우 대칭 정도
    left = thresh[:, :64]
    right = cv2.flip(thresh[:, 64:], 1)
    symmetry_score = np.mean(np.abs(left.astype(float) - right.astype(float))) / 255

    return [
        black_ratio,
        edge_ratio,
        mean_intensity,
        std_intensity,
        center_x,
        center_y,
        contour_count,
        bbox_area,
        aspect_ratio,
        horizontal_density_std,
        vertical_density_std,
        cell_occupancy_count,
        cell_density_std,
        symmetry_score
    ]


def build_dataset():
    data = []
    labels = []

    for label in ["class_0", "class_1"]:
        folder = os.path.join(base_path, label)

        for file in os.listdir(folder):
            if file.endswith(".png"):
                path = os.path.join(folder, file)
                features = extract_features(path)
                data.append(features)
                labels.append(0 if label == "class_0" else 1)

    columns = [
        "black_ratio",
        "edge_ratio",
        "mean_intensity",
        "std_intensity",
        "center_x",
        "center_y",
        "contour_count",
        "bbox_area",
        "aspect_ratio",
        "horizontal_density_std",
        "vertical_density_std",
        "cell_occupancy_count",
        "cell_density_std",
        "symmetry_score"
    ]

    df = pd.DataFrame(data, columns=columns)
    df["label"] = labels

    df.to_csv("results/wzt_features.csv", index=False)
    print("Feature CSV 저장 완료: results/wzt_features.csv")

    return df


# =========================
# 4. 모델 비교
# =========================

def evaluate_models(df):
    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "SVM": SVC(kernel="rbf", random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000)
    }

    results = []

    for name, model in models.items():
        if name in ["KNN", "SVM", "Logistic Regression"]:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        pre = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        results.append([name, acc, pre, rec, f1])

        print("\n====================")
        print(name)
        print("====================")
        print("Accuracy:", acc)
        print("Precision:", pre)
        print("Recall:", rec)
        print("F1:", f1)

        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(4, 3))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title(f"{name} Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        plt.savefig(f"results/{name.replace(' ', '_')}_confusion_matrix.png")
        plt.close()

    result_df = pd.DataFrame(
        results,
        columns=["Model", "Accuracy", "Precision", "Recall", "F1"]
    )

    result_df.to_csv("results/model_comparison.csv", index=False)

    print("\n\n===== Model Comparison =====")
    print(result_df)

    return result_df, X_train, X_test, y_train, y_test


# =========================
# 5. Feature Importance
# =========================

def analyze_feature_importance(df):
    X = df.drop("label", axis=1)
    y = df["label"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    importance_df.to_csv("results/feature_importance.csv", index=False)

    print("\n\n===== Feature Importance =====")
    print(importance_df)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=importance_df, x="Importance", y="Feature")
    plt.title("Random Forest Feature Importance")
    plt.tight_layout()
    plt.savefig("results/feature_importance.png")
    plt.close()

    return importance_df


# =========================
# 6. Ablation Study
# =========================

def ablation_study(df):
    feature_sets = {
        "Basic": [
            "black_ratio",
            "edge_ratio"
        ],
        "Spatial": [
            "center_x",
            "center_y",
            "bbox_area",
            "aspect_ratio"
        ],
        "Complexity": [
            "contour_count",
            "horizontal_density_std",
            "vertical_density_std"
        ],
        "Cell-based": [
            "cell_occupancy_count",
            "cell_density_std"
        ],
        "All Features": list(df.drop("label", axis=1).columns)
    }

    y = df["label"]
    ablation_results = []

    for set_name, features in feature_sets.items():
        X = df[features]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        ablation_results.append([set_name, acc, f1])

    ablation_df = pd.DataFrame(
        ablation_results,
        columns=["Feature Set", "Accuracy", "F1"]
    )

    ablation_df.to_csv("results/ablation_study.csv", index=False)

    print("\n\n===== Ablation Study =====")
    print(ablation_df)

    plt.figure(figsize=(7, 4))
    sns.barplot(data=ablation_df, x="Feature Set", y="F1")
    plt.title("Ablation Study by Feature Set")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("results/ablation_study.png")
    plt.close()

    return ablation_df


# =========================
# 7. Main 실행
# =========================

if __name__ == "__main__":
    generate_data(n=150)

    df = build_dataset()

    print("\n===== Dataset Sample =====")
    print(df.head())

    result_df, X_train, X_test, y_train, y_test = evaluate_models(df)

    importance_df = analyze_feature_importance(df)

    ablation_df = ablation_study(df)

    print("\n\n프로젝트 실행 완료")
    print("결과 파일은 results 폴더에 저장되었습니다.")