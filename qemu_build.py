"""
QEMU install helper for AICodo/pve-emu-realpc pre-built debs.
"""

import os
from utils import C, info, warn, error, step, header

GITHUB_RELEASES = "https://github.com/AICodo/pve-emu-realpc/releases"
EDK2_RELEASES = "https://github.com/AICodo/pve-emu-realpc_edk2-firmware-ovmf/releases"


def install_helper():
    """Guide user through pve-emu-realpc deb installation."""
    header("Install Patched QEMU (pve-emu-realpc)")
    print(f"""
  {C.CYAN}Pre-built .deb packages — no compilation needed.{C.RESET}

  {C.BOLD}Required files (upload to /root/):{C.RESET}
    1. pve-qemu-kvm_10.x.x_amd64.deb
    2. pve-edk2-firmware-ovmf_x.x.deb
    3. ssdt.aml (or ssdt-battery.aml), ssdt-ec.aml, hpet.aml

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


def check_aml_files():
    """Check if required AML files exist on the system."""
    header("Check ACPI Table Files")
    files = {
        "/root/ssdt.aml":         "SSDT (no battery)",
        "/root/ssdt-battery.aml": "SSDT (battery variant)",
        "/root/ssdt-ec.aml":      "SSDT-EC",
        "/root/hpet.aml":         "HPET",
    }
    for path, desc in files.items():
        if os.path.exists(path):
            info(f"{desc}: {C.GREEN}{path}{C.RESET} ({os.path.getsize(path)}B)")
        else:
            warn(f"{desc}: {C.RED}NOT FOUND{C.RESET} ({path})")
