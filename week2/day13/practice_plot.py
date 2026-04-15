import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

#점수 히스토그램 시각화
plt.figure()
plt.hist(df["score"])
plt.title("Score 시각화")
plt.xlabel("score")
plt.ylabel("count")
plt.show()

#나이별 인원수 막대그래프
age_count = df["age"].value_counts().sort_index()
plt.figure()
plt.bar(age_count.index, age_count.values)
plt.title("Age 카운트")
plt.xlabel("age")
plt.ylabel("count")
plt.show()
