import pandas as pd
from collections import Counter
import warnings
from sqlalchemy import select
from app.models.cultural_event import CulturalEvent
from sqlalchemy.orm import Session
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

warnings.filterwarnings('ignore')


class RecommendService:

    def __init__(self, db: Session):
        self.db = db

    def get_cultural_events_df(self):
        '''
        DB에서 Cultural Event 추출
        '''
        stmt = select(CulturalEvent.id, CulturalEvent.title, CulturalEvent.sentiment, CulturalEvent.topic)
        results = self.db.execute(stmt).all()
        return pd.DataFrame(results, columns=["id", "title", "sentiment", "topic"])

    def content_recommender(self, cultural_event_ids: List[int]) -> List[int]:
        '''
        input으로 들어온 id에 해당하는 작품들의 감정 키워드 중 표본(최빈값 2개)을 선정하고,
        이 표본들과 유사한 감정이 나타난 순으로 id를 재정렬
        '''
        # DF Load
        base_df = self.get_cultural_events_df()

        # 코사인 유사도 측정
        count_vect = CountVectorizer(ngram_range=(1, 2), lowercase=False)
        genre_mat = count_vect.fit_transform(base_df['sentiment'])
        genre_sim_sorted_idx = cosine_similarity(genre_mat, genre_mat).argsort()[:, ::-1]

        # input작품들의 감정 키워드 표본 수집
        sentiment_candidates = []
        for content_id in cultural_event_ids:
            content_idx = base_df[base_df['id'] == content_id].index.values
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
            idx_to_id_lst.append(base_df['id'].iloc[idx])
        return idx_to_id_lst
