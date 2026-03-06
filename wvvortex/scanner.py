import requests
import argparse
from tqdm import tqdm
from colorama import Fore, init

from .crawler import crawl
from .report_generator import generate_report
from .json_report import generate_json_report
from .dir_bruteforce import brute_force_dirs
from .param_discovery import discover_parameters
from .param_fuzzer import fuzz_parameters
from .tech_detector import detect_technologies

init(autoreset=True)

# --------------------------------------------------
# WVVortex Banner
# --------------------------------------------------

BANNER = r"""
██╗    ██╗ ██╗   ██╗  ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗
██║    ██║ ██║   ██║  ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
██║ █╗ ██║ ██║   ██║  ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝
██║███╗██║ ╚██╗ ██╔   ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗
╚███╔███╔╝  ╚████╔╝    ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗
 ╚══╝╚══╝    ╚═══╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

WVVortex - Web Vulnerability Scanner
Author  : Cybe07._
Version : 1.0
"""

# -----------------------------
# Global variables
# -----------------------------
missing_headers = []
xss_vulnerable_urls = []
sqli_vulnerable_urls = []
technologies = []

# -----------------------------
# Load payloads
# -----------------------------
def load_payloads(file_path):

    payloads = []

    with open(file_path, "r") as f:
        for line in f:
            payload = line.strip()

            if payload:
                payloads.append(payload)

    return payloads


# -----------------------------
# Security Header Scanner
# -----------------------------
def check_security_headers(url):

    print("\n[*] Checking Security Headers\n")

    important_headers = [
        "X-Frame-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options"
    ]

    try:

        response = requests.get(url, timeout=5)
        headers = response.headers

        for header in important_headers:

            if header not in headers:

                print(Fore.GREEN + f"[+] Missing header -> {header}")
                missing_headers.append(header)

            else:

                print(Fore.GREEN + f"[+] Header present -> {header}")

    except:
        print("[-] Could not check headers")


# -----------------------------
# XSS Scanner
# -----------------------------
def scan_xss(urls, payloads):

    print("\n[+] Starting XSS Scan\n")

    for url in tqdm(
        urls,
        desc="Scanning XSS",
        ascii="-#",
        ncols=70,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
    ):

        if "=" not in url:
            continue

        for payload in payloads:

            test_url = url + payload

            try:

                response = requests.get(test_url, timeout=5)

                if payload in response.text:

                    tqdm.write(
                        Fore.GREEN +
                        f"[+] XSS Vulnerability (Reflected) -> {url}"
                    )

                    xss_vulnerable_urls.append(url)
                    break

            except:
                pass


# -----------------------------
# SQL Injection Scanner
# -----------------------------
SQL_ERRORS = [
    "sql syntax",
    "mysql_fetch",
    "syntax error",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "pdoexception",
    "odbc sql server driver",
]


def scan_sqli(urls, payloads):

    print("\n[+] Starting SQL Injection Scan\n")

    for url in tqdm(
        urls,
        desc="Scanning SQLi",
        ascii="-#",
        ncols=70,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
    ):

        if "=" not in url:
            continue

        vulnerable = False

        for payload in payloads:

            test_url = url + payload

            try:

                response = requests.get(test_url, timeout=5)
                text = response.text.lower()

                for error in SQL_ERRORS:

                    if error in text:

                        tqdm.write(
                            Fore.GREEN +
                            f"[+] SQL Injection (Error-Based) -> {url}"
                        )

                        sqli_vulnerable_urls.append(url)
                        vulnerable = True
                        break

                if vulnerable:
                    break

            except:
                pass


# -----------------------------
# Scan Summary
# -----------------------------
def print_summary(urls):

    print("\n==============================")
    print("        SCAN SUMMARY")
    print("==============================")

    print(f"Pages Crawled: {len(urls)}")
    print(f"Missing Headers: {len(missing_headers)}")
    print(f"XSS Vulnerabilities: {len(xss_vulnerable_urls)}")
    print(f"SQL Injection Vulnerabilities: {len(sqli_vulnerable_urls)}")

    score = 100 - (
        len(missing_headers) * 5 +
        len(xss_vulnerable_urls) * 20 +
        len(sqli_vulnerable_urls) * 25
    )

    if score < 0:
        score = 0

    print(f"\nSecurity Score: {score}/100")

    if score > 80:
        risk_level = "LOW"
    elif score > 50:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    print(f"Risk Level: {risk_level}")

    return score, risk_level


# -----------------------------
# Main
# -----------------------------
def main():

    parser = argparse.ArgumentParser(
        prog="wvvortex",
        description="""
WVVortex - Web Vulnerability Scanner

Capabilities:
 • Web Crawling
 • Parameter Discovery
 • Parameter Fuzzing
 • Directory Bruteforce
 • XSS Detection
 • SQL Injection Detection
 • Security Header Analysis
 • Technology Detection
 • PDF & JSON Reporting
""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-u", "--url", required=True, help="Target URL")

    parser.add_argument(
        "--crawl",
        action="store_true",
        help="Run crawler only (URL discovery)"
    )

    parser.add_argument(
        "--dir",
        action="store_true",
        help="Directory brute force scan"
    )

    parser.add_argument(
        "--scan",
        action="store_true",
        help="Run vulnerability scanning (XSS, SQL Injection, Security Headers)"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full scan (crawl + param discovery + fuzzing + dir scan + vuln scan)"
    )

    parser.add_argument(
        "-w",
        "--wordlist",
        help="Custom wordlist for directory scanning"
    )

    parser.add_argument(
        "--stealth",
        action="store_true",
        help="Enable stealth mode"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Threads used for directory brute forcing"
    )

    args = parser.parse_args()
    target = args.url

    print(BANNER)

    if args.stealth:
        print("[+] Stealth Mode Enabled\n")

    urls = set()

    # -----------------------------
    # Crawl
    # -----------------------------
    if args.crawl or args.full or args.scan:

        urls = set(crawl(target))
        urls.add(target)

        print("\nDiscovered URLs:")
        for url in sorted(urls):
            print(url)

    # -----------------------------
    # Technology Detection
    # -----------------------------
    techs = detect_technologies(target)

    if techs:
        technologies.extend(techs)

    # -----------------------------
    # Parameter Discovery
    # -----------------------------
    params = discover_parameters(urls)
    urls.update(params)

    # -----------------------------
    # Parameter Fuzzing
    # -----------------------------
    fuzzed = fuzz_parameters(urls)
    urls.update(fuzzed)

    # -----------------------------
    # Directory Brute Force
    # -----------------------------
    if args.dir or args.full:

        wordlist = args.wordlist if args.wordlist else "payloads/discovery.txt"

        dirs = brute_force_dirs(
            target,
            wordlist,
            threads=args.threads
        )

        urls.update(dirs)

    # -----------------------------
    # Vulnerability Scanning
    # -----------------------------
    if args.scan or args.full:

        check_security_headers(target)

        xss_payloads = load_payloads("payloads/xss.txt")
        sqli_payloads = load_payloads("payloads/sqli.txt")

        scan_xss(urls, xss_payloads)
        scan_sqli(urls, sqli_payloads)

        score, risk_level = print_summary(urls)

        generate_report(
            target,
            urls,
            missing_headers,
            xss_vulnerable_urls,
            sqli_vulnerable_urls,
            technologies,
            score,
            risk_level
        )

        generate_json_report(
            target,
            urls,
            missing_headers,
            len(xss_vulnerable_urls),
            len(sqli_vulnerable_urls)
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        print("[+] Cleaning up threads...")
        print("[+] Goodbye from WVVortex 🌀")