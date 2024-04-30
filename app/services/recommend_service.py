# Main Section
from fastapi import requests
import pandas as pd
import requests


def get_cultural_event_list():
    base_url = "https://ticats.site/api/cultural-events"
    try:
        response = requests.get(base_url + "?type=ALL&page=1&size=100")
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        return df

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        print(f"Error converting to DataFrame: {e}")
        return None

# recommend func 
import pandas as pd
from bs4 import BeautifulSoup
import warnings; warnings.filterwarnings('ignore')
        
def df_setting(df):
    pd.set_option('max_colwidth', 100)

    if '영화명' in df.columns: # if 영화
        df = df[df['평점 참여수'] != '등록전 ']
        df['평점 참여수'] = df['평점 참여수'].astype(int)
        df['개봉일'] = pd.to_datetime(df['개봉일'])
        df = df[['영화명', '개봉일', '장르', '평점']] #평점은 없어질수도 있음
    
    else:
        df = df[df['시작일'] != '오픈런']
        df = df[df['종료일'] != '오픈런']
        df['시작일'] = pd.to_datetime(df['시작일'])
        df['종료일'] = pd.to_datetime(df['종료일'])
        df = df[['공연명', '장르', '시작일', '종료일']]

    return df



def recommend_contents(df, inputs, genres): 
    recommended_contents = pd.DataFrame()

    if '영화명' in df.columns: # if 영화
        if all(word in genres for word in inputs): # input이 장르일 경우
            for genre in inputs:
                filtered_df = df[(df['장르'] == genre) & (df['평점'] >= 5)] #인풋과 같은 장르이면서 평점이 5점 이상인 작품만 필터링
                latest_movies = filtered_df.sort_values(by='개봉일', ascending=False).head(3) # 개봉일 순 정렬(3개)
                if len(filtered_df) >= 3:
                    random_movies = filtered_df.sample(n=6, replace=False).sort_values(by='평점', ascending=False).head(2) #랜덤 2개 (가중평점 순 정렬 or 평점 순 정렬 선택 가능)
                else:
                    random_movies = filtered_df.sort_values(by='평점', ascending=False).head(2)
                recommended_contents = pd.concat([recommended_contents, latest_movies, random_movies])

        else: # input이 제목일 경우
            for title_idx in inputs:
                try:
                    title = df['영화명'].loc[title_idx]
                except:
                    print(f'exception: 인덱스 범위를 벗어났습니다, {title_idx}')
                    break
                genre = df.loc[df['영화명'] == title, '장르'].iloc[0] # 인풋과 같은 장르인 작품만 필터링
                recommend_candidate = df[df['영화명'] != title] # 기준 작품 제외
                filtered_df = recommend_candidate[(recommend_candidate['장르'] == genre) & (recommend_candidate['평점'] >= 5)] #사용자가 본 영화와 같은 장르이면서 평점이 5점 이상인 작품만 필터링
                latest_movies = filtered_df.sort_values(by='개봉일', ascending=False).head(3) # 개봉일 순 정렬(3개)
                if len(filtered_df) >= 3:
                    random_movies = filtered_df.sample(n=6, replace=False).sort_values(by='평점', ascending=False).head(2) #랜덤 2개 (평점 순 정렬)
                else:
                    random_movies = filtered_df.sort_values(by='평점', ascending=False).head(2)
                recommended_contents = pd.concat([recommended_contents, latest_movies, random_movies]) 
                
        recommended_contents = recommended_contents.drop_duplicates(subset=['영화명']).index

#----------------------------------------------------------------------------------------------------------------

    else: # if 뮤지컬
        if all(word in genres for word in inputs): # input이 장르일 경우
            for genre in inputs:
                filtered_df = df[df['장르'] == genre] #인풋과 같은 장르인 작품만 필터링
                latest_musicals = filtered_df.sort_values(by='종료일', ascending=False).reset_index(drop=True).head(5) # 종료일 순 정렬(5개)
                recommended_contents = pd.concat([recommended_contents, latest_musicals]).reset_index(drop=True)

        else: # input이 제목일 경우
            for title_idx in inputs:
                try:
                    title = df['공연명'].loc[title_idx]
                except:
                    print(f'exception: 인덱스 범위를 벗어났습니다, {title_idx}')
                    break
                genre = df.loc[df['공연명'] == title, '장르'].iloc[0] #인풋과 같은 장르인 작품만 필터링
                recommend_candidate = df[df['공연명'] != title] #기준 작품 제외
                filtered_df = recommend_candidate[(recommend_candidate['장르'] == genre)]
                latest_musicals = filtered_df.sort_values(by='종료일', ascending=False).head(5) # 종료일 순 정렬(5개)
                recommended_contents = pd.concat([recommended_contents, latest_musicals])

        recommended_contents = recommended_contents.drop_duplicates(subset=['공연명']).index

    return recommended_contents 


# Example usage_movie
movies_df = pd.read_csv('/Users/art029/Desktop/ticats/콘텐츠 추천/dataset/real/KOBIS_rating_dropna.csv')
input_df = df_setting(movies_df)

df_genres = ['드라마', '범죄', '미스터리', '액션', '애니메이션', '사극', '판타지', '스릴러', '코미디','어드벤처', 'SF', '기타', '뮤지컬', '다큐멘터리', '공포(호러)', '멜로/로맨스', '공연', '전쟁','가족', '서부극(웨스턴)']
usr_genres = ['드라마', '코미디', '액션']
titles = [5, 80, 4]

recommendation_result_t = recommend_contents(input_df, titles, df_genres)
recommendation_result_g = recommend_contents(input_df, usr_genres, df_genres)

print(f'input이 제목일 경우\n {recommendation_result_t.values}')
print(f'\ninput이 장르일 경우\n {recommendation_result_g.values}')

check = input_df.loc[recommendation_result_t]
check.head(20)


# Example usage_muscial
musical_df = pd.read_excel('/Users/art029/Desktop/ticats/콘텐츠 추천/dataset/real/KOPIS.xlsx')
input_df = df_setting(musical_df)

df_genres = ['복합', '연극', '무용', '서커스/마술', '뮤지컬', '한국음악(국악)', '대중음악', '서양음악(클래식)']
usr_genres = ['연극', '무용']
titles = [8, 10, 0]

recommendation_result_t = recommend_contents(input_df, titles, df_genres)
recommendation_result_g = recommend_contents(input_df, usr_genres, df_genres)

print(f'input이 제목일 경우\n {recommendation_result_t.values}')
print(f'\ninput이 장르일 경우\n {recommendation_result_g.values}')

check = input_df.loc[recommendation_result_t]
check.head(20)