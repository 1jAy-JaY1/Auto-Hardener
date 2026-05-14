import os
import subprocess

def check_firewall():
    """Returns True if firewall is active, False if inactive."""
    try:
        result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
        return "Status: active" in result.stdout
    except Exception as e:
        print(f"[ERROR] Error checking firewall: {e}")
        return False

def check_ssh_root_login():
    """Returns True if Root Login is DISABLED, False if ENABLED."""
    risky_values = (
        'PermitRootLogin yes',
        'PermitRootLogin prohibit-password',
        'PermitRootLogin without-password'
    )
    try:
        with open('/etc/ssh/sshd_config', 'r') as f:
            for line in f:
                if line.strip().startswith(risky_values):
                    return False
        return True
    except FileNotFoundError:
        print("[ERROR] sshd_config not found. Is SSH installed?")
        return False
    except PermissionError:
        print("[ERROR] Permission denied reading sshd_config.")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error checking SSH config: {e}")
        return False

def check_shadow_permissions():
    """Returns True if /etc/shadow permissions are safe, False if world-writable."""
    try:
        file_stat = os.stat('/etc/shadow')
        if file_stat.st_mode & 0o002:
            return False
        return True
    except FileNotFoundError:
        print("[ERROR] /etc/shadow not found.")
        return False
    except PermissionError:
        print("[ERROR] Permission denied checking /etc/shadow.")
        return False

def check_rogue_root():
    """
    Returns (True, None) if no rogue root accounts found.
    Returns (False, username) if a rogue root account is detected.
    Reference: CIS Benchmark 6.2.5
    """
    try:
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) < 4:
                    continue
                username = parts[0]
                uid = parts[2]
                if uid == '0' and username != 'root':
                    return False, username
        return True, None
    except Exception as e:
        print(f"[ERROR] Error checking users: {e}")
        return False, None
