# Main Section
from fastapi import requests
import pandas as pd
import requests

import re
import os
import statistics
import konlpy.tag
import numpy as np
np.bool = np.bool_
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter

import warnings; warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import gluonnlp as nlp
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model


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

#-----------------------------------------------------------------------------------------------------------------

def df_loader(path): #평가 단위로 데이터 로드
  content_info_df = pd.read_csv(path)
  content_info_df = content_info_df[['culturalEventId', 'culturalEventTitle', 'content']]

  content_info_df['content'] = content_info_df['content'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣]',' ',regex=True) # 한글 제외 문자 제거

  content_info_df = content_info_df.replace({' ': np.nan}) # 공백 문자 => nan
  content_info_df.dropna(how='any', inplace=True) # nan값 제거
  content_info_df = content_info_df.reset_index(drop=True) # index 재설정

  content_info_df['token'] = '' # 컬럼 추가
  content_info_df['topic'] = ''
  content_info_df['sentiment'] = ''

  return content_info_df

#-----------------------------------------------------------------------------------------------------------------

def text_tokenizer_morphs(text, stopword, stem_bool=False): # 토크나이저(형태소 단위)
    result = []
    module = konlpy.tag.Okt() # 토큰화 모듈 정의
    stop_words = set(stopword) # 불용어 사전 중복 제거
    tokens_ko = module.morphs(text, stem=stem_bool) # 토큰화
    for w in tokens_ko: #불용어 제거 및 너무 짧은 단어 제외
        if not w in stop_words and len(w) > 1:
            result.append(w)
    return result

#-----------------------------------------------------------------------------------------------------------------

def get_topics(components, feature_names, n=5):
    topics_lst = []
    for idx, topic in enumerate(components):
        topics_lst.append([(feature_names[i]) for i in topic.argsort()[:-n - 1:-1]]) # 토픽 모델링 결과에서 토픽만 추출하여 저장
    return topics_lst

#-----------------------------------------------------------------------------------------------------------------

class BERTDataset(Dataset): # KoBERT용 데이터 전처리
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len,vocab = vocab, pad = pad, pair = pair)
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))

#-----------------------------------------------------------------------------------------------------------------

class BERTClassifier(nn.Module): # KoBERT 모델 클래스 정의
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=7,
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

#-----------------------------------------------------------------------------------------------------------------

def sentiment_prediction(target_sentence, tok, vocab, model, device): # 감정 분류 수행
  input_sentence = BERTDataset([[target_sentence, '0']], 0, 1, tok, vocab, 64, True, False) # 모델에 적합하게 input 전처리
  input_loader = torch.utils.data.DataLoader(input_sentence, batch_size=64, num_workers=5)

  model.eval() # 예측 수행
  for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(input_loader):
      token_ids = token_ids.long().to(device)
      segment_ids = segment_ids.long().to(device)

      valid_length= valid_length
      label = label.long().to(device)

      out = model(token_ids, valid_length, segment_ids)

      sentiment=[]
      for i in out:
          logits=i
          logits = logits.detach().cpu().numpy()

  top_two_indices = logits.argsort()[-2:][::-1] # 예측 결과에서 확률이 높은 상위 두개의 클래스 저장

  sentiment = []
  for i in top_two_indices:
    if i == 0:
        sentiment.append("공포")
    elif i == 1:
        sentiment.append("놀람")
    elif i == 2:
        sentiment.append("분노")
    elif i == 3:
        sentiment.append("슬픔")
    elif i == 4:
        sentiment.append("중립")
    elif i == 5:
        sentiment.append("행복")
    elif i == 6:
        sentiment.append("혐오")

  return sentiment

#-----------------------------------------------------------------------------------------------------------------

def united_Processor(target, text_tokenizer, vectorizer, lda_lr_method, model_path): # 토픽모델링 + 감성 분류
# 파라미터 중 text_tokenizer, vectorizer, lda_lr_method은 각각 text_tokenizer_morphs, 'tfidf', 'batch'로 고정
# 파라미터 중 target과 Model_path는 input 및 감성 분류용 모델의 경로

