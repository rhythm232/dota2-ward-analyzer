import time
import requests
import sys
from .config import POLITE_SLEEP

def get_json(url, params=None, sleep=POLITE_SLEEP):
    """
    Fetches JSON data from a URL with a polite sleep interval.
    """
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()  # Raise an exception for bad status codes
        time.sleep(sleep)
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        return None
