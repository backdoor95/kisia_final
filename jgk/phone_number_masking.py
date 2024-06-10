import pandas as pd  

df = pd.read_csv('user_data_small.csv')

######## 1 : query 사용해서 전화번호 뒷자리 4개 마스킹 #######

# phone_number 열을 변경
df['phone_number'] = df['phone_number'].str[:-4] + '*'*4

# test 출력 : 처음 5개의 행만 출력
print(df.head())
# 수정된 결과를 output1.csv 파일로 저장
df.to_csv("phone_number_masking.csv")
