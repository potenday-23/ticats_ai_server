# Main Section
from fastapi import requests
import requests

import numpy as np

np.bool = np.bool_
import pandas as pd

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


# -----------------------------------------------------------------------------------------------------------------

def df_loader(path):  # 평가 단위로 데이터 로드
    content_info_df = pd.read_csv(path)
    content_info_df = content_info_df[['culturalEventId', 'culturalEventTitle', 'content']]

    content_info_df['content'] = content_info_df['content'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', regex=True)  # 한글 제외 문자 제거

    content_info_df = content_info_df.replace({' ': np.nan})  # 공백 문자 => nan
    content_info_df.dropna(how='any', inplace=True)  # nan값 제거
    content_info_df = content_info_df.reset_index(drop=True)  # index 재설정

    content_info_df['token'] = ''  # 컬럼 추가
    content_info_df['topic'] = ''
    content_info_df['sentiment'] = ''

    return content_info_df


# -----------------------------------------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------------------------------------


