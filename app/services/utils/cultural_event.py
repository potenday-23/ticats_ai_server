# Fast API
from fastapi import requests

# Third Party
import pandas as pd
import requests


# Main section
def get_cultural_event_list():
    """
    문화생활 목록을 가져와 DataFrame으로 반환하는 함수
    """
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
