
# Import pandas
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from folium import plugins

# reading csv file 
# terminal에서 실행중인 경로를 일치시켜야함. 
# encoding 한글 에러 발생시 encoding ='cp949' 를 사용할 것
df = pd.read_csv("sample.csv", encoding='cp949')
print(df.head())

# 한글 깨짐 sol
plt.rcParams['font.family'] = 'Malgun Gothic'

# 고유한 지역 목록 추출
#df['지역'] = df['주소'].apply(lambda x: x.split()[0])
# 주소에서 첫 번째 단어(지역) 추출 및 '경기도'와 '경기' 통일
df['지역'] = df['주소'].apply(lambda x: x.split()[0].replace('경기도', '경기'))

# 각 지역의 사람 수 계산
region_counts = df['지역'].value_counts()

# 파이차트 그리기
plt.figure(figsize=(10, 8))
region_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('지역별 사람 수 비율')
plt.ylabel('')  # y축 레이블 제거
plt.show()

# 막대 그래프 그리기
plt.figure(figsize=(12, 8))
region_counts.plot(kind='bar', color='skyblue')
plt.title('지역별 사람 수')
plt.xlabel('지역')
plt.ylabel('사람 수')
plt.xticks(rotation=45)
plt.show()

# 지도에 비율 표시하기
# 지역별 중심 좌표 (위도, 경도)를 사전에 정의합니다.
# 실제 프로젝트에서는 이 데이터를 외부 파일에서 로드하거나 API를 사용하여 가져올 수 있습니다.
region_coords = {
    '서울': [37.5665, 126.9780],
    '경기': [37.436317, 127.550802],
    '부산': [35.1796, 129.0756],
    '대구': [35.8714, 128.6014],
    '인천': [37.4563, 126.7052],
    '광주': [35.1595, 126.8526],
    '대전': [36.3504, 127.3845],
    '울산': [35.5392, 129.3114],
    '세종': [36.4877, 127.2817],
    '강원': [37.8228, 128.1555],
    '충북': [36.6358, 127.4913],
    '충남': [36.5184, 126.8000],
    '전북': [35.7175, 127.1530],
    '전남': [34.8679, 126.9910],
    '경북': [36.4919, 128.8889],
    '경남': [35.4606, 128.2132],
    '제주': [33.4890, 126.4983],
}

# 지도 생성 (중심을 서울로 설정)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=7)

# 원형 마커 크기를 조정하기 위한 스케일링 팩터
scale_factor = 0.1  # 이 값을 조정하여 원 크기를 변경합니다.

# 각 지역에 원 추가
for region, count in region_counts.items():
    if region in region_coords:
        folium.Circle(
            location=region_coords[region],
            radius=count * 10,  # 반경은 인구 수에 비례하여 설정 (단위: 미터)
            popup=f'{region}: {count}명',
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        ).add_to(m)

# 지도 저장
m.save('region_counts_map.html')


