import os
import subprocess

def check_firewall():
    """
    Returns True if Firewall is Active, False if Inactive.
    """
    try:
        result = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True)
        
        if "Status: active" in result.stdout:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error checking firewall: {e}")
        return False


def check_ssh_root_login():
    """
    Returns True if Root Login is DISABLED (Safe).
    Returns False if Root Login is ENABLED (Risk).
    """
    try:
        cmd = ['sudo', 'grep', '^PermitRootLogin yes', '/etc/ssh/sshd_config']
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout.strip():
            return False
        else:
            return True
            
    except Exception as e:
        return True

def check_shadow_permissions():
    """
    Critical Security Control: Check if /etc/shadow is writable by everyone.
    If it is, ANY user can overwrite passwords and become root.
    """
    file_path = '/etc/shadow'

    try:
        file_stat = os.stat(file_path)

        if file_stat.st_mode & 0o002:
            return False
        else:
            return True

    except FileNotFoundError:
        return True
    except PermissionError:

        return True

def check_rogue_root():
    """
    Critical: Checks for non-root accounts with UID 0.
    Reference: CIS Benchmark 6.2.5 (Ensure root is the only UID 0 account)
    """
    try:
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.split(':')
                username = parts[0]
                uid = parts[2]

                if uid == '0' and username != 'root':
                    print(f"[ALERT] Rogue Root Account Detected: {username}")
                    return False

        return True

    except Exception as e:
        print(f"Error checking users: {e}")
        return False


# --- TEST AREA ---
if __name__ == "__main__":
    # This block only runs if 'python3 checks.py' is ran directly
    is_active = check_firewall()
    
    if is_active:
        print("[PASS] Firewall is currently ACTIVE.")
    else:
        print("[FAIL] Firewall is INACTIVE.")

    if check_ssh_root_login():
        print("[PASS] SSH Root Login is DISABLED (Safe).")
    else:
        print("[FAIL] SSH Root Login is ENABLED (Risk!).")

    if check_shadow_permissions():
        print("[PASS] /etc/shadow permissions are safe.")
    else:
        print("[FAIL] /etc/shadow is WORLD WRITABLE (Critical Risk!).")

    if check_rogue_root():
        print("[PASS] No rogue root accounts found.")
    else:
        print("[FAIL] ROGUE ROOT ACCOUNT DETECTED!")
