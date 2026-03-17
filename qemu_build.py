"""
QEMU build helper: automates patching and building pve-qemu
from source with the anti-detection patch for PVE 9.1.x.
"""

import os

from utils import C, info, warn, error, step, header


# ============================================================================
#  PVE VERSION → GIT COMMIT MAPPING
# ============================================================================

PVE_COMMITS = {
    "8.0.2-3": "409db0cd7bdc833e4a09d39492b319426029aa92",
    "8.1.5-3": "d70533ff83b5298fe86733dd6f9341e6e20c01c0",
    "9.0":     None,   # user-provided
    "9.1":     None,   # user-provided
}


# ============================================================================
#  BUILD PIPELINE
# ============================================================================

def build_patched_qemu():
    """Guide and automate the QEMU build process for PVE 9.1.x."""
    header("Build Patched QEMU for PVE 9.1.x")

    print(f"""
  {C.YELLOW}This process will:{C.RESET}
    1. Clone the pve-qemu repository
    2. Apply the anti-detection patch
    3. Build a patched .deb package

  {C.RED}⚠ Run this on a Proxmox VE build VM, NOT your production system!{C.RESET}
  {C.RED}⚠ Requires: git, devscripts, build dependencies{C.RESET}
""")

    confirm = input(f"  {C.YELLOW}Continue? [y/N]: {C.RESET}").strip().lower()
    if confirm != 'y':
        warn("Build cancelled.")
        return

    print(f"\n  {C.CYAN}PVE Git Commit{C.RESET}")
    print(f"  Find your commit at: {C.BLUE}https://git.proxmox.com/?p=pve-qemu.git;a=summary{C.RESET}")

    commit = input(f"\n  Git commit hash (or 'latest'): ").strip()
    if not commit:
        error("Commit hash required.")
        return

    patch_dir = os.path.dirname(os.path.abspath(__file__))
    patch_9_path = os.path.join(patch_dir, "001-anti-detection-9.0.patch")

    if not os.path.exists(patch_9_path):
        error(f"Patch file not found: {patch_9_path}")
        error("Ensure 001-anti-detection-9.0.patch is in the same directory as this script.")
        return

    build_dir = "/root/pve-qemu-build"

    commands = [
        f"# Step 1: Prepare build directory",
        f"mkdir -p {build_dir}",
        f"cd {build_dir}",
        f"",
        f"# Step 2: Clone and reset pve-qemu",
        f"git clone git://git.proxmox.com/git/pve-qemu.git",
        f"cd pve-qemu",
    ]

    if commit != 'latest':
        commands.append(f"git reset --hard {commit}")

    commands += [
        f"",
        f"# Step 3: Install build dependencies",
        f"apt update",
        f"apt install -y devscripts",
        f"mk-build-deps --install",
        f"git submodule update",
        f"",
        f"# Step 4: Copy the anti-detection patch",
        f"cp {patch_9_path} qemu/001-anti-detection.patch",
        f"",
        f"# Step 5: Inject patch into debian/rules",
        f"# Find '# guest-agent is only required for guest systems'",
        f"# and add BEFORE it:",
        f"#   patch -p1 < 001-anti-detection.patch",
        f"",
        f"# Step 6: Build",
        f"make clean",
        f"make",
        f"",
        f"# Step 7: Install the result",
        f"# dpkg -i --force-all pve-qemu-kvm_*_amd64.deb",
    ]

    print(f"\n{C.BOLD}  Build Commands:{C.RESET}")
    print(f"  {C.DIM}{'─'*50}{C.RESET}")
    for cmd in commands:
        if cmd.startswith("#"):
            print(f"  {C.GREEN}{cmd}{C.RESET}")
        elif cmd == "":
            print()
        else:
            print(f"  {C.WHITE}{cmd}{C.RESET}")
    print(f"  {C.DIM}{'─'*50}{C.RESET}")

    auto = input(f"\n  {C.YELLOW}Execute automatically? [y/N]: {C.RESET}").strip().lower()
    if auto == 'y':
        script_content = "\n".join(
            c for c in commands if not c.startswith("#") and c.strip()
        )
        script_path = "/tmp/build_patched_qemu.sh"

        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\nset -e\n\n")
            f.write(script_content)

        os.chmod(script_path, 0o755)

        step("Injecting patch line into debian/rules...")

        rules_path = os.path.join(build_dir, "pve-qemu", "debian", "rules")
        if os.path.exists(rules_path):
            inject_patch_line(rules_path)

        info(f"Build script written to {script_path}")
        step("Run: bash /tmp/build_patched_qemu.sh")

        run = input(f"  {C.YELLOW}Run now? [y/N]: {C.RESET}").strip().lower()
        if run == 'y':
            os.system(f"bash {script_path}")
    else:
        info("Copy and run the commands above on your PVE build VM.")


def inject_patch_line(rules_path):
    """Inject the patch command into debian/rules before the configure line."""
    with open(rules_path, 'r') as f:
        content = f.read()

    target = "# guest-agent is only required for guest systems"
    inject = "\t# [Inject] Anti-detection patch\n\tpatch -p1 < 001-anti-detection.patch\n\n\t"

    if "001-anti-detection.patch" in content:
        info("Patch line already present in debian/rules")
        return

    if target in content:
        content = content.replace(target, inject + target)
        with open(rules_path, 'w') as f:
            f.write(content)
        info("Injected patch line into debian/rules")
    else:
        warn("Could not find target line in debian/rules. Manual injection needed.")


# ============================================================================
#  CUSTOM VENDOR PATCH GENERATOR
# ============================================================================

def generate_custom_patch(profile):
    """Generate a modified anti-detection patch with custom vendor strings."""
    header("Generate Custom Vendor Patch")

    patch_dir = os.path.dirname(os.path.abspath(__file__))
    source_patch = os.path.join(patch_dir, "001-anti-detection-9.0.patch")

    if not os.path.exists(source_patch):
        error(f"Source patch not found: {source_patch}")
        return None

    vendor_name = profile["manufacturer"].split()[0]
    if len(vendor_name) > 10:
        vendor_name = vendor_name[:10]

    step(f"Generating patch with vendor: {C.BOLD}{vendor_name}{C.RESET}")

    with open(source_patch, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace ASUS references only in + lines (new content), not - lines
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('+') and not line.startswith('+++'):
            line = line.replace('"ASUS ', f'"{vendor_name} ')
            line = line.replace('"ASUS"', f'"{vendor_name}"')
            line = line.replace("'ASUS", f"'{vendor_name}")
            line = line.replace('ASUS_', f'{vendor_name}_')
        new_lines.append(line)

    output_name = f"001-anti-detection-9.0-{vendor_name.lower()}.patch"
    output_path = os.path.join(patch_dir, output_name)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    info(f"Custom patch saved: {output_name}")
    info(f"Use this patch when building QEMU for {vendor_name} branding")
    return output_path
