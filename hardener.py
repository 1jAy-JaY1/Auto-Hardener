import subprocess

def apply_fix(fix_name, command, simulate=True):
    """
    The Master Function that runs all fixes.
    
    Args:
        fix_name (str): A human-readable name for the fix (e.g., "Enable Firewall").
        command (list): The actual Linux command to run (e.g., ['ufw', 'enable']).
        simulate (bool): If True, it ONLY prints what it would do. If False, it actually runs it.
    """
    print(f"[+] Attempting to fix: {fix_name}...")

    if simulate:
        # SAFETY NET: Just print the command, don't run it.
        print(f"    [SIMULATION] Would run command: {' '.join(command)}")
        print(f"    [SIMULATION] {fix_name} simulated successfully.\n")
        return True
    else:
        # DANGER ZONE: Actually run the command.
        try:
            # I used 'sudo' here because hardening usually requires root
            full_command = ['sudo'] + command
            
            subprocess.run(full_command, check=True, stdout=subprocess.DEVNULL)
            print(f"    [SUCCESS] {fix_name} applied successfully.\n")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"    [ERROR] Failed to apply {fix_name}.")
            print(f"    Error details: {e}\n")
            return False

# --- SPECIFIC FIXES BELOW ---

def remediate_firewall(simulate=True):
    """
    Fix 1: Enable the UFW Firewall
    """
    cmd = ['ufw', 'enable']
    apply_fix("Enable Firewall (UFW)", cmd, simulate)

def remediate_ssh_root(simulate=True):
    """
    Fix 2: Disable Root Login for SSH (Advanced but common)
    This uses 'sed' to edit the config file.
    """
    # This command finds 'PermitRootLogin yes' and changes it to 'no'
    cmd = ['sed', '-i', 's/PermitRootLogin yes/PermitRootLogin no/g', '/etc/ssh/sshd_config']
    apply_fix("Disable SSH Root Login", cmd, simulate)

def remediate_shadow_permissions(simulate=True):
    """
    Fix: Removes write permissions for 'others' on /etc/shadow.
    Command: chmod o-w /etc/shadow
    """
    cmd = ['chmod', 'o-w', '/etc/shadow']
    apply_fix("Secure Shadow File Permissions", cmd, simulate)

def remediate_rogue_root(simulate=True):
    """
    Fix: Deletes any user with UID 0 that is NOT 'root'.
    Includes a SAFETY CHECK to prevent accidental deletion.
    """
    find_cmd = "awk -F: '($3 == 0 && $1 != \"root\") {print $1}' /etc/passwd"
    
    try:
        result = subprocess.run(find_cmd, shell=True, capture_output=True, text=True)
        rogue_user = result.stdout.strip()
        
        if rogue_user:
            # SAFETY CHECK(Cross Check)
            print(f"\n    [!] WARNING: You are about to DELETE user '{rogue_user}'.")
            print(f"    This cannot be undone.")
            confirm = input(f"    Are you sure you want to proceed? (y/n): ")
            
            if confirm.lower() == 'y':
                cmd = ['userdel', '-f', rogue_user]
                apply_fix(f"Remove Rogue User ({rogue_user})", cmd, simulate)
            else:
                print("    [INFO] Skipping Rogue Root remediation.")
        else:
            print("    [INFO] No rogue user found to remove.")
            
    except Exception as e:
        print(f"    [ERROR] Could not remove rogue user: {e}")



# --- TEST AREA ---
if __name__ == "__main__":
    print("--- Starting Auto-Hardener (TEST MODE) ---")
    
    remediate_firewall(simulate=False)
    remediate_ssh_root(simulate=True)
