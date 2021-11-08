import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

NYT_API_KEY = os.getenv("NYT_API_KEY")
most_popular_url = (
    f"https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={API_KEY}"
)


def get_most_popular():
    article_urls = []
    article_titles = []
    article_abstracts = []

    try:
        response = requests.get(most_popular_url)
        response_json = response.json()

        for i in range(10):
            article_urls.append(response_json["results"][i]["url"])
            article_titles.append(response_json["results"][i]["title"])
            article_abstracts.append(response_json["results"][i]["abstract"])

        print(response_json["num_results"])
        print(article_urls)
        print(article_titles)
        print(article_abstracts)
    except:
        return "error"


get_most_popular()
