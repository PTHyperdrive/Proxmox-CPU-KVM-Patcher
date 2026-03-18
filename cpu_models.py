"""
CPU model profile management for /etc/pve/virtual-guest/cpu-models.conf.
"""

import os
from utils import C, info, warn, error, step, header


CPU_MODEL_TEMPLATE = [
    "cpu-model: {name}",
    "    flags +avx;+avx2",
    "    phys-bits host",
    "    hidden 0",
    "    hv-vendor-id {hv_vendor}",
    "    reported-model {model}",
]


def patch_cpu_models(cpu_models_directory):
    """Ensure cpu-models.conf exists with default profile."""
    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')

    if not os.path.exists(cpu_models_directory):
        os.makedirs(cpu_models_directory, exist_ok=True)
        info(f"Created directory: {cpu_models_directory}")

    if not os.path.exists(file_path):
        step(f"Creating {file_path}...")
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
    """Create a new CPU model profile."""
    header("Create CPU Model Profile")

    name = input("  Profile name (e.g., MyAntiDetect): ").strip()
    if not name:
        error("Name cannot be empty.")
        return

    default_hv = "GenuineIntel"
    hv = input(f"  HV Vendor ID [{C.DIM}{default_hv}{C.RESET}]: ").strip() or default_hv
    if len(hv) > 12:
        warn("Truncated to 12 chars.")
        hv = hv[:12]

    model = input(f"  CPU Model [{C.DIM}Skylake-Client{C.RESET}]: ").strip() or "Skylake-Client"

    lines = []
    for tmpl in CPU_MODEL_TEMPLATE:
        lines.append(
            tmpl.replace("{name}", name)
                .replace("{hv_vendor}", hv)
                .replace("{model}", model)
        )

    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')
    os.makedirs(cpu_models_directory, exist_ok=True)

    with open(file_path, 'a') as f:
        f.write("\n" + "\n".join(lines) + "\n")

    info(f"Added CPU model '{name}'")


def change_profile_vendor(cpu_models_directory):
    """Change hv-vendor-id of an existing profile."""
    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')
    if not os.path.exists(file_path):
        error("cpu-models.conf not found.")
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    profiles = []
    cur = None
    for line in lines:
        if "cpu-model:" in line:
            if cur:
                profiles.append(cur)
            cur = {"name": line.split(":")[1].strip(), "lines": [], "hv": "?"}
        if cur:
            if "hv-vendor-id" in line:
                parts = line.strip().split()
                cur["hv"] = parts[1] if len(parts) > 1 else "?"
            cur["lines"].append(line)
    if cur:
        profiles.append(cur)

    if not profiles:
        error("No profiles found.")
        return

    header("CPU Profiles")
    for idx, p in enumerate(profiles, 1):
        print(f"  {C.CYAN}{idx}.{C.RESET} {C.BOLD}{p['name']}{C.RESET}  (hv: {p['hv']})")

    try:
        choice = int(input(f"\n  Select [1-{len(profiles)}]: ").strip()) - 1
        if not (0 <= choice < len(profiles)):
            error("Invalid.")
            return
    except ValueError:
        error("Invalid.")
        return

    new_hv = input(f"  New HV Vendor ID: ").strip()
    if not new_hv:
        return
    if len(new_hv) > 12:
        new_hv = new_hv[:12]

    for i, line in enumerate(profiles[choice]['lines']):
        if "hv-vendor-id" in line:
            profiles[choice]['lines'][i] = f"    hv-vendor-id {new_hv}\n"

    with open(file_path, 'w') as f:
        for p in profiles:
            f.writelines(p['lines'])

    info(f"Updated to '{new_hv}'")


def show_cpu_profiles(cpu_models_directory):
    """Display all CPU profiles."""
    file_path = os.path.join(cpu_models_directory, 'cpu-models.conf')
    if not os.path.exists(file_path):
        error("cpu-models.conf not found.")
        return

    header("CPU Model Profiles")
    with open(file_path, 'r') as f:
        print(f.read())
