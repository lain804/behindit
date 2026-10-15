from bs4 import BeautifulSoup
from curl_cffi import requests
from .constants import MOBILE_USER_AGENT
import json
import jmespath

def process_url(url):
    headers = {
        "User-Agent": MOBILE_USER_AGENT
    }

    response = requests.get(
        url=url,
        headers=headers,
        impersonate="chrome"
    )
    response.raise_for_status()

    soup = BeautifulSoup(
        markup=response.text,
        features="lxml"
    )
    
    script_tags = soup.find_all(
        "script",
        {
            "type": "application/json"
        }
    )

    sharer_info_json = None

    for tag in script_tags:
        if '"full_name"' in tag.text:
            sharer_info_json = tag.text
            break

    if sharer_info_json is None:
        raise RuntimeError("Failed to find sharer_info_json")
    
    sharer_info_deserialized = json.loads(sharer_info_json)

    sender_info_expression = "require[0][3][0].__bbox.require[0][3][1].__bbox.result.data.xig_polaris_media.user_for_shid_logged_out"
    
    sender_info = jmespath.search(sender_info_expression,sharer_info_deserialized)
    
    if not sender_info:
        raise RuntimeError("Failed to find sender_info using jmespath search expression")

    # trick to put profile link at the top
    sender_info = {
        "profile_link": f"https://www.instagram.com/{sender_info["username"]}",
        **sender_info
    }
    
    print(
        json.dumps(
            sender_info,
            indent=4
        )
    )