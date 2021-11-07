import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv("API_KEY")
most_popular_url = (
    f"https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={API_KEY}"
)


def get_most_popular():
    article_urls = []
    article_titles = []
    article_abstracts = []
    article_images = []

    try:
        response = requests.get(most_popular_url)
        response_json = response.json()

        article_urls.append(response_json["results"][0]["url"])
        article_titles.append(response_json["results"][0]["title"])
        article_abstracts.append(response_json["results"][0]["abstract"])
        article_images.append(
            response_json["results"][0]["media"][0]["media-metadata"][0]["url"]
        )

        print(response_json["num_results"])
        print(article_urls)
        print(article_titles)
        print(article_abstracts)
        print(article_images)
    except:
        return "error"


get_most_popular()
