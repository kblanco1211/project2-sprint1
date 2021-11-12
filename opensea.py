import requests


def get_assets():
    image_urls = []
    names = []
    collections = []
    contract_addresses = []
    token_ids = []

    url = "https://api.opensea.io/api/v1/assets"
    params = {"limit": 16}

    response = requests.get(url, params=params)
    response_json = response.json()

    for i in range(16):
        image_urls.append(response_json["assets"][i]["image_url"])
        names.append(response_json["assets"][i]["name"])
        try:
            collections.append(response_json["assets"][i]["collection"]["name"])
        except:
            collections.append(None)
        contract_addresses.append(
            response_json["assets"][i]["asset_contract"]["address"]
        )
        token_ids.append(response_json["assets"][i]["token_id"])

    return {
        "image_urls": image_urls,
        "names": names,
        "collections": collections,
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
        string_price = response_json["orders"][0]["current_price"]
        price = round(int(string_price) * 0.000000000000000001, 3)
    except:
        price = None
    crypto = response_json["orders"][0]["payment_token_contract"]["symbol"]
    traits = response_json["traits"]

    return {
        "image_url": image_url,
        "name": name,
        "collection_name": collection_name,
        "description": description,
        "creator": creator,
        "price": price,
        "crypto": crypto,
        "traits": traits,
        "contract_address": contract_address,
        "token_id": token_id,
    }
