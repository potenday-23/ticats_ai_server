# Modules
from fastapi import HTTPException
import numpy as np
np.bool = np.bool_

import warnings;
warnings.filterwarnings('ignore')
from fastapi import requests
import requests

# Main Section
class KeywordService:
    def __init__(self):
        # 미사용
        self.model_s3_url = "https://tickets2323.s3.ap-northeast-2.amazonaws.com/Ai/Kobert_ver1.pt"

    def download_model_from_s3(self, s3_url, local_path):
        response = requests.get(s3_url)
        with open(local_path, 'wb') as f:
            f.write(response.content)

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

    def get_model():
      genai.configure(api_key='AIzaSyCZ55ym49UmyUnM7_5x83I2zq8RmIOfbHA')
      generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
      }
      model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
      return model

    def topic_extraction1(ocr_result, model):
        '''
        토픽 추출1: 평가 단위 추출
        '''
        prompt1 = "위의 내용들은 공연에 대한 평가입니다."
        prompt2 = "이 평가들을 키워드 형태로 요약하세요"
        prompt3 = "요구한 내용 외에 다른 말은 하지 말고, 리스트 형태로 반환하세요"
        response = model.generate_content(f"{prompt1}\n{ocr_result}\n{prompt2}\n{prompt3}")

        try:
            topic = response.text.replace("-", "").replace("\n", ", ")
        except:
            topic = ''

        return topic

    def topic_extraction2(ocr_result, model):
        '''
        토픽 추출2: 콘텐츠 단위 추출
        '''
        prompt1 = "위의 키워드들은 공연에 대한 평가를 요약한 키워드입니다."
        prompt2 = "이 중 핵심 키워드를 선택해주세요"
        prompt3 = "요구한 내용 외에 다른 말은 하지 말고, 리스트 형태로 반환하세요"
        response = model.generate_content(f"{prompt1}\n{ocr_result}\n{prompt2}\n{prompt3}")

        try:
            topic = response.text.replace("-", "").replace("\n", ", ")
        except:
            topic = ''

        topic = topic.str.replace(r'[^\w,]', '', regex=True).str.replace(r',', ' ', regex=True)
        return topic