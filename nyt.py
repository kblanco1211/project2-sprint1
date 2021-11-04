import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv("API_KEY")
response = requests.get(
    f"https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={API_KEY}"
)

print(response.json())
