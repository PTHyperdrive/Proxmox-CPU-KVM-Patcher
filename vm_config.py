"""
VM configuration patching for the AICodo/pve-emu-realpc config format.

Builds the full `args:` line with ACPI table injection, CPU flags,
and SMBIOS types. Patches/restores .conf files with backups.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

from utils import C, info, warn, error, step, header
from utils import random_serial, random_hex_serial, random_mac


# ============================================================================
#  ACPI TABLE PATHS (on the PVE host)
# ============================================================================

DEFAULT_ACPI_FILES = {
    "ssdt":    "/root/pve-emu-realpc/ssdt.aml",
    "ssdt_ec": "/root/pve-emu-realpc/ssdt-ec.aml",
    "hpet":    "/root/pve-emu-realpc/hpet.aml",
}

# Battery variant (for laptops / NVIDIA 43 error workaround)
ACPI_BATTERY_VARIANT = {
    "ssdt":    "/root/pve-emu-realpc/ssdt-battery.aml",
    "ssdt_ec": "/root/pve-emu-realpc/ssdt-ec.aml",
    "hpet":    "/root/pve-emu-realpc/hpet.aml",
}


# ============================================================================
#  QEMU VERSION FORMATS
# ============================================================================

def get_qemu_version_choice():
    """Ask user which QEMU version format to use."""
    print(f"\n  {C.CYAN}QEMU Version:{C.RESET}")
    print(f"  {C.GREEN}1.{C.RESET} QEMU 9 / 10  (recommended — compact args)")
    print(f"  {C.GREEN}2.{C.RESET} QEMU 7 / 8   (legacy — full SMBIOS in args)")
    
    while True:
        choice = input(f"  {C.CYAN}Select [1-2]: {C.RESET}").strip()
        if choice in ('1', '2'):
            return int(choice)
        error("Enter 1 or 2.")


# ============================================================================
#  BUILD ARGS LINE
# ============================================================================

def _esc(val):
    """Escape a value for QEMU args (wrap in double quotes if needed)."""
    s = str(val)
    if any(c in s for c in (' ', '(', ')')):
        return '"' + s + '"'
    return s


def build_args_line(profile, qemu_version=1, use_battery_ssdt=False):
    """
    Build the full `args:` line matching pve-emu-realpc format.
    
    qemu_version: 1 = QEMU 9/10 (compact), 2 = QEMU 7/8 (full)
    use_battery_ssdt: True = use ssdt-battery.aml (laptop/NVIDIA 43 fix)
    """
    acpi = ACPI_BATTERY_VARIANT if use_battery_ssdt else DEFAULT_ACPI_FILES
    
    ram_serial = random_hex_serial(8)

    # ── ACPI table injection ──
    acpi_args = []
    for name, path in acpi.items():
        acpi_args.append(f"-acpitable file={path}")
    acpi_str = " ".join(acpi_args)

    # ── CPU flags ──
    cpu_str = (
        "-cpu host,"
        "host-cache-info=on,"
        "hypervisor=off,"
        "vmware-cpuid-freq=false,"
        "enforce=false,"
        "host-phys-bits=true"
    )

    # ── SMBIOS type 0: BIOS ──
    t0 = (
        f"-smbios type=0,"
        f"vendor={_esc(profile['bios_vendor'])},"
        f"version={profile['bios_version']},"
        f"date='{profile['bios_date']}',"
        f"release={profile['bios_release']}"
    )

    # ── SMBIOS type 1: System ──
    t1 = (
        f"-smbios type=1,"
        f"manufacturer={_esc(profile['sys_manufacturer'])},"
        f"product={_esc(profile['sys_product'])},"
        f"version={_esc(profile['sys_version'])},"
        f"serial={_esc(profile['sys_serial'])},"
        f"sku={_esc(profile['sys_sku'])},"
        f"family={_esc(profile['sys_family'])}"
    )

    # ── SMBIOS type 2: Board ──
    t2 = (
        f"-smbios type=2,"
        f"manufacturer={_esc(profile['board_manufacturer'])},"
        f"product={_esc(profile['board_product'])},"
        f"version={_esc(profile['board_version'])},"
        f"serial={_esc(profile['board_serial'])},"
        f"asset={_esc(profile['board_asset'])},"
        f"location={_esc(profile['board_location'])}"
    )

    # ── SMBIOS type 3: Chassis ──
    t3 = (
        f"-smbios type=3,"
        f"manufacturer={_esc(profile['chassis_manufacturer'])},"
        f"version={_esc(profile['chassis_version'])},"
        f"serial={_esc(profile['chassis_serial'])},"
        f"asset={_esc(profile['chassis_asset'])},"
        f"sku={_esc(profile['chassis_sku'])}"
    )

    # ── SMBIOS type 4: Processor ──
    if qemu_version == 1:
        # QEMU 9/10: compact form (patch handles sock_pfx, speeds internally)
        t4 = (
            f"-smbios type=4,"
            f"manufacturer={_esc(profile['cpu_manufacturer'])},"
            f"version={_esc(profile['cpu_version'])}"
        )
    else:
        # QEMU 7/8: full form
        t4 = (
            f"-smbios type=4,"
            f"sock_pfx={_esc(profile['cpu_socket'])},"
            f"manufacturer={_esc(profile['cpu_manufacturer'])},"
            f"version={_esc(profile['cpu_version'])},"
            f"max-speed={profile['cpu_max_speed']},"
            f"current-speed={profile['cpu_cur_speed']},"
            f"serial={_esc('To Be Filled By O.E.M.')},"
            f"asset={_esc('To Be Filled By O.E.M.')},"
            f"part={_esc('To Be Filled By O.E.M.')}"
        )

    # ── SMBIOS type 17: Memory ──
    if qemu_version == 1:
        # QEMU 9/10: compact
        t17 = (
            f"-smbios type=17,"
            f"serial={ram_serial},"
            f"asset={_esc(profile['ram_asset'])}"
        )
    else:
        # QEMU 7/8: full
        t17 = (
            f"-smbios type=17,"
            f"loc_pfx={_esc(profile['ram_loc_pfx'])},"
            f"manufacturer={_esc(profile['ram_manufacturer'])},"
            f"speed={profile['ram_speed']},"
            f"serial={ram_serial},"
            f"part={_esc(profile['ram_part'])},"
            f"bank={_esc(profile['ram_bank'])},"
            f"asset={_esc(profile['ram_asset'])}"
        )

    # ── SMBIOS type 9: System Slots ──
    t9 = "-smbios type=9"

    # ── SMBIOS type 8: Port Connectors ──
    port_args = []
    for entry in profile.get("port_entries", []):
        if qemu_version == 1:
            port_args.append("-smbios type=8")
        else:
            port_args.append(
                f"-smbios type=8,"
                f"internal_reference={_esc(entry['internal'])},"
                f"external_reference={_esc(entry['external'])},"
                f"connector_type=0xFF,"
                f"port_type=0xFF"
            )

    # ── SMBIOS type 11: OEM Strings (QEMU 7/8 only) ──
    t11_str = ""
    if qemu_version == 2:
        t11_str = f' -smbios type=11,value={_esc("Default string")}'

    # ── Assemble ──
    parts = [acpi_str, cpu_str, t0, t1, t2, t3, t17, t4, t9]
    parts.extend(port_args)

    args = "args: " + " ".join(parts)
    if t11_str:
        args += t11_str

    return args


# ============================================================================
#  PATCH / RESTORE .conf
# ============================================================================

def patch_vm_config(conf_directory, vmid, profile, qemu_version=1, use_battery=False):
    """Patch a VM .conf file with anti-detection args."""
    file_path = os.path.join(conf_directory, f"{vmid}.conf")

    if not os.path.exists(file_path):
        error(f"VM config {vmid}.conf not found in {conf_directory}")
        return False

    with open(file_path, 'r') as f:
        lines = f.readlines()

    args_line = build_args_line(profile, qemu_version, use_battery)

    new_lines = []
    args_found = False
    balloon_found = False

    for line in lines:
        stripped = line.strip()

        # Replace existing args: line
        if stripped.startswith("args:"):
            new_lines.append(args_line + "\n")
            args_found = True
            continue

        # Force balloon off
        if stripped.startswith("balloon:"):
            new_lines.append("balloon: 0\n")
            balloon_found = True
            continue

        new_lines.append(line)

    if not args_found:
        new_lines.insert(0, args_line + "\n")

    if not balloon_found:
        new_lines.append("balloon: 0\n")

    # Backup
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_path = file_path + f".bak.{ts}"
    shutil.copy2(file_path, backup_path)
    info(f"Backup: {backup_path}")

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    info(f"Patched {vmid}.conf with pve-emu-realpc args")
    return True


def restore_vm_config(conf_directory, vmid):
    """Remove anti-detection args or restore from backup."""
    file_path = os.path.join(conf_directory, f"{vmid}.conf")

    if not os.path.exists(file_path):
        error(f"VM config {vmid}.conf not found")
        return False

    backups = sorted(Path(conf_directory).glob(f"{vmid}.conf.bak.*"), reverse=True)

    if backups:
        print(f"\n  {C.YELLOW}Available backups:{C.RESET}")
        for idx, bak in enumerate(backups[:5], 1):
            print(f"    {idx}. {bak.name}")

        choice = input(
            f"\n  Restore from backup [1-{min(5,len(backups))}], or 'n' to strip args: "
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= min(5, len(backups)):
            shutil.copy2(str(backups[int(choice)-1]), file_path)
            info(f"Restored from {backups[int(choice)-1].name}")
            return True

    # Strip args line
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = [l for l in lines if not l.strip().startswith("args:")]

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    info(f"Stripped args from {vmid}.conf")
    return True


# ============================================================================
#  DISPLAY HELPERS
# ============================================================================

def show_vm_config(conf_directory, vmid):
    """Display a VM config with color-coded lines."""
    file_path = os.path.join(conf_directory, f"{vmid}.conf")
    if not os.path.exists(file_path):
        error(f"VM config {vmid}.conf not found.")
        return

    header(f"VM {vmid} Configuration")
    with open(file_path, 'r') as f:
        for line in f:
            s = line.rstrip()
            if s.startswith("args:"):
                # Break long args into readable chunks
                print(f"  {C.GREEN}args:{C.RESET}")
                content = s[5:].strip()
                for part in content.split(" -"):
                    if part:
                        prefix = "  " if part.startswith("smbios") or part.startswith("cpu") or part.startswith("acpi") else "-"
                        print(f"    {C.GREEN}{prefix}{part}{C.RESET}")
            elif s.startswith("balloon:"):
                print(f"  {C.YELLOW}{s}{C.RESET}")
            elif s.startswith("cpu:"):
                print(f"  {C.CYAN}{s}{C.RESET}")
            elif s.startswith("smbios"):
                print(f"  {C.MAGENTA}{s}{C.RESET}")
            elif s.startswith("net"):
                print(f"  {C.BLUE}{s}{C.RESET}")
            else:
                print(f"  {s}")


def list_vms(conf_directory):
    """List all VMs in the config directory."""
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
            has_acpi = False
            with open(conf_path, 'r') as cf:
                for line in cf:
                    if line.strip().startswith("name:"):
                        name = line.split(":", 1)[1].strip()
                    if line.strip().startswith("args:"):
                        has_args = True
                        if "-acpitable" in line:
                            has_acpi = True

            if has_acpi:
                icon = f"{C.GREEN}✓ ACPI{C.RESET}"
            elif has_args:
                icon = f"{C.YELLOW}~ args{C.RESET}"
            else:
                icon = f"{C.DIM}○     {C.RESET}"

            vms.append((vmid, name, has_args))
            print(f"  {icon}  VM {C.BOLD}{vmid}{C.RESET} — {name}")

    if not vms:
        warn("No VM configs found.")

    return vms


def preview_args(profile, qemu_version=1, use_battery=False):
    """Preview the args line that would be generated without writing."""
    header("Preview Generated Args")

    args = build_args_line(profile, qemu_version, use_battery)

    print(f"\n  {C.DIM}{'─'*58}{C.RESET}")
    # Pretty-print by splitting on -smbios / -acpitable / -cpu
    segments = args.replace(" -smbios", "\n  -smbios") \
                   .replace(" -acpitable", "\n  -acpitable") \
                   .replace(" -cpu", "\n  -cpu")
    for line in segments.split("\n"):
        print(f"  {C.GREEN}{line.strip()}{C.RESET}")
    print(f"  {C.DIM}{'─'*58}{C.RESET}")
