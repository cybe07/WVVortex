import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import random
import string

session = requests.Session()
session.headers.update({
    "User-Agent": "SmartVulnScan/1.0"
})


# -----------------------------
# Load wordlist
# -----------------------------
def load_wordlist(path):

    words = []

    with open(path, "r") as f:
        for line in f:
            word = line.strip()

            if word:
                words.append(word)

    return words


# -----------------------------
# Wildcard detection
# -----------------------------
def detect_wildcard(url):

    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    test_url = f"{url.rstrip('/')}/{rand}"

    try:
        r = session.get(test_url, timeout=5)
        return (r.status_code, len(r.text))

    except:
        return (None, None)


# -----------------------------
# Check directory
# -----------------------------
def check_directory(args):

    base_url, word, wildcard = args

    url = f"{base_url.rstrip('/')}/{word}"

    try:

        r = session.get(url, timeout=5)

        status = r.status_code
        length = len(r.text)

        if status == wildcard[0] and abs(length - wildcard[1]) < 10:
            return None

        if status in [200, 301, 302, 403]:
            return (url, status)

    except:
        pass

    return None


# -----------------------------
# Recursive scanning
# -----------------------------
def brute_force_dirs(base_url, wordlist, depth=2, threads=20):

    words = load_wordlist(wordlist)

    discovered = set()

    print("\n[+] Starting Directory Brute Force (Depth 1)\n")

    wildcard = detect_wildcard(base_url)

    tasks = [(base_url, word, wildcard) for word in words]

    with ThreadPoolExecutor(max_workers=threads) as executor:

        for r in tqdm(
            executor.map(check_directory, tasks),
            total=len(tasks),
            desc="Dir Bruteforce",
            ascii="-#",
            ncols=70
        ):

            if r:
                url, status = r
                print(f"[+] Found -> {url} ({status})")
                discovered.add(url)

    # -----------------------------
    # Depth 2 recursive scan
    # -----------------------------
    if depth > 1 and discovered:

        print("\n[+] Starting Directory Brute Force (Depth 2)\n")

        depth2_results = set()

        for directory in discovered:

            wildcard = detect_wildcard(directory)

            tasks = [(directory, word, wildcard) for word in words]

            with ThreadPoolExecutor(max_workers=threads) as executor:

                for r in tqdm(
                    executor.map(check_directory, tasks),
                    total=len(tasks),
                    desc="Dir Bruteforce",
                    ascii="-#",
                    ncols=70
                ):

                    if r:
                        url, status = r
                        print(f"[+] Found -> {url} ({status})")
                        depth2_results.add(url)

        discovered.update(depth2_results)

        if not depth2_results:
            print("[!] No directories found at depth 2")

    return discovered