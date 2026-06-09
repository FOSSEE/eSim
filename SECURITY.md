# 🔒 Security Policy

The eSim project takes security seriously. As a desktop EDA application handling various local file formats, external executables (Ngspice, GHDL, KiCad), and third-party models, we are committed to providing a secure environment for our users.

---

## ✅ Supported Versions

Security updates are provided for the latest stable release of eSim. Older releases may receive critical patches at the discretion of the core maintainers.

| eSim Version | Status | Security Support |
| :--- | :--- | :--- |
| **2.5.x** | Current Stable | 🟢 Supported |
| **2.4.x** | Previous Stable | 🟡 Critical Fixes Only |
| **< 2.4** | End of Life | 🔴 Not Supported |

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability in eSim (or its integration with bundled tools like Ngspice or GHDL), **please do not report it through public GitHub issues.** Instead, we ask that you practice responsible disclosure.

### Where to Report
Please email your findings to the core security team at:
📧 **contact-esim@fossee.in** (Subject: `[SECURITY] Vulnerability Report`)

### What to Include
To help us quickly understand and reproduce the issue, please include the following in your report:
- **Description:** A clear summary of the vulnerability and its potential impact (e.g., Local Privilege Escalation, Arbitrary Code Execution via crafted netlists).
- **Environment:** Your OS version, Python version, and the eSim version.
- **Reproduction Steps:** Step-by-step instructions, including any malicious/crafted `.cir`, `.sch`, or XML files used.
- **Proof of Concept (PoC):** Code snippets or a video demonstrating the exploit, if possible.

### Expected Response Timeline
- **Acknowledgement:** We will acknowledge receipt of your vulnerability report within **48 hours**.
- **Assessment:** A preliminary assessment and timeline for a patch will be provided within **1 week**.
- **Fix & Disclosure:** We aim to release a patch and issue a CVE (if applicable) within **30-90 days**, depending on the severity and complexity of the issue. We will keep you updated throughout the process.

---

## 🛡️ Scope of Security

When reporting vulnerabilities, please keep in mind the architecture of eSim. 

### In-Scope (Please Report)
- Vulnerabilities in the core Python application (`src/` codebase).
- Arbitrary code execution triggered by opening malicious eSim projects, `.xml` files, or schematic files.
- Insecure handling of permissions or temporary directories during the KiCad-to-Ngspice conversion pipeline.

### Out-of-Scope (Do Not Report Here)
- Upstream vulnerabilities strictly within the core engines of **KiCad**, **Ngspice**, or **GHDL** that are not exacerbated by eSim's wrapper implementations. Please report these directly to their respective upstream maintainers.
- Social engineering, phishing, or physical access attacks.

---

*Thank you for helping keep the eSim community safe and secure!*
