'''
import numpy as np
import pandas as pd
import os
from pyarrow import csv
import hashlib
import argparse
import matplotlib


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-input", help="대상 CSV 파일명")
    parser.add_argument("-output", help="출력 대상 파일명")
    parser.add_argument("-algorithm", 
                        help="비식별 알고리즘 선택\n"
                        +"A:솔트 암호화\n"
                        +"B:순서보존 암호화\n"
                        +"C:형태보존 암호화\n")
    parser.add_argument("-option", help="비식별 알고리즘 행동 선택(마스킹시 뒷자리(1)/앞자리(2)/숫자(3) 등)")

    args = parser.parse_args()
    
        # pyarrow로 load
    inputFile = args.input
    outputFile = args.output
    print(f"input file Name: {inputFile}, ouotput file name: {outputFile}")
    
    df = csv.read_csv(inputFile).to_pandas()
    
    # 모든 열의 데이터 타입을 문자열로 변환합니다.
    df = df.astype(str)

if __name__ == "__main__":
    main()
    
'''