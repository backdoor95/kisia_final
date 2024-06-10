import numpy as np
import pandas as pd
import os
from pyarrow import csv
import hashlib
import argparse
import matplotlib

##############################################################################################
# 가명처리 함수 정의
def anonymize_name_back(name):
    return name[0] + '*'*2
def anonymize_name_front(name):
    return '*'*2 + name[2]

def anonymize_address(address):
    parts = address.split(' ', 1)
    return parts[0]

def anonymize_postcode(postcode):
    return '*'*5

def anonymize_company(company):
    return '*'*8

def anonymize_phone_number_back(phone_number):
    parts = phone_number.rsplit('-', 1)
    return parts[0] + '-' + '*'*4

def anonymize_phone_number_front(phone_number):
    parts = phone_number.split('-', 1)
    return '*'*3+'-'+'*'*4 + parts[1]

def anonymize_email(email):
    local, domain = email.split('@')
    return '*'*5 + '@' + domain

def anonymize_credit_card_number_back(credit_card_number):
    return  credit_card_number[:6] + '*'*10

def anonymize_credit_card_number_front(credit_card_number):
    return  '*'*10 + credit_card_number[-6:]
##############################################################################################


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

def masking_front(df):
    df['name'] = df['name'].apply(anonymize_name_back)
    df['phone_number'] = df['phone_number'].apply(anonymize_phone_number_back)
    df['credit_card_number'] = df['credit_card_number'].apply(anonymize_credit_card_number_back)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", help="대상 CSV 파일명")
    parser.add_argument("-output", help="출력 대상 파일명")
    parser.add_argument("-algorithm", 
                        help="비식별 알고리즘 선택\n"
                        +"S:솔트 암호화\n"
                        +"O:순서보존(Order) 암호화\n"
                        +"F:형태보존(Format) 암호화\n")
    parser.add_argument("-option", help="비식별 알고리즘 행동 선택(마스킹시 뒷자리(1)/앞자리(2)/숫자(3) 등)")

    args = parser.parse_args()
    
    # pyarrow로 load
    inputFile = args.input
    outputFile = args.output
    print(f"input file Name: {inputFile}, ouotput file name: {outputFile}")
    
    df = csv.read_csv(inputFile).to_pandas()
    
    # 모든 열의 데이터 타입을 문자열로 변환합니다.
    df = df.astype(str)
    
    if args.algorithm == "S" or args.algorithm == "s":
        print("솔트 암호화 알고리즘 시작")
        # 새로운 컬럼을 추가합니다.
        df[['hashed_value', 'salt']] = df.apply(lambda row: pd.Series(hash_sensitive_data(row)), axis=1)
        # 원래 민감한 정보를 포함한 컬럼을 삭제합니다.
        df = df.drop(columns=['name', 'email', 'phone_number', 'credit_card_number'])
        ##### 
        df.to_csv(outputFile, index=False)# 파일을 저장
        print("솔트 알고리즘 끝")
    elif args.algorithm == "O" or args.algorithm == "o":
        print("순서보존 암호화 알고리즘 시작")

        df.to_csv(outputFile, index=False)# 파일을 저장
        print("순서보존 암호화 알고리즘 끝")
    elif args.algorithm == "F" or args.algorithm == "F":
        print("형태보존 암호화 알고리즘 시작")
        
        df.to_csv(outputFile, index=False)# 파일을 저장
        
        print("형태보존 암호화 알고리즘 끝")
        
    if args.option == '1':
        print("option-1 start")
        masking_front(df)
        df.to_csv(outputFile, index=False)# 파일을 저장 -> 이 부분이 비어있으면 업데이트가 안됨.
        print("option-1 end")

        

        
        

if __name__ == "__main__":
    main()