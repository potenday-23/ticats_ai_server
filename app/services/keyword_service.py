# Modules
import time

from fastapi import HTTPException
import numpy as np
from torch.autograd.profiler import record_function

np.bool = np.bool_
from collections import Counter

import warnings;

warnings.filterwarnings('ignore')
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from torch.utils.data import Dataset
from constants import STOP_WORDS
import numpy as np

np.bool = np.bool_

import warnings;

warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import gluonnlp as nlp
import torch

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
from fastapi import requests
import requests

import re
from transformers import BertTokenizer

from ai.bert_classifier import BERTClassifier
from ai.bert_dataset import BERTDataset


# Main Section
class KeywordService:
    def __init__(self):
        # Load the tokenizer once during initialization
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.stopwords = STOP_WORDS
        self.model_path = "/Users/rosie/PycharmProjects/ticats_ai_server/ai/KoBERT_D2_E11_A92.pt"

        # KoBERT용 토크나이저 정의
        self.bert_model, self.vocab = get_pytorch_kobert_model(cachedir=".cache")
        self.tok = nlp.data.BERTSPTokenizer(get_tokenizer(), self.vocab, lower=False)

        # 감정 분석 모델 로드
        self.model = BERTClassifier(self.bert_model, dr_rate=0.5)
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')), strict=False)

    def fetch_evaluations(self, url: str) -> str:
        """
        문화생활 기대평 & 관람평을 call하는 함수
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch evaluations")
        data = response.json().get("data", [])
        return " ".join(evaluation.get("content", "") for evaluation in data)

    def get_evaluations(self, goods_code: str) -> str:
        """
        문화생활 기대평 & 관람평을 추출하는 함수
        """
        base_url = "https://api-ticketfront.interpark.com/v1/boards"

        expect_evaluation_url = f"{base_url}?best=false&notice=false&page=1&pageSize=60&sort=DESC_WRITE_DATE&boardNo=62&goodsCode={goods_code}"
        review_evaluation_url = f"{base_url}?best=false&notice=false&page=1&pageSize=40&sort=DESC_WRITE_DATE&boardNo=10&goodsCode={goods_code}"

        expect_evaluation_text = self.fetch_evaluations(expect_evaluation_url)
        review_evaluation_text = self.fetch_evaluations(review_evaluation_url)

        combined_evaluation_text = expect_evaluation_text + review_evaluation_text

        return combined_evaluation_text

    def get_modeling_topics(self, target: str) -> str:
        try:
            # Vectorizer
            vect = TfidfVectorizer()  # vect = CountVectorizer()
            feat_vect = vect.fit_transform([target])

            # LDA Algorithm(토픽 모델)
            lda = LatentDirichletAllocation(n_components=5, learning_method="batch", max_iter=150)
            lda.fit_transform(feat_vect)

            # 토픽 모델링 결과 저장
            terms = vect.get_feature_names_out()
            topics = [','.join(t) for t in self.get_topics(lda.components_, terms)]

            # 중복 필터링
            return ','.join(sorted(set(','.join(topics).split(','))))

        except Exception as e:
            print(f'Exception: {e}')
            return ' '

    def united_Processor(self, target: str) -> (str, str):
        """
        토픽모델링 + 감성 분류
        """

        # 인풋 값 전처리
        target = ' '.join(self.text_tokenizer_morphs(target))

        # Device 정의
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        # topic 추출
        topics = self.get_modeling_topics(target=target)

        # 한글 외 문자 및 중복 제거
        input_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', ' ', topics)
        tokenized_sentence = self.text_tokenizer_morphs(input_sentence)
        filtered_sentence = ' '.join(set(tokenized_sentence))

        # 감정 분류 수행
        sentiments_lst = self.sentiment_prediction(filtered_sentence, self.tok, self.vocab, self.model, device)
        sentiments = ', '.join(sentiments_lst)

        return topics, sentiments

    def content_recommender(self, base_df, content_id_lst,
                            return_type='return_id'):  # 다중 인풋 처리용, id를 리스트 형태로 넣으면 됨(=content_id_lst).
        count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2), lowercase=False)  # 유사도 측정을 위한 피처 백터화
        genre_mat = count_vect.fit_transform(base_df['sentiment'])  # standard 인자 추가 가능

        genre_sim = cosine_similarity(genre_mat, genre_mat)  # 코사인 유사도 측정
        genre_sim_sorted_idx = genre_sim.argsort()[:, ::-1]  # 유사도가 높은 순으로 인덱스 나열(각 인덱스(작품)별로)

        sentiment_candidates = []
        for content_id in content_id_lst:
            content_idx = base_df[base_df['culturalEventId'] == content_id].index.values
            similar_indexes = genre_sim_sorted_idx[content_idx, :4]  # top3 만큼 가져옴(기준 인덱스 포함하여 4)
            similar_indexes = similar_indexes[similar_indexes != content_idx].reshape(-1)
            for idx in similar_indexes:
                sentiment_candidates.append(base_df.loc[idx, 'sentiment'])  # 감정 추출

        sentiment_candidates = ', '.join(sentiment_candidates).split(',')
        counter = Counter(sentiment_candidates)
        recommend_sentiment = ', '.join([item[0].strip() for item in counter.most_common(2)])  # 빈도 수 높은 감정 상위 2개 추출

        base_content = base_df[base_df['sentiment'] == recommend_sentiment].sample(
            n=1).index.values  # 같은 감정을 가진 작품 랜덤으로 선택
        similar_indexes = genre_sim_sorted_idx[base_content, :]  # base와 비슷한 작품 추천
        similar_indexes = similar_indexes[similar_indexes != content_idx].reshape(-1)

        if return_type == 'return_id':  # id
            idx_to_id_lst = []
            for idx in similar_indexes:
                idx_to_id_lst.append(base_df['culturalEventId'].iloc[idx])
            return idx_to_id_lst

        elif return_type == 'return_idx':  # index
            return similar_indexes

        else:
            print('return_type error')

    def sentiment_prediction(self, target_sentence, tok, vocab, model, device):
        start_time = time.time()  # 시작 시간 기록

        # 모델에 적합하게 input 전처리
        input_sentence = BERTDataset([[target_sentence, '0']], 0, 1, tok, vocab, 64, True, False)
        input_loader = torch.utils.data.DataLoader(input_sentence, batch_size=1, num_workers=0, pin_memory=True)

        model.eval()
        with torch.no_grad():
            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(input_loader):
                token_ids = token_ids.long().to(device)
                segment_ids = segment_ids.long().to(device)

                out = model(token_ids, valid_length, segment_ids)

                logits = out[0].detach().cpu().numpy()

        top_two_indices = logits.argsort()[-2:][::-1]  # 예측 결과에서 확률이 높은 상위 두개의 클래스 저장

        sentiment = []
        emotion_map = ["공포", "놀람", "분노", "슬픔", "중립", "행복", "혐오"]
        sentiment.extend(emotion_map[i] for i in top_two_indices)

        end_time = time.time()  # 끝 시간 기록
        total_time = end_time - start_time  # 총 실행 시간 계산

        print(f"Execution Time: {total_time} seconds")  # 실행 시간 출력
        return sentiment

    def text_tokenizer_morphs(self, text):
        # 텍스트 토큰화
        tokens_ko = self.tokenizer.tokenize(text)

        # 불용어 및 짧은 토큰 필터링
        result = [w for w in tokens_ko if w not in self.stopwords and len(w) > 1]

        return result

    def get_topics(self, components, feature_names, n=5):
        topics_lst = []
        for idx, topic in enumerate(components):
            topics_lst.append([(feature_names[i]) for i in topic.argsort()[:-n - 1:-1]])  # 토픽 모델링 결과에서 토픽만 추출하여 저장
        return topics_lst
