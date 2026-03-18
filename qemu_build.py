"""
QEMU install helper & AML file deployment for AICodo/pve-emu-realpc.
"""

import os
import shutil
from pathlib import Path
from utils import C, info, warn, error, step, header

GITHUB_RELEASES = "https://github.com/AICodo/pve-emu-realpc/releases"
EDK2_RELEASES = "https://github.com/AICodo/pve-emu-realpc_edk2-firmware-ovmf/releases"

# ── Project-bundled AML directory (relative to this script) ──────────────
SCRIPT_DIR = Path(__file__).resolve().parent
AML_SOURCE_DIR = SCRIPT_DIR / "pve-emu-realpc"

# ── Target location on the PVE host ─────────────────────────────────────
AML_DEPLOY_DIR = Path("/root/pve-emu-realpc")

# Required AML files
AML_FILES = [
    "ssdt.aml",
    "ssdt-battery.aml",
    "ssdt-ec.aml",
    "hpet.aml",
]


def deploy_aml_files():
    """Copy AML files from the project's pve-emu-realpc/ dir to /root/."""
    header("Deploy ACPI Table Files")

    if not AML_SOURCE_DIR.exists():
        error(f"Source directory not found: {AML_SOURCE_DIR}")
        print(f"\n  {C.YELLOW}Create the directory and place AML files there:{C.RESET}")
        print(f"  mkdir -p {AML_SOURCE_DIR}")
        print(f"  {C.DIM}Download from: {GITHUB_RELEASES}{C.RESET}")
        return False

    # Check which files are available
    available = []
    missing = []
    for name in AML_FILES:
        src = AML_SOURCE_DIR / name
        if src.exists():
            available.append((name, src))
        else:
            missing.append(name)

    if not available:
        error("No AML files found in pve-emu-realpc/ directory.")
        print(f"\n  {C.YELLOW}Expected files:{C.RESET}")
        for name in AML_FILES:
            print(f"    - {name}")
        print(f"\n  {C.DIM}Download from: {GITHUB_RELEASES}{C.RESET}")
        return False

    if missing:
        warn(f"Missing optional files: {', '.join(missing)}")

    # Deploy
    deployed = 0
    for name, src in available:
        dst = AML_DEPLOY_DIR / name
        try:
            shutil.copy2(str(src), str(dst))
            info(f"Deployed: {src.name} → {dst}  ({src.stat().st_size}B)")
            deployed += 1
        except PermissionError:
            error(f"Permission denied copying {name} to {dst}  (run as root?)")
        except Exception as e:
            error(f"Failed to copy {name}: {e}")

    if deployed:
        info(f"{C.GREEN}{deployed} AML file(s) deployed to {AML_DEPLOY_DIR}{C.RESET}")
    return deployed > 0


def check_aml_files():
    """Check AML files in both the project dir and the deploy target."""
    header("Check ACPI Table Files")

    # ── Project source ──
    print(f"\n  {C.BOLD}Project source ({AML_SOURCE_DIR}):{C.RESET}")
    source_ok = 0
    for name in AML_FILES:
        src = AML_SOURCE_DIR / name
        if src.exists():
            info(f"  {name}: {C.GREEN}FOUND{C.RESET} ({src.stat().st_size}B)")
            source_ok += 1
        else:
            warn(f"  {name}: {C.RED}NOT FOUND{C.RESET}")

    # ── Deploy target ──
    print(f"\n  {C.BOLD}Deploy target ({AML_DEPLOY_DIR}):{C.RESET}")
    target_ok = 0
    for name in AML_FILES:
        dst = AML_DEPLOY_DIR / name
        if dst.exists():
            info(f"  {name}: {C.GREEN}FOUND{C.RESET} ({dst.stat().st_size}B)")
            target_ok += 1
        else:
            warn(f"  {name}: {C.RED}NOT FOUND{C.RESET}")

    # ── Summary ──
    print()
    if target_ok == 0 and source_ok > 0:
        warn(f"AML files exist in project but not deployed to {AML_DEPLOY_DIR}")
        print(f"  {C.CYAN}Use menu option 11 to deploy them.{C.RESET}")
    elif target_ok == 0 and source_ok == 0:
        error("No AML files found anywhere!")
        print(f"  {C.YELLOW}Download from: {GITHUB_RELEASES}{C.RESET}")
        print(f"  {C.YELLOW}Place into:    {AML_SOURCE_DIR}/{C.RESET}")


def install_helper():
    """Guide user through pve-emu-realpc deb installation."""
    header("Install Patched QEMU (pve-emu-realpc)")
    print(f"""
  {C.CYAN}Pre-built .deb packages — no compilation needed.{C.RESET}

  {C.BOLD}Required files (upload to /root/):{C.RESET}
    1. pve-qemu-kvm_10.x.x_amd64.deb
    2. pve-edk2-firmware-ovmf_x.x.deb
    3. AML files (auto-deployed from pve-emu-realpc/ via menu)

  {C.BLUE}Downloads:{C.RESET}
    {GITHUB_RELEASES}
    {EDK2_RELEASES}

  {C.BOLD}Commands:{C.RESET}
    $ dpkg -l | grep pve-qemu-kvm          # check version
    $ apt update && apt install pve-qemu-kvm
    $ dpkg -i pve-qemu-kvm_10.x.x_amd64.deb
    $ dpkg -i pve-edk2-firmware-ovmf_x.x.deb

  {C.YELLOW}Restore official:{C.RESET}  apt reinstall pve-qemu-kvm
""")
