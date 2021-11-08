import os
from dotenv import find_dotenv, load_dotenv
from googleapiclient import discovery

load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
resource = discovery.build("customsearch", "v1", developerKey=GOOGLE_API_KEY).cse()
results = resource.list(q="news", cx="238bdc64abf04114c").execute()
print(results)
