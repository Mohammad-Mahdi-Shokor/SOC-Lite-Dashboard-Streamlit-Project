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
    "DDoS Attack",
    "Brute Force Attack",
    "SQL Injection",
    "Cross-Site Scripting (XSS)",
    "Unauthorized Access",
    "Data Breach",
    "Privilege Escalation",
    "Man-in-the-Middle (MITM)",
    "Zero-Day Exploit",
    "Insider Threat",
    "System Compromise",
    "Network Intrusion",
    "Credential Theft",
    "Business Email Compromise",
    "Supply Chain Attack",
    "Configuration Error",
    "Suspicious Login Activity"
]


affectedTargetsTypes=["Web","APK","IOS","Network","Web3","API"]

affectedScopeTemp = {
    "Web": ["*.muctf.tech","mohammadmahdishokor.dev","*.zaad.com"],
    "APK":["Scouts Guide apk","Trivia App"],
    "IOS":["Scouts Guide IOS"],
    "Network":["192.168.0.1"]
}