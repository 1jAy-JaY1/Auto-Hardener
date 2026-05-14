import logging
import subprocess

logger = logging.getLogger("AutoHardener")

def apply_fix(fix_name, command, simulate=True):
    """Master function that runs or simulates all fixes."""
    print(f"[+] Attempting to fix: {fix_name}...")

    if simulate:
        print(f"    [SIMULATION] Would run command: {' '.join(command)}")
        print(f"    [SIMULATION] {fix_name} simulated successfully.\n")
        logger.info(f"SIMULATED: {fix_name} - no changes made")
        return True
    else:
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
            print(f"    [SUCCESS] {fix_name} applied successfully.\n")
            logger.info(f"FIX APPLIED: {fix_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"    [ERROR] Failed to apply {fix_name}.")
            print(f"    Error details: {e}\n")
            logger.error(f"FIX FAILED: {fix_name} - {e}")
            return False

def remediate_firewall(simulate=True):
    """Fix 1: Enable the UFW Firewall."""
    return apply_fix("Enable Firewall (UFW)", ['ufw', 'enable'], simulate)

def remediate_ssh_root(simulate=True):
    """Fix 2: Disable Root Login for SSH and restart SSH service."""
    cmd = [
        'sed', '-i',
        's/PermitRootLogin yes/PermitRootLogin no/g;s/PermitRootLogin prohibit-password/PermitRootLogin no/g;s/PermitRootLogin without-password/PermitRootLogin no/g',
        '/etc/ssh/sshd_config'
    ]
    result = apply_fix("Disable SSH Root Login", cmd, simulate)
    if result:
        return apply_fix("Restart SSH Service", ['systemctl', 'restart', 'ssh'], simulate)
    return False

def remediate_shadow_permissions(simulate=True):
    """Fix 3: Set strict permissions on /etc/shadow."""
    return apply_fix("Secure Shadow File Permissions", ['chmod', '640', '/etc/shadow'], simulate)

def remediate_rogue_root(rogue_user, simulate=True):
    """Fix 4: Delete any user with UID 0 that is not root."""
    if rogue_user:
        print(f"\n    [!] WARNING: You are about to DELETE user '{rogue_user}'.")
        print(f"    This cannot be undone.")
        confirm = input(f"    Are you sure you want to proceed? (y/n): ")

        if confirm.lower() == 'y':
            return apply_fix(f"Remove Rogue User ({rogue_user})", ['userdel', '-f', rogue_user], simulate)
        else:
            print("    [INFO] Skipping Rogue Root remediation.")
            logger.info(f"Rogue root remediation skipped by user for: {rogue_user}")
            return False
    else:
        print("    [INFO] No rogue user found to remove.")
        return False
