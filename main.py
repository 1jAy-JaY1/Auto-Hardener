#!/usr/bin/env python3
import os
import sys

if os.geteuid() != 0:
    print("[-] This script must be run as root.")
    sys.exit(1)

from logger import setup_logger
from checks import check_firewall, check_ssh_root_login, check_shadow_permissions, check_rogue_root
from hardener import remediate_firewall, remediate_ssh_root, remediate_shadow_permissions, remediate_rogue_root

logger = setup_logger()

def main():
    print("----  STARTING SECURITY RISK AUDIT  ----")
    logger.info("---- SECURITY AUDIT STARTED ----")

    print("\n[Phase 1] Scanning System...")
    score = 100

    is_firewall_active = check_firewall()
    if is_firewall_active:
        print("    Firewall is ACTIVE")
        logger.info("Firewall: ACTIVE")
    else:
        print("    Firewall is INACTIVE")
        score -= 20
        logger.warning("Firewall: INACTIVE")

    is_ssh_safe = check_ssh_root_login()
    if is_ssh_safe:
        print("    SSH Root Login is DISABLED")
        logger.info("SSH Root Login: DISABLED")
    else:
        print("    SSH Root Login is ENABLED")
        score -= 30
        logger.warning("SSH Root Login: ENABLED")

    is_shadow_safe = check_shadow_permissions()
    if is_shadow_safe:
        print("    /etc/shadow permissions are SAFE")
        logger.info("Shadow File: SAFE")
    else:
        print("    /etc/shadow is WORLD-WRITABLE")
        score -= 40
        logger.critical("Shadow File: WORLD-WRITABLE")

    is_root_safe, rogue_user = check_rogue_root()
    if is_root_safe:
        print("    No Rogue Root accounts found")
        logger.info("User Integrity: OK")
    else:
        print(f"    [ALERT] Rogue Root Account Detected: {rogue_user}")
        print("    ROGUE ROOT ACCOUNT DETECTED")
        score -= 50
        logger.critical(f"Rogue Root Account Detected: {rogue_user}")

    print("\n[Phase 2] Generating Risk Report...")
    score = max(0, score)
    print(f"    Current Security Score: {score}/100")
    logger.info(f"Security Score: {score}/100")

    if score == 100:
        print("    Risk Level: LOW")
        logger.info("Risk Level: LOW")
        print("\nSystem is secure. Exiting.")
        logger.info("---- AUDIT COMPLETE - SYSTEM SECURE ----")
        sys.exit(0)
    elif not is_root_safe:
        print("    Risk Level: HIGH")
        logger.info("Risk Level: HIGH")
    elif score >= 60:
        print("    Risk Level: MEDIUM")
        logger.info("Risk Level: MEDIUM")
    else:
        print("    Risk Level: HIGH")
        logger.info("Risk Level: HIGH")

    print("\n[Phase 3] Remediation")
    user_choice = input("    Issues found. Attempt auto-hardening? (y/n): ")

    if user_choice.lower() == 'y':
        logger.info("Remediation started by user")

        if not is_firewall_active:
            remediate_firewall(simulate=False)
        if not is_ssh_safe:
            remediate_ssh_root(simulate=False)
        if not is_shadow_safe:
            remediate_shadow_permissions(simulate=False)
        if not is_root_safe:
            remediate_rogue_root(rogue_user, simulate=False)

        print("\n    Fixes applied. Please re-run scan to verify.")
        logger.info("---- AUDIT COMPLETE - REMEDIATION APPLIED ----")
    else:
        print("\n    Remediation cancelled by user.")
        logger.info("Remediation declined by user")
        logger.info("---- AUDIT COMPLETE ----")

if __name__ == "__main__":
    main()
