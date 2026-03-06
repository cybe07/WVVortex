import json
import os


def generate_json_report(
    target,
    urls,
    missing_headers,
    xss_count,
    sqli_count
):

    os.makedirs("output", exist_ok=True)

    score = 100 - (
        len(missing_headers) * 5 +
        xss_count * 20 +
        sqli_count * 25
    )

    if score < 0:
        score = 0

    if score > 80:
        risk = "LOW"
    elif score > 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    report = {
        "target": target,
        "pages_crawled": len(urls),
        "missing_headers": missing_headers,
        "xss_vulnerabilities": xss_count,
        "sqli_vulnerabilities": sqli_count,
        "security_score": score,
        "risk_level": risk
    }

    with open("output/report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\n[✔] JSON Report Generated → output/report.json")