from bs4 import BeautifulSoup
from curl_cffi import requests
from .constants import MOBILE_USER_AGENT, TIKTOK_SHARE_INFO_SETTING_OFF_CODE
import json

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

    rehydration_data_tag = soup.find("script",id="__UNIVERSAL_DATA_FOR_REHYDRATION__")

    if not rehydration_data_tag:
        raise RuntimeError("Failed to find Tiktok rehydration data tag")

    rehydration_data = rehydration_data_tag.text

    info_json = json.loads(rehydration_data)

    user_data = info_json["__DEFAULT_SCOPE__"]["webapp.reflow.global.shareUser"]

    if user_data.get("statusCode") == TIKTOK_SHARE_INFO_SETTING_OFF_CODE:
        raise RuntimeError("Tiktok User explicitly disabled sharing their user via links")

    share_user = user_data.get("shareUser")
    if share_user is None:
        raise RuntimeError("Failed to get shareUser")

    # 2 smaller sizes redundant if we have biggest size and highest quality under avatarLarger
    # + they take up a lot of space due to the urls being signed
    del share_user["avatarMedium"]
    del share_user["avatarThumb"]

    # trick to put the profile link at the top of the returned dictionary (python dictionaries are ordered)
    user_data["shareUser"] = {
        "profile_link": f"https://tiktok.com/@{share_user["uniqueId"]}",
        **share_user
    }

    print(
        json.dumps(
            user_data,
            indent=4
        )
    )