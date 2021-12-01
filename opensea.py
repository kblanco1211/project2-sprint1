"""Contains all opensea api logic"""

import requests
from requests.models import Response
import json


def get_assets():
    """Information for several NFTs are returned by this function, and it is used to display information on the explore NFTs page"""

    # lists that will be returned that store information obtained from the api call
    image_urls = []
    names = []
    collections = []
    contract_addresses = []
    token_ids = []

    # url link and parameters used to make an opensea retrieve assets api call
    # the api call returns information for individual NFTs or assets the amount of assets returned is given by the parameters
    url = "https://api.opensea.io/api/v1/assets?order_by=sale_date&order_direction=desc&offset=0&limit=20"

    # try except is to account for if there is an error when making the api call
    try:
        # a request is used to make the api call and the information returned is stored in a json
        response = requests.get(url)
        response_json = response.json()

        # this loop parses the response json and stores the correct information for each NFT in the correct lists
        for i in range(20):
            image_urls.append(response_json["assets"][i]["image_url"])
            names.append(response_json["assets"][i]["name"])
            try:
                collections.append(response_json["assets"][i]["collection"]["name"])
            except Exception:
                collections.append(None)
            contract_addresses.append(
                response_json["assets"][i]["asset_contract"]["address"]
            )
            token_ids.append(response_json["assets"][i]["token_id"])
    except Exception:
        return "error"

    return {
        "image_urls": image_urls,
        "names": names,
        "collections": collections,
        "contract_addresses": contract_addresses,
        "token_ids": token_ids,
    }


def get_single_asset(contract_address, token_id):
    """
    function takes in an NFT's contract address and token id and uses them to make an opensea api call that returns information for that NFT
    the information returned from this function is used to display on the details page
    """

    # url link used to make the opensea retrieve single asset api call
    url = f"https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}/"
    # try except is to account for if there is an error when making the api call
    try:
        response = requests.get(url)
        response_json = response.json()

        image_url = response_json["image_url"]
        name = response_json["name"]
        collection = response_json["collection"]["name"]
        collection_description = response_json["collection"]["description"]
        description = response_json["description"]
        try:
            creator = response_json["creator"]["user"]["username"]
        except Exception:
            creator = None
        try:
            price = float("0." + str(response_json["last_sale"]["total_price"][:4]))
            usd_price = response_json["collection"]["payment_tokens"][0]["usd_price"]
            usd_price = round(usd_price * price, 2)

        except Exception:
            price = None
            usd_price = None
        try:
            crypto = response_json["orders"][0]["payment_token_contract"]["symbol"]
        except Exception:
            crypto = None
        trait_types = []
        traits = []
        for i in range(len(response_json["traits"])):
            trait_types.append(response_json["traits"][i]["trait_type"])
            traits.append(response_json["traits"][i]["value"])
    except Exception:
        return "error"

    # information on the given NFT is returned
    return {
        "image_url": image_url,
        "name": name,
        "collection": collection,
        "collection_description": collection_description,
        "description": description,
        "creator": creator,
        "price": price,
        "usd_price": usd_price,
        "crypto": crypto,
        "trait_types": trait_types,
        "traits": traits,
        "contract_address": contract_address,
        "token_id": token_id,
    }
