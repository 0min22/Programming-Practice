import pandas as pd
df = pd.read_csv("data.csv")

print("=== 원본 데이터 ===")
print(df)

#열 선택
print("\n=== age, score만 선택 ===")
print(df[["age", "score"]])

#결측치 확인
print("\n=== 결측치 확인 ===")
print(df.isnull().sum())

#조건 필터링
print("\n=== 나이 21 이상 ===")
print(df[df["age"] > 21])

