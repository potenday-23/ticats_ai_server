# Main Section
from fastapi import requests
import requests

import numpy as np
import pandas as pd
from collections import Counter
import warnings; warnings.filterwarnings('ignore')
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from typing import List

import warnings;
warnings.filterwarnings('ignore')



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



def df_loader(path):
    content_info_df = pd.read_csv(path)
    content_info_df = content_info_df[['culturalEventId', 'culturalEventTitle', 'content']]

    # 전처리
    content_info_df['content'] = content_info_df['content'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', regex=True)
    content_info_df = content_info_df.replace({' ': np.nan})  
    content_info_df.dropna(how='any', inplace=True)
    content_info_df = content_info_df.reset_index(drop=True)

    # 컬럼 추가
    content_info_df['token'] = ''
    content_info_df['topic'] = ''
    content_info_df['sentiment'] = ''

    return content_info_df



def content_recommender(base_df: pd.DataFrame, content_id_lst: List[int]) -> List[int]:
    '''
    input으로 들어온 id에 해당하는 작품들의 감정 키워드 중 표본(최빈값 2개)을 선정하고,
    이 표본들과 유사한 감정이 나타난 순으로 id를 재정렬
    '''
    # 코사인 유사도 측정
    count_vect = CountVectorizer(ngram_range=(1, 2), lowercase=False)
    genre_mat = count_vect.fit_transform(base_df['sentiment'])
    genre_sim_sorted_idx = cosine_similarity(genre_mat, genre_mat).argsort()[:, ::-1]

    # input작품들의 감정 키워드 표본 수집
    sentiment_candidates=[]
    for content_id in content_id_lst:
        content_idx = base_df[base_df['culturalEventId'] == content_id].index.values
        similar_indexes = genre_sim_sorted_idx[content_idx, :4]
        similar_indexes = similar_indexes[similar_indexes != content_idx].reshape(-1)
        for idx in similar_indexes:
            sentiment_candidates.append(base_df.loc[idx, 'sentiment'].split(', ')[0])
            sentiment_candidates.append(base_df.loc[idx, 'sentiment'].split(', ')[1])

    recommend_sentiment = ', '.join([item[0].strip() for item in Counter(sentiment_candidates).most_common(2)])
    base_content = base_df[base_df['sentiment'] == recommend_sentiment].sample(n=1).index.values

    # base_content와 유사한 순으로 나열
    similar_indexes = genre_sim_sorted_idx[base_content, :]
    similar_indexes = similar_indexes[similar_indexes != content_idx].reshape(-1)

    # culturalEventId값 반환
    idx_to_id_lst = []
    for idx in similar_indexes:
        idx_to_id_lst.append(base_df['culturalEventId'].iloc[idx])
    return idx_to_id_lst