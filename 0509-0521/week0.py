import pandas as pd
import numpy as np

df = pd.read_csv('user_data_small.csv')

######## 1 : query 사용해서 전화번호 뒷자리 4개 마스킹 #######

# phone_number 마스킹
df['phone_number'] = df['phone_number'].str[:-4] + '*'*4

# test 출력 : 처음 5개의 행만 출력
#print(df.head())
# 수정된 결과를 output1.csv 파일로 저장
df.to_csv("output1.csv", index=False)

######## 2 : 열 삭제 ###############
# 랜덤으로 열을 선택
random_column = np.random.choice(df.columns)
print("selected_column 2 = ", random_column)
df = df.drop(columns=[random_column])
# 수정된 결과를 output2.csv 파일로 저장
df.to_csv("output2.csv", index=False)

######## 3 : 열 하나 랜덤 정렬? #########
# 무작위로 열 선택
random_column = np.random.choice(df.columns)
print("selected_column 3 = ", random_column)
# 선택된 열을 기준으로 정렬
df_sorted = df.sort_values(by=random_column)

# 선택한 열의 데이터를 랜덤으로 섞기
random_index = np.random.permutation(df_sorted.index)
print("###############################")
print(random_index)
print("###############################")

df = df_sorted.loc[random_index]

# 원본 데이터프레임에 새로운 열을 추가
df.to_csv("output3.csv", index=False)

# tip
# NumPy 배열의 표현입니다. NumPy 배열은 리스트와 비슷하지만, 요소들 사이에 쉼표로 구분되지 않음. - gpt 
