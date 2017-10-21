
import requests


def fetch_url_content(url: str) -> str:
    return requests.get(url).content
