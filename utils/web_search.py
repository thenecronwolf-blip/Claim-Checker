# utils/web_search.py
import requests
import os

def bing_search(query):
    return requests.get(
        "https://api.bing.microsoft.com/v7.0/search",
        headers={"Ocp-Apim-Subscription-Key": os.environ["BING_API_KEY"]},
        params={"q": query, "count": 5}
    ).json()
