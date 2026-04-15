#pandas 사용
import pandas as pd

#csv 읽기
df = pd.read_csv("data.csv")

#데이터 확인
print("=== head ===")
print(df.head())

print("\n=== info ===")
print(df.info())

print("\n=== describe ===")
print(df.describe())