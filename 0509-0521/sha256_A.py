import numpy as np
import pandas as pd
import os
from pyarrow import csv
import hashlib
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-input", help="대상 CSV 파일명")
parser.add_argument("-output", help="출력 대상 파일명")
parser.add_argument("-algorithm", 
                    help="비식별 알고리즘 선택\n"
                    +"A:주요정보+솔트 => 암호화\n"
                    +"B:순서보존 암호화\n"
                    +"C:형태보존 암호화\n")
parser.add_argument("-option", help="비식별 알고리즘 행동 선택(마스킹시 뒷자리(1)/앞자리(2)/숫자(3) 등)")

args = parser.parse_args()


##########################################################################################
##########################################################################################
#컬럼 : postcode| company	|job	|phone_number	|email	|user_name	|ip_address	|credit_card_number|	date	|total_int	|total_float

# pyarrow로 load
inputFile = args.input
outputFile = args.output
print(f"input file Name: {inputFile}, ouotput file name: {outputFile}")

df = csv.read_csv(inputFile).to_pandas()

# 모든 열의 데이터 타입을 문자열로 변환합니다.
df = df.astype(str)

# user_name, email, phone_number, credit_card_number와 salt - encryption(SHA256)
# 해시화 및 솔트 생성 함수 정의
def hash_with_salt(data, salt):
    # 데이터를 결합하고 해시화합니다.
    combined = data + salt
    return hashlib.sha256(combined.encode()).hexdigest()

# 각 레코드마다 솔트를 생성하고 해시화합니다.
def hash_sensitive_data(row):
    salt = os.urandom(16).hex()  # 16 바이트 솔트를 생성하고 16진수 문자열로 변환
    user_data = row['name'] + row['email'] + row['phone_number'] + row['credit_card_number']
    hashed_value = hash_with_salt(user_data, salt)
    return hashed_value, salt


if args.algorithm == 'A':
    print("algorithm A start")
    # 새로운 컬럼을 추가합니다.
    df[['hashed_value', 'salt']] = df.apply(lambda row: pd.Series(hash_sensitive_data(row)), axis=1)
    # 원래 민감한 정보를 포함한 컬럼을 삭제합니다.
    df = df.drop(columns=['name', 'email', 'phone_number', 'credit_card_number'])
    ##### 
    df.to_csv(outputFile, index=False)
    print("algorithm A end")






