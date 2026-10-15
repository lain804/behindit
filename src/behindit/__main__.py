from curl_cffi import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from behindit import instagram
from behindit import tiktok
import re
from urllib.parse import urlsplit

URL_HANDLERS = {
    r"(?:www\.)?instagram\.com": instagram.process_url,
    r"(?:(?:www|m|vm|vt)\.)?tiktok\.com": tiktok.process_url,
}

def process_url(url: str):
    url = url.strip()

    if not url.startswith("https://"):
        url = "https://" + url

    parsed_url = urlsplit(url)

    hostname = parsed_url.hostname
    if hostname is None:
        raise RuntimeError("Failed to parse url hostname")

    url_handler = None

    for pattern, handler in URL_HANDLERS.items():
        if re.fullmatch(pattern, hostname, re.IGNORECASE):
            url_handler = handler
            break

    if url_handler is None:
        raise RuntimeError("Failed to find handler for url")
    else:
        handler(url)

def main():
    parser = ArgumentParser()

    parser.add_argument("url")

    args = parser.parse_args()

    process_url(args.url)

if __name__ == "__main__":
    main()