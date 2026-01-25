#!/usr/bin/env python3
import sys

from checks import check_firewall, check_ssh_root_login, check_shadow_permissions, check_rogue_root
from hardener import remediate_firewall, remediate_ssh_root, remediate_shadow_permissions, remediate_rogue_root

def main():
    print("----  STARTING SECURITY RISK AUDIT  ----")
    
    # --- STEP 1: THE SCAN ---
    print("\n[Phase 1] Scanning System...")
    
    score = 100
    report = []
    
# --- Check 1: Firewall Check
    is_firewall_active = check_firewall()
    
    if is_firewall_active:
        print("    Firewall is ACTIVE")
        report.append("Firewall: OK")
    else:
        print("    Firewall is INACTIVE")
        score = score - 20
        report.append("Firewall: FAIL")

# --- Check 2: SSH Root Login ---
    is_ssh_safe = check_ssh_root_login()

    if is_ssh_safe:
        print("    SSH Root Login is DISABLED")
        report.append("SSH: OK")
    else:
        print("    SSH Root Login is ENABLED")
        score = score - 30 
        report.append("SSH: FAIL")

# --- Check 3: Critical File Permissions (CIS 6.1.10) ---
    is_shadow_safe = check_shadow_permissions()

    if is_shadow_safe:
        print("    /etc/shadow permissions are SAFE")
        report.append("Shadow File: OK")
    else:
        print("    /etc/shadow is WORLD-WRITABLE")
        score = score - 40
        report.append("Shadow File: FAIL")

# --- Check 4: Rogue Root (Backdoor Detection) ---
    is_root_safe = check_rogue_root()

    if is_root_safe:
        print("    No Rogue Root accounts found")
        report.append("User Integrity: OK")
    else:
        print("    ROGUE ROOT ACCOUNT DETECTED")
        score = score - 50
        report.append("User Integrity: FAIL")



    # --- STEP 2: THE REPORT ---
    print("\n[Phase 2] Generating Risk Report...")
    print(f"   Current Security Score: {score}/100")
    
    if score < 100:
        print("    Risk Level: HIGH")
    else:
        print("    Risk Level: LOW")
        print("\nSystem is secure. Exiting.")
        sys.exit()

    # --- STEP 3: THE AUTO-FIX ---
    print("\n[Phase 3] Remediation")
    user_choice = input("   Critical issues found. Attempt auto-hardening? (y/n): ")
    
    if user_choice.lower() == 'y':
        # Firewall fix
        if not is_firewall_active:
            remediate_firewall(simulate=False)

        # SSH fix
        if not is_ssh_safe:
            remediate_ssh_root(simulate=False)

	# Shadow File Fix
        if not is_shadow_safe:
            remediate_shadow_permissions(simulate=False)

        # Rogue Root Fix
        if not is_root_safe:
            remediate_rogue_root(simulate=False)
            
        print("\n    Fixes applied. Please re-run scan to verify.")
    else:
        print("\n    Remediation cancelled by user.")


if __name__ == "__main__":
    main()
