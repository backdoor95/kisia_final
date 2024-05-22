import argparse

# ArgumentParser 객체 생성
parser = argparse.ArgumentParser()
# --verbosity 인자 추가
parser.add_argument("--verbosity", help="increase output verbosity")
# 명령 줄 인자 파싱
args = parser.parse_args()

# 포맷 문자열 내에 %s 형식 지정자 추가
print("verbosity = %s" % (args.verbosity))

# verbosity 인자가 설정된 경우 출력
if args.verbosity:
    print("verbosity turned on")

