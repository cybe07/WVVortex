import requests
from tqdm import tqdm
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()

PARAM_WORDLIST = [
    "id",
    "page",
    "file",
    "path",
    "include",
    "template",
    "redirect",
    "url",
    "next",
    "view"
]


def check_fuzz(task):

    url, param, base_len = task

    test_url = f"{url}?{param}=1"

    try:

        r = session.get(test_url, timeout=2)

        if abs(len(r.text) - base_len) > 30:
            return test_url

    except:
        pass

    return None


def fuzz_parameters(urls, threads=20):

    print("\n[+] Starting Parameter Fuzzing\n")

    discovered = set()
    tasks = []

    for url in urls:

        parsed = urlparse(url)

        if "=" in url:
            continue

        if parsed.path.endswith(".php") or parsed.path == "" or parsed.path == "/":

            try:
                baseline = session.get(url, timeout=2)
                base_len = len(baseline.text)
            except:
                continue

            for param in PARAM_WORDLIST:
                tasks.append((url, param, base_len))

    with ThreadPoolExecutor(max_workers=threads) as executor:

        results = list(
            tqdm(
                executor.map(check_fuzz, tasks),
                total=len(tasks),
                desc="Param Fuzzing",
                ascii="-#",
                ncols=70
            )
        )

    for r in results:

        if r:
            print(f"[+] Hidden parameter discovered -> {r}")
            discovered.add(r)

    return discovered