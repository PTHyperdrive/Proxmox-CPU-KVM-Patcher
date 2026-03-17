"""
VM configuration patching: builds QEMU args lines with anti-detection
CPU flags and SMBIOS tables, patches .conf files, backup/restore.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

from utils import C, info, warn, error, step, header, random_serial


# ============================================================================
#  BUILD QEMU ARGS LINE
# ============================================================================

def build_args_line(profile):
    """Build the QEMU args line with all anti-detection flags."""

    serial_bios  = random_serial(profile.get("serial_prefix", "OEM"), 8)
    serial_board = random_serial(profile.get("serial_prefix", "OEM"), 10)
    serial_ram   = random_serial("", 8)

    manufacturer   = profile["manufacturer"]
    product        = profile["product"]
    bios_vendor    = profile.get("bios_vendor", "American Megatrends Inc.")
    bios_version   = profile.get("bios_version", "1.0")
    board_product  = profile.get("board_product", product)
    board_version  = profile.get("board_version", "1.0")
    chassis_vendor = profile.get("chassis_vendor", manufacturer)
    ram_manufacturer = profile.get("ram_manufacturer", "Kingston")
    ram_part       = profile.get("ram_part", "KHX3200C16D4/16GX")
    ram_speed      = profile.get("ram_speed", 3200)
    hv_vendor      = profile.get("hv_vendor_id", "GenuineIntel")

    # CPU flags for anti-detection
    cpu_args = (
        f"-cpu host,"
        f"+kvm_pv_unhalt,+kvm_pv_eoi,"
        f"hv_spinlocks=0x1fff,hv_vapic,hv_time,hv_reset,"
        f"hv_vpindex,hv_runtime,hv_relaxed,"
        f"kvm=off,hv_vendor_id={hv_vendor},"
        f"vmware-cpuid-freq=false,enforce=false,"
        f"host-phys-bits=true,hypervisor=off"
    )

    # SMBIOS tables for hardware spoofing
    smbios = [
        f"-smbios type=0,vendor={bios_vendor},version={bios_version}",
        f"-smbios type=1,manufacturer={manufacturer},product={product},version=1.0,serial={serial_bios}",
        f"-smbios type=2,manufacturer={manufacturer},product={board_product},version={board_version},serial={serial_board}",
        f"-smbios type=3,manufacturer={chassis_vendor}",
        f"-smbios type=4,manufacturer=Intel,max-speed=5200,current-speed=4800",
        f"-smbios type=17,manufacturer={ram_manufacturer},speed={ram_speed},part={ram_part},serial={serial_ram}",
    ]

    return f"args: {cpu_args} " + " ".join(smbios)


# ============================================================================
#  PATCH / RESTORE VM CONFIG
# ============================================================================

def patch_vm_config(conf_directory, vmid, profile):
    """Patch a VM configuration file with anti-detection args."""
    file_path = os.path.join(conf_directory, f"{vmid}.conf")

    if not os.path.exists(file_path):
        error(f"VM config {vmid}.conf not found in {conf_directory}")
        return False

    with open(file_path, 'r') as f:
        lines = f.readlines()

    args_line = build_args_line(profile)

    new_lines = []
    args_found = False
    balloon_found = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("args:"):
            new_lines.append(args_line + "\n")
            args_found = True
            continue

        if stripped.startswith("balloon:"):
            new_lines.append("balloon: 0\n")
            balloon_found = True
            continue

        new_lines.append(line)

    if not args_found:
        new_lines.insert(0, args_line + "\n")

    if not balloon_found:
        new_lines.append("balloon: 0\n")

    # Backup original
    backup_path = file_path + f".bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    info(f"Backup saved: {backup_path}")

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    info(f"Patched {vmid}.conf with anti-detection args")
    return True


def restore_vm_config(conf_directory, vmid):
    """Remove anti-detection args from a VM config file."""
    file_path = os.path.join(conf_directory, f"{vmid}.conf")

    if not os.path.exists(file_path):
        error(f"VM config {vmid}.conf not found in {conf_directory}")
        return False

    backups = sorted(Path(conf_directory).glob(f"{vmid}.conf.bak.*"), reverse=True)

    if backups:
        print(f"\n  {C.YELLOW}Found backups:{C.RESET}")
        for idx, bak in enumerate(backups[:5], 1):
            print(f"    {idx}. {bak.name}")

        choice = input(f"\n  Restore from backup? [1-{min(5,len(backups))}] or 'n' to strip args: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= min(5, len(backups)):
            shutil.copy2(str(backups[int(choice)-1]), file_path)
            info(f"Restored from {backups[int(choice)-1].name}")
            return True

    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = [l for l in lines if not l.strip().startswith("args:")]

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    info(f"Stripped args line from {vmid}.conf")
    return True


# ============================================================================
#  DISPLAY / LIST HELPERS
# ============================================================================

def show_vm_config(conf_directory, vmid):
    """Display the current VM configuration with color highlights."""
    file_path = os.path.join(conf_directory, f"{vmid}.conf")
    if not os.path.exists(file_path):
        error(f"VM config {vmid}.conf not found.")
        return

    header(f"VM {vmid} Configuration")
    with open(file_path, 'r') as f:
        content = f.read()

    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith("args:"):
            print(f"  {C.GREEN}{line}{C.RESET}")
        elif stripped.startswith("balloon:"):
            print(f"  {C.YELLOW}{line}{C.RESET}")
        elif stripped.startswith("cpu:"):
            print(f"  {C.CYAN}{line}{C.RESET}")
        elif stripped.startswith("smbios"):
            print(f"  {C.MAGENTA}{line}{C.RESET}")
        else:
            print(f"  {line}")


def list_vms(conf_directory):
    """List all VMs found in the config directory."""
    if not os.path.exists(conf_directory):
        warn(f"Config directory not found: {conf_directory}")
        return []

    vms = []
    for f in sorted(os.listdir(conf_directory)):
        if f.endswith('.conf') and '.bak' not in f:
            vmid = f.replace('.conf', '')
            conf_path = os.path.join(conf_directory, f)
            name = "Unknown"
            has_args = False
            with open(conf_path, 'r') as cf:
                for line in cf:
                    if line.strip().startswith("name:"):
                        name = line.split(":", 1)[1].strip()
                    if line.strip().startswith("args:"):
                        has_args = True

            icon = f"{C.GREEN}✓{C.RESET}" if has_args else f"{C.DIM}○{C.RESET}"
            vms.append((vmid, name, has_args))
            print(f"  {icon} VM {C.BOLD}{vmid}{C.RESET} — {name}")

    if not vms:
        warn("No VM configs found.")

    return vms
