import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
#Those are lists of types of vulnerabilites / attacks 
owaspTopTen = [
    "Broken Access Control",
    "Cryptographic Failures",
    "Injection",
    "Insecure Design",
    "Security Misconfiguration",
    "Vulnerable and Outdated Components",
    "Authentication Failures",
    "Software and Data Integrity Failures",
    "Logging and Monitoring Failures",
    "Server-Side Request Forgery (SSRF)"
]

cweTopTen = [
    "CWE-79: Cross-site Scripting (XSS)",
    "CWE-89: SQL Injection",
    "CWE-287: Improper Authentication",
    "CWE-434: Unrestricted Upload of File with Dangerous Type",
    "CWE-352: Cross-Site Request Forgery (CSRF)",
    "CWE-22: Improper Limitation of a Pathname to a Restricted Directory (Path Traversal)",
    "CWE-331: Insufficient Entropy",
    "CWE-250: Execution with Unnecessary Privileges",
    "CWE-426: Untrusted Search Path",
    "CWE-20: Improper Input Validation"
]

incidentTypes = [
    "Phishing",
    "Malware",
    "Ransomware",
    "DDoS",# short for distributed dinail of service
    "Brute Force",
    "SQLI",# short for SQL Injection
    "XSS", # short for cross site scripting
    "Unautho Access",
    "Data Breach",
    "Priv Esc", # short for Privilege Escalation
    "MITM", # short for man in the middle
    "Zero-Days",
    "Insider Threat",
    "Network Intrusion",
    "Creds Theft", # short for Credentials Theft
    "Email Compromise",
    "Supply Chain",
    "Config Error",
    "Sus Login Activity"# short for suspecious loging activity
]


affectedTargetsTypes=["Web","APK","IOS","Network","Web3","API"]

affectedScopeTemp = {
    "Web": ["*.muctf.tech","mohammadmahdishokor.dev","*.zaad.com"],
    "APK":["Scouts Guide apk","Trivia App"],
    "IOS":["Scouts Guide IOS"],
    "Network":["192.168.0.1"]
}

reporters = ["Mohammad Shokor","Hasan Sheet","0Day","guest"]
severityKeys = ["Low", "Medium", "High", "Critical"]


def ratingToSeverity(rating):
    if(rating<4):
        return "Low"
    elif(rating<7):
        return "Medium"
    elif(rating<9):
        return "High"
    else:
        return "Critical"
    
start = datetime(2025, 10, 27)
end = datetime.now()
reports = []
for _ in range(150):
    tempRating = round(np.random.uniform(0, 10), 1)
    reports.append({
            "name": reporters[np.random.randint(0, len(reporters))],
            "title": "",
            "type": incidentTypes[np.random.randint(0, len(incidentTypes))],
            "rating": f"{tempRating:.1f}",
            "severity": ratingToSeverity(tempRating),
            "description": "",
            "time":  (start + timedelta(seconds=np.random.randint(0, int((end - start).total_seconds())))).date(), # random date between 27 of october 2025 (the date I started bughunting) and today's date
            "affectedTargets": np.random.choice(
                affectedTargetsTypes,
                size=np.random.randint(1, 4),
                replace=False
            ).tolist()
    })