# define Elements for processing ----------------------------------------------------------------------------------------
  stopword = ['보다는', '이지만', '보다', '치고', '자다', '이대로', '같다', '입니다', '에게', '텐데', '저런', '그렇다',
              '보기', '밖에', '같이', '이었다', '다소', '듣는', '가면', '되다', '되게', '하고', '너무', '라는', '하다',
              '해보다', '이라도', '그래도', '에요', '으로', '없이', '처럼', '였던가', '에서', '않아요', '들고', '예요', '했을지',
              '라니', '없다는', '에서도', '됩니다', '같은데', '왔다는', '않은', '보니', '합니다', '왔는데', '와서', '까지', '알았는데',
              '되었으면', '처럼', '있는', '마다', '함께', '보고', '보았어요', '에는', '까지', '그런데', '같네요', '보내고', '하면서',
              '우연히', '가게', '있기에', '한다', '가는', '하는지', '싶은', '있었어요', '같기도', '이다', '이긴', '이기는', '같아요',
              '싶었는데', '스럽게', '있어서', '않았다', '했네요', '했다', '부터', '그리고', '하여', '라고', '걸까', '싶다던','이었는데',
              '되네요', '스러운', '돼도', '들도', '해도', '였던', '갖고', '받습니다', '했습니다', '보는', '되진', '않네요', '되는', '봤었고',
              '으로만', '됐어요', '없었어요', '이에요','이었어요', '있으면', '스러워요', '있다는', '없어지고', '비해', '였습니다', '지만', '하시고',
              '이번', '하시는', '떠나지', '마치', '한편', '미리', '다시', '부분', '정도', '얼마나', '다른', '계속', '약간', '때문', '혹시', '통해',
              '지금', '등등', '건가', '해도', '여러분', '공연', '한번', '더라도', '그게', '뿐더러', '이고', '있는데', '이었지만', '보내는', '됐습니다',
              '라고는', '까요', '하던가', '하셨고', '봤네요', '무엇', '있을', '싶어요', '이었지만', '이렇게', '였는데', '했는데', '하다가', '인데',
              '가서', '있었다', '그렇지', '같은', '가장', '들수록', '해주세요', '있다니', '하는게', '이러면서', '이라니', '해서', '하며', '많이', '어떻게',
              '보러', '어떤', '조차', '하는', '덕분', '알았습니다','이었습니다', '전에', '내려가', '진짜', '그렇게', '언제', '같습니다', '있습니다', '모두',
              '있을까', '없을까', '될지', '왔습니다', '하던', '하셔서', '있고', '보려고', '본다고', '없으니', '였어요', '아닌', '갔는데', '않는데',
              '볼까', '보여주며', '들이', '볼수는', '보는데', '보면서', '같아용', '했었습니다', '가능한가요', '봤습니다', '그냥', '같다', '오다', '해주다', '라도'] # 불용어 리스트

  bertmodel, vocab = get_pytorch_kobert_model(cachedir=".cache") # KoBERT용 토크나이저 정의
  tok = nlp.data.BERTSPTokenizer(get_tokenizer(), vocab, lower=False)

  device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu') # device 정의(cpu or gpu)

  model = BERTClassifier(bertmodel,  dr_rate=0.5) # 모델 정의
  if device == 'cuda': # device 종류에 따른 모델 가중치 로드
    model.load_state_dict(torch.load(model_path))
    model = model.cuda()
  else:
    model.load_state_dict(torch.load(model_path,  map_location=torch.device('cpu')))

  if isinstance(target, pd.DataFrame): #input이 데이터프레임의 경우
    # topic modeling for df ----------------------------------------------------------------------------------------
    print('Start topic modeling for df')
    for idx in range(len(target)): # 각 행 단위로 수행
      target.loc[idx, 'token'] =  ' '.join(text_tokenizer_morphs(target.loc[idx, 'content'], stopword, False))
      try:
        if vectorizer == 'tfidf': # tfidf vetorizer로 벡터화 수행
          vect = TfidfVectorizer()
          feat_vect = vect.fit_transform([target.loc[idx, 'token']])
        else: #count vetorizer로 벡터화 수행(사용X, 추후 업뎃 대비한 옵션)
          vect = CountVectorizer()
          feat_vect = vect.fit_transform([target.loc[idx, 'token']])

        lda = LatentDirichletAllocation(n_components=3,learning_method=lda_lr_method, max_iter=150) # 토픽 모델(lda 알고리즘) 정의
        lda.fit_transform(feat_vect) # 토픽 모델링 수행

        terms = vect.get_feature_names_out() # 토픽 모델링 결과 저장
        topics = []
        for t in get_topics(lda.components_,terms):
            topics.append(','.join(t))
        topics = ','.join(list(set(topics))) # 1차 중복 필터링
        topics = ','.join(set(topics.split(','))) # 2차 중복 필터링
        target.loc[idx, 'topic'] = topics

      except:
        print(f'Exception in {idx}')

    topic_df = target[['culturalEventId', 'culturalEventTitle', 'topic', 'sentiment']] # Id, Title, Topic, Sentiment 컬럼만 남겨둠
    print('End topic modeling for df')
    # sentiment classification for df -----------------------------------------------------------------------------------------------------------------
    print('Start sentiment classification for df')
    table_per_content = topic_df.groupby('culturalEventId').agg({'culturalEventTitle': 'first', 'topic': ','.join, 'sentiment': ' '.join}).reset_index() # 작품 단위로 그룹화

    for topic in table_per_content['topic']: # 작품 단위로 감정 분류 수행
      input_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]',' ', topic) # 한글 이외 문자 제거
      sentence_sequneced = text_tokenizer_morphs(input_sentence, stopword, True) # 토큰화1(자체 불용어 제거를 통해 topic 필터링)
      sentence_sequneced = ' '.join(list(set(sentence_sequneced)))

      sentiments_lst = sentiment_prediction(sentence_sequneced, tok, vocab, model, device) # 감정 분류 수행

      sentiment = ', '.join(sentiments_lst)  # 분류 결과 저장
      table_per_content.loc[table_per_content['topic'] == topic, 'sentiment'] = sentiment

    setiment_df = table_per_content
    print('End sentiment classification for df')
    return setiment_df # 수행 종료(결과 리턴)

  else: #input이 문장일 경우
    # topic modeling for sentence -----------------------------------------------------------------------------------------------------------------
    print('Start topic modeling for sentence')
    target = ' '.join(text_tokenizer(target, stopword, False)) #input 전처리 (토큰화, 자체 불용어 제거)

    try:
      if vectorizer == 'tfidf': #tfidf vetorizer로 벡터화 수행
          vect = TfidfVectorizer()
          feat_vect = vect.fit_transform([target])
      else: #count vetorizer로 벡터화 수행(사용X, 추후 업뎃 대비한 옵션)
          vect = CountVectorizer()
          feat_vect = vect.fit_transform([target])

      lda = LatentDirichletAllocation(n_components=5,learning_method=lda_lr_method, max_iter=150) # 토픽 모델(lda알고리즘) 정의
      lda.fit_transform(feat_vect) #토픽 모델링 수행

      terms = vect.get_feature_names_out() # 토픽 모델링 결과 저장
      topics = []
      for t in get_topics(lda.components_,terms):
          topics.append(','.join(t))
      topics = ','.join(list(set(topics))) # 1차 중복 필터링
      topics = ','.join(set(topics.split(','))) # 2차 중복 필터링

    except:
      print('Exception') # 예외 발생시 빈값으로 처리
      topics = ' '
    print('End topic modeling for sentence')

    # sentiment classification for sentence -----------------------------------------------------------------------------------------------------------------
    print('Start sentiment classification for sentence')
    input_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]',' ', topics) # 한글 이외 문자 제거
    sentence_sequneced = text_tokenizer_morphs(input_sentence, stopword, True) # 토큰화1(자체 불용어 제거를 통해 topic 필터링)
    sentence_sequneced = ' '.join(list(set(sentence_sequneced)))

    sentiments_lst = sentiment_prediction(sentence_sequneced, tok, vocab, model, device) # 감정 분류 수행

    sentiment = ', '.join(sentiments_lst)
    print('End sentiment classification for sentence')
    return topics, sentiment # 수행 종료(결과 리턴, str타입)
  
