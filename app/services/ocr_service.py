# Python
import os
import re
import ast
import json
import time
import uuid
from io import BytesIO

import requests
from collections import OrderedDict

# Third Party
import google.generativeai as genai

NAVER_SECRET_KEY = os.getenv("NAVER_SECRET_KEY", None)
GEMINAI_SECRET_KEY = os.getenv("GEMINAI_SECRET_KEY", None)


# Main Section
class OcrService:
    """
    티켓 이미지로부터 정보 추출
    input_img: 입력 이미지
    model: 정보 추출에 사용될 모델(Gemini)
    """

    def __init__(self):
        self.model = self.get_model()

    def info_extractor(self, image):
        """
        char_recognizer: OCR
        ocr_result_processor: OCR 결과 처리
        info_extraction: 정보 추출
        correct_seat_info: 좌석정보 정제
        """
        ticket_words = self.char_recognizer(image)
        ticket_info_processed = self.ocr_result_processor(ticket_words)
        infos = self.info_extraction(ticket_info_processed)
        try:
            infos['좌석정보'] = self.correct_seat_info(infos)
        except:
            # Exception1: 부적합한 결과가 드물게 발생 => 다시 수행
            infos = self.info_extraction(ticket_info_processed)
            try:
                infos['좌석정보'] = self.correct_seat_info(infos)
            except:
                # Exception2: 정보없음으로 처리
                pass
        return infos

    def char_recognizer(self, image_content):
        """
        OCR 수행
        """
        api_url = 'https://yhnf1pbln5.apigw.ntruss.com/custom/v1/29894/d66583da242cd4fcddc7c2c8b2e3a6a65692b0d9df8eb03bfea832e0a4d8f713/general'
        secret_key = NAVER_SECRET_KEY

        input_format = image_content.split('.')[-1].lower()
        if input_format not in ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'pdf']:
            raise ValueError(f"Unsupported file format: {input_format}, Supported formats are 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'pdf'.")
        request_json = {
            'images': [{'format': input_format, 'name': 'demo'}],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = {'file': ('image.jpg', BytesIO(image_content), 'application/octet-stream')}
        headers = {'X-OCR-SECRET': secret_key}
        response = requests.post(api_url, headers=headers, data=payload, files=files)
        result_json = response.json()

        return result_json

    def ocr_result_processor(self, ocr_result):
        '''
        OCR결과에서 필요한 요소만을 남겨둠
        '''
        ticket_words = {}
        for image in ocr_result['images']:
            for field in image['fields']:
                infertext = field['inferText']
                vertices = field['boundingPoly']['vertices']
                y_coords = [point['y'] for point in vertices]
                center_y = sum(y_coords) / len(y_coords)
                # 중복된 경우 이름을 수정하여 새로운 키 생성
                if infertext in ticket_words:
                    new_key = infertext + '_duplicatied'
                    ticket_words[new_key] = [center_y]
                else:
                    ticket_words[infertext] = [center_y]

        # 예매시간에 해당하는 정보는 제외
        target = None
        for key, value in ticket_words.items():
            if '예매' in key or '예약' in key or '판매' in key:
                if '일시' in key or '일자' in key or '시각' in key or '시간' in key:
                    target = value[0]
        if target:
            L = target + 20
            U = target - 20
            del_lst = []
            for key, value in ticket_words.items():
                if U <= value[0] <= L:
                    del_lst.append(key)
            for key in del_lst:
                del ticket_words[key]

        return ticket_words

    def get_model(self):
        '''
        제미나이 모델 정의
        '''
        genai.configure(api_key=GEMINAI_SECRET_KEY)
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
        return model

    def info_extraction(self, ocr_result):
        '''
        정보 추출
        '''
        # 프롬프트 양식
        prompt1 = "다음은 공연티켓에 OCR을 수행한 결과입니다. 이 정보는 단어와 y좌표로 구성되어 있습니다."
        prompt2 = "여기에서 공연제목, 공연장소(건물이름), 공연날짜, 좌석정보에 해당하는 정보를 찾아주세요. 그리고 딕셔너리 형태로 알려주세요."
        prompt3 = "그리고 공연정보 딕셔너리 외에는 어떠한 문장도 답변에 포함하지 마세요"
        prompt4 = "공연날짜의 양식은 'year-month-date' 입니다."
        prompt5 = "좌석정보는 '층, 블럭, 관, 구역, 열, 번, 스탠딩, 자유석, 비지정석' 중 일부가 포함된 요소만 해당합니다"
        prompt6 = "좌석정보 내 단어들의 순서는 '층, 관, 블럭, 구역, 열, 번' 입니다."
        prompt7 = "만약 좌석정보에서 '스탠딩'과 '스탠딩석' 이 포함된 단어가 모두 존재한다면, '스탠딩'이 포함된 단어만 남겨놓습니다."
        prompt8 = "좌석정보는 여러 개의 좌석을 포함 가능합니다."

        # 정보 추출
        response = self.model.generate_content(f"{prompt1}\n{ocr_result}\n{prompt2}\n{prompt4}\n{prompt3}\n{prompt4}\n{prompt5}\n{prompt6}\n{prompt7}\n{prompt8}")

        # 추출결과를 딕셔너리로 재구성
        infos = re.search(r'\{(.*?)\}', response.text)
        if infos:
            result = ast.literal_eval("{" + infos.group(1) + "}")
        else:
            result = {'info' : 'None'}

        return result

    def correct_seat_info(self, ticket_words):
        '''
        좌석정보가 비어있는 경우에 대응
        '''
        seat_info_refined = '정보없음'

        if ticket_words['좌석정보'] != None:
            if isinstance(ticket_words['좌석정보'], list):
                seat_info_refined = ' '.join(ticket_words['좌석정보'])
                if seat_info_refined == '':
                    seat_info_refined = '정보없음'

        return seat_info_refined
