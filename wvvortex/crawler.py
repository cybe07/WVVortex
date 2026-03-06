import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl(target_url):

    print(f"[+] Crawling {target_url}")

    discovered_urls = set()
    domain = urlparse(target_url).netloc

    try:
        response = requests.get(target_url, timeout=5)

    except:
        print("[-] Could not connect to target")
        return discovered_urls

    soup = BeautifulSoup(response.text, "html.parser")

    # extract links from multiple tags
    tags = [
        ("a", "href"),
        ("form", "action"),
        ("script", "src"),
        ("iframe", "src")
    ]

    for tag, attr in tags:

        for element in soup.find_all(tag):

            link = element.get(attr)

            if not link:
                continue

            full_url = urljoin(target_url, link)

            parsed = urlparse(full_url)

            # remove fragments (#something)
            clean_url = parsed._replace(fragment="").geturl()

            if parsed.netloc == domain:
                discovered_urls.add(clean_url)

    return discovered_urls