#-----------------------------------------------------------------------------------------------------------------

def content_recommender(base_df, content_id_lst, return_type='return_id'): #다중 인풋 처리용, id를 리스트 형태로 넣으면 됨(=content_id_lst).
  count_vect = CountVectorizer(min_df = 0, ngram_range=(1, 2), lowercase=False) # 유사도 측정을 위한 피처 백터화
  genre_mat = count_vect.fit_transform(base_df['sentiment']) #standard 인자 추가 가능

  genre_sim = cosine_similarity(genre_mat, genre_mat) # 코사인 유사도 측정
  genre_sim_sorted_idx = genre_sim.argsort()[:, ::-1] # 유사도가 높은 순으로 인덱스 나열(각 인덱스(작품)별로)

  sentiment_candidates=[]
  for content_id in content_id_lst:
    content_idx = base_df[base_df['culturalEventId'] == content_id].index.values
    similar_indexes = genre_sim_sorted_idx[content_idx, :4] #top3 만큼 가져옴(기준 인덱스 포함하여 4)
    similar_indexes = similar_indexes[similar_indexes != content_idx].reshape(-1)
    for idx in similar_indexes:
      sentiment_candidates.append(base_df.loc[idx, 'sentiment']) #감정 추출

  sentiment_candidates = ', '.join(sentiment_candidates).split(',') 
  counter = Counter(sentiment_candidates)
  recommend_sentiment = ', '.join([item[0].strip() for item in counter.most_common(2)]) #빈도 수 높은 감정 상위 2개 추출

  base_content = base_df[base_df['sentiment'] == recommend_sentiment].sample(n=1).index.values #같은 감정을 가진 작품 랜덤으로 선택
  similar_indexes = genre_sim_sorted_idx[base_content, :] #base와 비슷한 작품 추천
  similar_indexes = similar_indexes[similar_indexes != content_idx].reshape(-1)

  if return_type == 'return_id': #id
    idx_to_id_lst = []
    for idx in similar_indexes:
      idx_to_id_lst.append(base_df['culturalEventId'].iloc[idx])
    return idx_to_id_lst

  elif return_type == 'return_idx': #index
    return similar_indexes

  else:
    print('return_type error')