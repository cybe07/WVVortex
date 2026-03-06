import requests


def detect_technologies(url):

    print("\n[+] Detecting Technologies\n")

    tech = []

    try:
        response = requests.get(url, timeout=5)

        headers = response.headers
        body = response.text.lower()

    except:
        print("[-] Could not analyze technologies")
        return []

    # Server detection
    if "server" in headers:
        tech.append(f"Server: {headers['server']}")

    # PHP detection
    if ".php" in body or "php" in body:
        tech.append("Language: PHP")

    # Apache detection
    if "apache" in str(headers).lower():
        tech.append("Web Server: Apache")

    # jQuery detection
    if "jquery" in body:
        tech.append("Framework: jQuery")

    # WordPress detection
    if "wp-content" in body or "wordpress" in body:
        tech.append("CMS: WordPress")

    # Bootstrap detection
    if "bootstrap" in body:
        tech.append("Framework: Bootstrap")

    # MySQL detection
    if "mysql" in body:
        tech.append("Database: MySQL")

    if tech:

        for t in tech:
            print(f"[+] {t}")

    else:

        print("[-] No technologies detected")

    return tech