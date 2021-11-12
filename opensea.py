import requests


def get_assets():
    image_urls = []
    names = []
    creators = []
    contract_addresses = []
    token_ids = []

    url = "https://api.opensea.io/api/v1/assets"
    params = {"limit": 10}

    response = requests.get(url, params=params)
    response_json = response.json()

    for i in range(10):
        image_urls.append(response_json["assets"][i]["image_url"])
        names.append(response_json["assets"][i]["name"])
        try:
            creators.append(response_json["assets"][i]["creator"]["user"]["username"])
        except:
            creators.append(None)
        contract_addresses.append(
            response_json["assets"][i]["asset_contract"]["address"]
        )
        token_ids.append(response_json["assets"][i]["token_id"])

    return {
        "image_urls": image_urls,
        "names": names,
        "creators": creators,
        "contract_addresses": contract_addresses,
        "token_ids": token_ids,
    }


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
