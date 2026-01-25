# Auto-Hardener: Adaptive Security Risk Engine

## Overview
Auto-Hardener is a Python-based automated security auditing tool designed to detect, score, and remediate system misconfigurations on Linux environments. It assesses system integrity against industry-standard benchmarks (CIS) and provides immediate remediation capabilities.

The tool calculates a dynamic risk score (0-100) based on critical security controls, including firewall status, SSH configurations, file permissions, and user identity integrity.

## Key Features

### 1. Automated Compliance Auditing
The engine performs real-time scans of the following security controls:
* **Network Security:** Verifies the status of the Uncomplicated Firewall (UFW) to ensure network traffic is regulated.
* **Access Control:** Audits `/etc/ssh/sshd_config` to detect and flag Root Login permission (PermitRootLogin).
* **System Integrity:** Inspects critical file permissions, specifically checking if `/etc/shadow` is world-writable (referencing CIS Benchmark 6.1.10).
* **Identity Management:** Scans the `/etc/passwd` database for "Rogue Root" accounts (non-root users with UID 0), a common indicator of backdoor compromise.

### 2. Adaptive Risk Scoring
* Calculates a weighted security score based on the severity of detected vulnerabilities.
* High-risk findings (such as Rogue Root accounts or exposed password files) incur significant score penalties to prioritize critical remediation.

### 3. Interactive Auto-Remediation
* **Hardening Engine:** Automatically applies fixes for detected vulnerabilities using system calls.
* **Safety Interlocks:** Features a "Human-in-the-Loop" confirmation workflow for high-risk operations, such as deleting user accounts, to prevent accidental system damage.
* **Simulation Mode:** Capable of dry-running remediation commands to preview changes without altering system state.

## Technical Architecture
* **Language:** Python 3
* **Dependencies:** Standard Library only (`os`, `sys`, `subprocess`) — No external PIP packages required.
* **Platform:** Linux (Tested on Kali Linux, Ubuntu, Debian).
* **Privileges:** Requires Root/Sudo privileges to modify system configurations.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/1jAy-JaY1/Auto-Hardener.git
cd AutoHardener
