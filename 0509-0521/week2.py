import numpy as np
import pandas as pd
from pyarrow import csv


##########################################################################################

import argparse
import functools

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--add', type=int, nargs='+', metavar='N', help='더할 숫자')
parser.add_argument('-m', '--mul', type=int, nargs='+', metavar='N', help='곱할 숫자')

args = parser.parse_args()

if args.add:
    print("합은 %d입니다." % functools.reduce(lambda x, y: x + y, args.add))
if args.mul:
    print("곱은 %d입니다." % functools.reduce(lambda x, y: x * y, args.mul))
##########################################################################################

# pyarrow로 load
df = csv.read_csv('user_data.csv').to_pandas()

# 데이터타입 변경
df = df.astype({'credit_card_number':'str'})

# 가명처리 함수 정의
def anonymize_name(name):
    return name[0] + '*'*2

def anonymize_address(address):
    parts = address.split(' ', 1)
    return parts[0]

def anonymize_postcode(postcode):
    return '*'*5

def anonymize_company(company):
    return '*'*8

def anonymize_phone_number(phone_number):
    parts = phone_number.rsplit('-', 1)
    return parts[0] + '-' + '*'*4

def anonymize_email(email):
    local, domain = email.split('@')
    return '*'*5 + '@' + domain

def anonymize_credit_card_number(credit_card_number):
    return  credit_card_number[:6] + '*'*10


# 가명처리 함수 적용
df['name'] = df['name'].apply(anonymize_name)
df['address'] = df['address'].apply(anonymize_address)
df['postcode'] = df['postcode'].apply(anonymize_postcode)
df['company'] = df['company'].apply(anonymize_postcode)
df['phone_number'] = df['phone_number'].apply(anonymize_phone_number)
df['email'] = df['email'].apply(anonymize_email)
df['credit_card_number'] = df['credit_card_number'].apply(anonymize_credit_card_number)

# 'ip_address' 칼럼의 항목들을 랜덤으로 섞기
df['ip_address'] = np.random.permutation(df['ip_address'].values)

# 불필요한 칼럼 삭제
df = df.drop(columns=['total_int'])
df = df.drop(columns=['total_float'])

print(df.head(11))
df.to_csv("week01.csv", index=False)