import requests
from urllib.parse import urlparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()

COMMON_PARAMS = [
    "id",
    "page",
    "file",
    "path",
    "search",
    "query",
    "cat",
    "item",
    "view"
]


def check_parameter(task):

    url, param = task

    url1 = f"{url}?{param}=1"
    url2 = f"{url}?{param}=2"

    try:

        r1 = session.get(url1, timeout=2)
        r2 = session.get(url2, timeout=2)

        len1 = len(r1.text)
        len2 = len(r2.text)

        if abs(len1 - len2) > 20:
            return (url, param)

    except:
        pass

    return None


def discover_parameters(urls, threads=20):

    print("\n[+] Performing Parameter Discovery\n")

    param_urls = set()
    tasks = []

    for url in urls:

        parsed = urlparse(url)

        # If URL already has parameters
        if parsed.query:
            param_urls.add(url)
            continue

        # Only test dynamic pages
        if not parsed.path.endswith((".php", ".asp", ".jsp")):
            continue

        for param in COMMON_PARAMS:
            tasks.append((url, param))

    with ThreadPoolExecutor(max_workers=threads) as executor:

        results = list(
            tqdm(
                executor.map(check_parameter, tasks),
                total=len(tasks),
                desc="Param Discovery",
                ascii="-#",
                ncols=70
            )
        )

    for r in results:

        if r:
            url, param = r
            print(f"[+] Parameter discovered → {param} on {url}")
            param_urls.add(f"{url}?{param}=1")

    return param_urls