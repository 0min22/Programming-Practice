import pandas as pd
import matplotlib.pyplot as plt

#데이터 읽기
df = pd.read_csv("data.csv")

#데이터 전처리
print("=== 결측치 확인 ===")
print(df.isnull().sum())

#간단 분석
print("\n=== 나이 21 이상 ===")
print(df[df["age"] >= 21])

#시각화 1 (score)
plt.figure()
plt.hist(df["score"])
plt.title("Score Distribution")
plt.xlabel("score")
plt.ylabel("count")
plt.show()

#시각화 2 (age)
age_count = df["age"].value_counts().sort_index()
plt.figure()
plt.bar(age_count.index, age_count.values)
plt.title("Age Count")
plt.xlabel("age")
plt.ylabel("count")
plt.show()