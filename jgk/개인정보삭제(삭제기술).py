import numpy as np
import pandas as pd
from pyarrow import csv

# 파일 경로 지정
file_path = r"C:\Users\82106\OneDrive\바탕 화면\kisia_final\jgk\user_data_small.csv"

# pyarrow로 CSV 파일 로드
df = csv.read_csv(file_path).to_pandas()

# 데이터타입 변경
df = df.astype({'credit_card_number': 'str'})

# 가명처리 함수 정의 [세부기술: 부분 삭제]
def anonymize_address(address): 
    parts = addres
# 가명처리 함수 적용 [세부기술: 부분 삭제]
df['address'] = df['address'].apply(anonymize_address)
    s.split(' ', 1)
    return parts[0]


# 다른 정보와 뚜렷하게 구분되는 행 항목 삭제 [세부기술: 행 항목 삭제]
df = df.drop(columns=['total_int'])
df = df.drop(columns=['total_float'])

# 'phone_number' 개인정보 해당 행 단순 삭제 [세부기술: 삭제]
df = df[df['phone_number'].isna()]

# 'credit_card_number' 특이정보 해당 행 삭제 [세부기술: 로컬 삭제]
df = df[df['credit_card_number'].isna()]

# 결과 확인 (상위 11개 행)
print(df.head(11))

# 수정된 CSV 파일 저장
output_path = r"C:\Users\82106\OneDrive\바탕 화면\kisia_final\jgk\output.csv"
df.to_csv(output_path, index=False)