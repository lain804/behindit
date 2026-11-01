from urllib import parse

from curl_cffi import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from behindit import instagram
from behindit import tiktok
import re
from urllib.parse import urlsplit
import logging
from behindit.constants import EXIT_FAILURE

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
        logging.error("Failed to parse url hostname")
        exit(EXIT_FAILURE)

    url_handler = None

    for pattern, handler in URL_HANDLERS.items():
        if re.fullmatch(
            pattern, 
            hostname, 
            re.IGNORECASE
        ):
            url_handler = handler
            break

    if url_handler is None:
        logging.error("Failed to find handler for url")
        exit(EXIT_FAILURE)
    else:
        handler(url)

def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-v","--verbose", 
        dest="verbose", 
        action="store_true"
    )

    parser.add_argument("url")

    args = parser.parse_args()

    logging_level = logging.WARNING
    if args.verbose:
        logging_level = logging.DEBUG

    logging.basicConfig(
        level=logging_level,
        format="[%(asctime)s] [%(levelname)-8s] %(message)s",
    )

    process_url(args.url)

if __name__ == "__main__":
    main()
