import json
from pathlib import Path
from datetime import datetime

reportsFile = Path(__file__).with_name("reports.json")
reportersFile = Path(__file__).with_name("reporters.json")  # fixed typo

def load_reports():
    if reportsFile.exists():
        with open(reportsFile, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_reports(items):
    with open(reportsFile, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def load_reporters():
    if reportersFile.exists():
        with open(reportersFile, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_reporters(items):
    with open(reportersFile, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def addReporter(name):
    items = load_reporters()
    if name not in items:
        items.append({"name":name})
        save_reporters(items)

def addReport(
    name,
    title,
    type,
    rating,
    severity,
    description,
    time,
    affectedTargets=None,
    affetecTargets=None,  # backward compatibility
):
    targets = affectedTargets if affectedTargets is not None else (affetecTargets or [])

    new_report = {
        "name": name,
        "title": title,
        "type": type,
        "rating": rating,
        "severity": severity,
        "description": description,
        "time": str(time),
        "affectedTargets": targets,
    }

    items = load_reports()
    items.append(new_report)
    save_reports(items)
    addReporter(name)


rep = load_reporters()
reporters = [item["name"] if isinstance(item, dict) else item for item in rep]
reports=load_reports()
start = datetime(2025, 10, 27)
end = datetime.now()

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
    "Unauth Access",
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
# reports = []

#how random reports are made : 
# for _ in range(200):
#     tempRating = round(np.random.uniform(0, 10), 1)
#     reports.append({
#             "name": reporters[np.random.randint(0, len(reporters))],
#             "title": "",
#             "type": incidentTypes[np.random.randint(0, len(incidentTypes))],
#             "rating": f"{tempRating:.1f}",
#             "severity": ratingToSeverity(tempRating),
#             "description": "",
#             "time":  (start + timedelta(seconds=np.random.randint(0, int((end - start).total_seconds())))).date(), # random date between 27 of october 2025 (the date I started bughunting) and today's date
#             "affectedTargets": np.random.choice(
#                 affectedTargetsTypes,
#                 size=np.random.randint(1, 4),
#                 replace=False
#             ).tolist()
#     })


