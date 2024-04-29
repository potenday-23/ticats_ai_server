# Main Section
from fastapi import requests
import pandas as pd
import requests


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
