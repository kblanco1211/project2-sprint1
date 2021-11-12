import requests


def get_assets():
    url = "https://api.opensea.io/api/v1/assets"
    params = {"limit": 1}

    response = requests.get(url, params=params)
    response_json = response.json()

    permalink = response_json["assets"][0]["permalink"]
    image_url = response_json["assets"][0]["image_url"]
    name = response_json["assets"][0]["name"]
    try:
        creator = response_json["assets"][0]["creator"]["user"]["username"]
    except:
        creator = None
    contract_address = response_json["assets"][0]["asset_contract"]["address"]
    token_id = response_json["assets"][0]["token_id"]
    print(permalink)
    print(image_url)
    print(name)
    print(creator)
    print(contract_address)
    print(token_id)


def get_single_asset(contract_address, token_id):
    url = f"https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}/"

    response = requests.get(url)
    response_json = response.json()

    image_url = response_json["image_url"]
    name = response_json["name"]
    collection_name = response_json["collection"]["name"]
    description = response_json["description"]
    creator = response_json["creator"]["user"]["username"]
    try:
        price = response_json["orders"][0]["current_price"]
    except:
        price = None
    crypto = response_json["orders"][0]["payment_token_contract"]["symbol"]
    traits = response_json["traits"]
    contract_address = response_json["asset_contract"]["address"]
    token_id = response_json["token_id"]
    print(image_url)
    print(name)
    print(collection_name)
    print(description)
    print(creator)
    print(price)
    print(crypto)
    print(traits)
    print(contract_address)
    print(token_id)


get_assets()
get_single_asset(
    "0xf43aaa80a8f9de69bc71aea989afceb8db7b690f",
    "2090",
)
