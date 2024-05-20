# Fast API
from fastapi import requests

# Third Party
import pandas as pd
import requests


# Main section
def get_cultural_event_evaluation_list():
    """
    문화생활 평가 목록을 가져와 DataFrame으로 반환하는 함수
    type : EXPECT(기대평), REVIEW(관람평)
    """
    base_url = "https://ticats.site/api/cultural-event-evaluations"
    try:
        response = requests.get(base_url + "?page=1&size=100")
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
