#!/usr/bin/env python3
"""
Proxmox VE Anti-VM Detection Config Patcher (PVE 9.1.x)
========================================================
Based on: https://github.com/zhaodice/proxmox-ve-anti-detection

Entry point — imports from:
  utils.py            – colors, terminal helpers, generators
  vendor_profiles.py  – vendor presets + selection UI
  vm_config.py        – VM .conf file patching / restore
  cpu_models.py       – cpu-models.conf management
  qemu_build.py       – QEMU build pipeline + custom patch gen
  detection_info.py   – anti-detection coverage reference
"""

import sys

from utils            import C, info, warn, error, header, banner
from vendor_profiles  import select_vendor_profile
from vm_config        import patch_vm_config, restore_vm_config, show_vm_config, list_vms
from cpu_models       import patch_cpu_models, create_cpu_model, change_profile_vendor, show_cpu_profiles
from qemu_build       import install_helper, check_aml_files, deploy_aml_files
from detection_info   import show_detection_vectors

# ============================================================================
#  PATHS (change if your PVE layout differs)
# ============================================================================

CONF_DIR        = "/etc/pve/qemu-server/"
CPU_MODELS_DIR  = "/etc/pve/virtual-guest/"

# ============================================================================
#  MAIN MENU
# ============================================================================

def main_menu():
    """Main interactive menu loop."""
    current_profile = None

    banner()

    while True:
        # ── Menu ──────────────────────────────────────────────
        print(f"\n{C.BOLD}  ┌─ Main Menu {'─'*40}{C.RESET}")
        if current_profile:
            vendor = current_profile.get("manufacturer", "?").split()[0]
            print(f"  │  {C.DIM}Active profile: {C.CYAN}{vendor}{C.RESET}")
        else:
            print(f"  │  {C.DIM}No vendor profile selected{C.RESET}")

        print(f"  │")
        print(f"  │  {C.CYAN} 1.{C.RESET} Select Vendor Profile")
        print(f"  │  {C.GREEN} 2.{C.RESET} Patch All (VM Config + CPU Models)")
        print(f"  │  {C.GREEN} 3.{C.RESET} Patch Single VM Config")
        print(f"  │  {C.GREEN} 4.{C.RESET} Patch CPU Models")
        print(f"  │  {C.BLUE} 5.{C.RESET} Create CPU Model Profile")
        print(f"  │  {C.BLUE} 6.{C.RESET} Change Profile Vendor ID")
        print(f"  │  {C.BLUE} 7.{C.RESET} Show CPU Profiles")
        print(f"  │  {C.MAGENTA} 8.{C.RESET} List VMs")
        print(f"  │  {C.MAGENTA} 9.{C.RESET} Show VM Config")
        print(f"  │  {C.YELLOW}10.{C.RESET} Restore VM Config (Remove Patch)")
        print(f"  │  {C.GREEN}11.{C.RESET} Deploy AML Files to /root/")
        print(f"  │  {C.YELLOW}12.{C.RESET} Check AML Files")
        print(f"  │  {C.YELLOW}13.{C.RESET} Install Patched QEMU")
        print(f"  │  {C.DIM}14.{C.RESET} Show Detection Coverage Info")
        print(f"  │  {C.RED}15.{C.RESET} Exit")
        print(f"  └{'─'*52}")

        choice = input(f"\n  {C.CYAN}Choose [1-15]: {C.RESET}").strip()

        # ── 1  Select vendor ─────────────────────────────────
        if choice == '1':
            current_profile = select_vendor_profile()

        # ── 2  Patch all ─────────────────────────────────────
        elif choice == '2':
            if not current_profile:
                warn("Select a vendor profile first (option 1).")
                continue
            vmid = input("  Enter VM ID (e.g., 100): ").strip()
            if vmid:
                patch_vm_config(CONF_DIR, vmid, current_profile)
                patch_cpu_models(CPU_MODELS_DIR)

        # ── 3  Patch single VM ───────────────────────────────
        elif choice == '3':
            if not current_profile:
                warn("Select a vendor profile first (option 1).")
                continue
            header("Available VMs")
            list_vms(CONF_DIR)
            vmid = input(f"\n  Enter VM ID to patch: ").strip()
            if vmid:
                patch_vm_config(CONF_DIR, vmid, current_profile)

        # ── 4  Patch CPU models ──────────────────────────────
        elif choice == '4':
            patch_cpu_models(CPU_MODELS_DIR)

        # ── 5  Create CPU model ──────────────────────────────
        elif choice == '5':
            create_cpu_model(CPU_MODELS_DIR, current_profile)

        # ── 6  Change vendor ID ──────────────────────────────
        elif choice == '6':
            change_profile_vendor(CPU_MODELS_DIR)

        # ── 7  Show profiles ─────────────────────────────────
        elif choice == '7':
            show_cpu_profiles(CPU_MODELS_DIR)

        # ── 8  List VMs ──────────────────────────────────────
        elif choice == '8':
            header("VM List")
            list_vms(CONF_DIR)

        # ── 9  Show VM config ────────────────────────────────
        elif choice == '9':
            vmid = input("  Enter VM ID: ").strip()
            if vmid:
                show_vm_config(CONF_DIR, vmid)

        # ── 10 Restore VM config ─────────────────────────────
        elif choice == '10':
            vmid = input("  Enter VM ID to restore: ").strip()
            if vmid:
                restore_vm_config(CONF_DIR, vmid)

        # ── 11 Deploy AML files ──────────────────────────────
        elif choice == '11':
            deploy_aml_files()

        # ── 12 Check AML files ───────────────────────────────
        elif choice == '12':
            check_aml_files()

        # ── 13 Install patched QEMU ──────────────────────────
        elif choice == '13':
            install_helper()

        # ── 14 Detection info ────────────────────────────────
        elif choice == '14':
            show_detection_vectors()

        # ── 15 Exit ──────────────────────────────────────────
        elif choice == '15':
            print(f"\n  {C.CYAN}Goodbye!{C.RESET}\n")
            break

        else:
            error("Invalid option. Please try again.")


# ============================================================================
#  ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}Interrupted. Exiting.{C.RESET}\n")
        sys.exit(0)
