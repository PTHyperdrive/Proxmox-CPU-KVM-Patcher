"""
CPU model profile management for /etc/pve/virtual-guest/cpu-models.conf.
"""

import os

from utils import C, info, warn, error, step, header


# ============================================================================
#  TEMPLATE
# ============================================================================

CPU_MODEL_LINES_TEMPLATE = [
    "cpu-model: {profile_name}",
    "    flags +avx;+avx2",
    "    phys-bits host",
    "    hidden 0",
    "    hv-vendor-id {hv_vendor}",
    "    reported-model {cpu_model}",
]


# ============================================================================
#  PATCH / CREATE / MODIFY
# ============================================================================

def patch_cpu_models(cpu_models_directory):
    """Ensure cpu-models.conf exists with default Anti-Detect profile."""
    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')

    if not os.path.exists(cpu_models_directory):
        os.makedirs(cpu_models_directory, exist_ok=True)
        info(f"Created directory: {cpu_models_directory}")

    if not os.path.exists(file_path):
        step(f"Creating {file_path} with default Anti-Detect profile...")
        lines = [
            "cpu-model: Anti-Detect",
            "    flags +avx;+avx2",
            "    phys-bits host",
            "    hidden 0",
            "    hv-vendor-id GenuineIntel",
            "    reported-model Skylake-Client",
        ]
        with open(file_path, 'w') as f:
            f.write("\n".join(lines) + "\n")
        info(f"Created {file_path}")
    else:
        info(f"{file_path} already exists")


def create_cpu_model(cpu_models_directory, profile=None):
    """Create a new CPU model profile interactively."""
    header("Create CPU Model Profile")

    profile_name = input(f"  Profile name (e.g., MyAntiDetect): ").strip()
    if not profile_name:
        error("Profile name cannot be empty.")
        return

    default_hv = profile.get("hv_vendor_id", "GenuineIntel") if profile else "GenuineIntel"

    hv_vendor = input(f"  HV Vendor ID [{C.DIM}{default_hv}{C.RESET}]: ").strip()
    if not hv_vendor:
        hv_vendor = default_hv
    if len(hv_vendor) > 12:
        warn("HV Vendor ID truncated to 12 characters.")
        hv_vendor = hv_vendor[:12]

    cpu_model = input(f"  CPU Model [{C.DIM}Skylake-Client{C.RESET}]: ").strip() or "Skylake-Client"

    custom = []
    for line in CPU_MODEL_LINES_TEMPLATE:
        line = line.replace("{profile_name}", profile_name)
        line = line.replace("{hv_vendor}", hv_vendor)
        line = line.replace("{cpu_model}", cpu_model)
        custom.append(line)

    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')

    if not os.path.exists(cpu_models_directory):
        os.makedirs(cpu_models_directory, exist_ok=True)

    with open(file_path, 'a') as f:
        f.write("\n" + "\n".join(custom) + "\n")

    info(f"Added CPU model '{profile_name}' to cpu-models.conf")


def change_profile_vendor(cpu_models_directory):
    """Change the hv-vendor-id of an existing CPU profile."""
    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')
    if not os.path.exists(file_path):
        error("cpu-models.conf not found. Create one first.")
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    profiles = []
    current = None
    for line in lines:
        if "cpu-model:" in line:
            if current:
                profiles.append(current)
            current = {"name": line.split(":")[1].strip(), "lines": [], "hv_id": "?"}
        if current:
            if "hv-vendor-id" in line:
                parts = line.strip().split()
                current["hv_id"] = parts[1] if len(parts) > 1 else "?"
            current["lines"].append(line)
    if current:
        profiles.append(current)

    if not profiles:
        error("No CPU profiles found in cpu-models.conf.")
        return

    header("Existing CPU Profiles")
    for idx, p in enumerate(profiles, 1):
        print(f"  {C.CYAN}{idx}.{C.RESET} {C.BOLD}{p['name']}{C.RESET}  (hv-vendor-id: {p['hv_id']})")

    try:
        choice = int(input(f"\n  Select profile to modify [1-{len(profiles)}]: ").strip()) - 1
        if not (0 <= choice < len(profiles)):
            error("Invalid selection.")
            return
    except ValueError:
        error("Invalid input.")
        return

    new_hv = input(f"  New HV Vendor ID for '{profiles[choice]['name']}': ").strip()
    if not new_hv:
        error("Vendor ID cannot be empty.")
        return
    if len(new_hv) > 12:
        warn("Truncated to 12 characters.")
        new_hv = new_hv[:12]

    for i, line in enumerate(profiles[choice]['lines']):
        if "hv-vendor-id" in line:
            profiles[choice]['lines'][i] = f"    hv-vendor-id {new_hv}\n"

    with open(file_path, 'w') as f:
        for p in profiles:
            f.writelines(p['lines'])

    info(f"Updated hv-vendor-id to '{new_hv}' for profile '{profiles[choice]['name']}'")


def show_cpu_profiles(cpu_models_directory):
    """Display all CPU profiles from cpu-models.conf."""
    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')
    if not os.path.exists(file_path):
        error("cpu-models.conf not found.")
        return

    header("CPU Model Profiles")
    with open(file_path, 'r') as f:
        content = f.read()

    if content.strip():
        print(f"\n{C.DIM}{'─'*50}{C.RESET}")
        print(content)
        print(f"{C.DIM}{'─'*50}{C.RESET}")
    else:
        warn("File is empty.")
