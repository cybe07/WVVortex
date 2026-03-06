from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def generate_report(
    target,
    urls,
    missing_headers,
    xss_vulns,
    sqli_vulns,
    technologies,
    security_score,
    risk_level
):

    file_path = "output/report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    y = 750

    # -----------------------------
    # Title
    # -----------------------------
    c.setFont("Helvetica-Bold", 20)
    c.drawString(170, y, "WV VORTEX Security Report")

    y -= 40

    c.setFont("Helvetica", 12)

    scan_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    c.drawString(50, y, f"Target: {target}")
    y -= 20
    c.drawString(50, y, f"Scan Date: {scan_date}")

    y -= 30

    # -----------------------------
    # Executive Summary
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Executive Summary")

    y -= 20
    c.setFont("Helvetica", 11)

    summary = (
        "The automated scan identified potential security issues including "
        "missing security headers and injection vulnerabilities. "
        "Immediate remediation is recommended to reduce the attack surface."
    )

    c.drawString(50, y, summary)

    y -= 40

    # -----------------------------
    # Scan Statistics
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Scan Statistics")

    y -= 20
    c.setFont("Helvetica", 11)

    c.drawString(50, y, f"Pages Crawled: {len(urls)}")
    y -= 20
    c.drawString(50, y, f"XSS Vulnerabilities: {len(xss_vulns)}")
    y -= 20
    c.drawString(50, y, f"SQL Injection Vulnerabilities: {len(sqli_vulns)}")

    y -= 40

    # -----------------------------
    # Technology Detection
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Technology Detection")

    y -= 20
    c.setFont("Helvetica", 11)

    if technologies:
        for tech in technologies:
            c.drawString(50, y, f"- {tech}")
            y -= 15
    else:
        c.drawString(50, y, "No technologies detected")
        y -= 15

    y -= 25

    # -----------------------------
    # Security Headers
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Missing Security Headers")

    y -= 20
    c.setFont("Helvetica", 11)

    if missing_headers:
        for header in missing_headers:
            c.drawString(50, y, f"- {header}")
            y -= 15
    else:
        c.drawString(50, y, "No missing security headers detected")
        y -= 15

    y -= 25

    # -----------------------------
    # Vulnerability Details
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Vulnerability Details")

    y -= 20
    c.setFont("Helvetica", 11)

    # XSS
    if xss_vulns:
        c.drawString(50, y, "Reflected XSS:")
        y -= 15

        for url in xss_vulns:
            c.drawString(60, y, url)
            y -= 15

        y -= 10

    # SQLi
    if sqli_vulns:
        c.drawString(50, y, "SQL Injection:")
        y -= 15

        for url in sqli_vulns:
            c.drawString(60, y, url)
            y -= 15

    y -= 30

    # -----------------------------
    # Risk Score
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Risk Assessment")

    y -= 20
    c.setFont("Helvetica", 11)

    c.drawString(50, y, f"Security Score: {security_score}/100")
    y -= 15
    c.drawString(50, y, f"Risk Level: {risk_level}")

    # Save report
    c.save()

    print(f"\n[✔] PDF Report Generated → {file_path}")