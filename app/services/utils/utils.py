import re
import ast
import json
import time
import uuid
import requests
from collections import OrderedDict
import google.generativeai as genai


def char_recognizer(input_img):
  '''
  OCR 수행
  '''
  api_url = 'https://yhnf1pbln5.apigw.ntruss.com/custom/v1/29894/d66583da242cd4fcddc7c2c8b2e3a6a65692b0d9df8eb03bfea832e0a4d8f713/general'
  secret_key = 'WEtmdkt4VUhTVGd0cUVzRHFhdEp0Zk5rd1BDRllGc1Q='
  request_json = {
                  'images': [{'format': 'jpg', 'name': 'demo'}],
                  'requestId': str(uuid.uuid4()),
                  'version': 'V2',
                  'timestamp': int(round(time.time() * 1000))
                  }
  payload = {
            'message': json.dumps(request_json).encode('UTF-8')
            }
  files = [('file', open(input_img,'rb'))]
  headers = {
            'X-OCR-SECRET': secret_key
            }
  response = requests.request("POST", api_url, headers=headers, data = payload, files = files)
  result_json = json.loads(response.text.encode('utf8'))

  return result_json


def ocr_result_processor(ocr_result):
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

    #예매시간에 해당하는 정보는 제외
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


def get_model():
    '''
    제미나이 모델 정의
    '''
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


def info_extraction(ocr_result, model):
    '''
    정보 추출
    '''
    #프롬프트 양식
    prompt1 = "다음은 공연티켓에 OCR을 수행한 결과입니다. 이 정보는 단어와 y좌표로 구성되어 있습니다."
    prompt2 = "여기에서 공연제목, 공연장소(건물이름), 공연날짜, 좌석정보에 해당하는 정보를 찾아주세요. 그리고 딕셔너리 형태로 알려주세요."
    prompt3 = "그리고 공연정보 딕셔너리 외에는 어떠한 문장도 답변에 포함하지 마세요"

    #정보 추출
    response = model.generate_content(f"{prompt1}\n{ocr_result}\n{prompt2}{prompt3}")

    #추출결과를 딕셔너리로 재구성
    infos = re.search(r'\{(.*?)\}', response.text)
    if infos:
        result = ast.literal_eval("{" + infos.group(1) + "}")
    else:
        result = {'info' : 'None'}

    return result


def correct_seat_info(ticket_words):
    '''
    좌석정보와 관련있는 키워드를 제외하고는 모두 제거
    '''
    if ticket_words['좌석정보'] != None:
        seat_info = ticket_words['좌석정보']
        patterns = [r"\d{1,2}\s?층",
                    r"\w{1,3}블럭",
                    r"스탠딩",
                    r"\d{1,2}관",
                    r"(?!딩)(?!층)\w{1,2}구역",
                    r"(?!역)(?!구역)\w{1,3}열",
                    r"자유석+$",
                    r"\d{1,4}번",
                    r"자유석",
                    r"비지정석"]
        matches = []
        for pattern in patterns:
            matches.extend(re.findall(pattern, seat_info))
        mathces_unique = list(OrderedDict.fromkeys(matches))
        seat_info_refined = ' '.join(mathces_unique)
        if seat_info_refined == '':
          seat_info_refined = '정보없음'

    else:
        seat_info_refined = '정보없음'

    return seat_info_refined
