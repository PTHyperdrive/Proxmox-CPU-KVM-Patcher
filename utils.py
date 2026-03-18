"""
Utility functions: ANSI colors, terminal formatting, random generators.
"""

import random
import string


# ============================================================================
#  ANSI COLORS
# ============================================================================

class C:
    """ANSI color codes for terminal output."""
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"


# ============================================================================
#  LOGGING HELPERS
# ============================================================================

def info(msg):    print(f"  {C.GREEN}[✓]{C.RESET} {msg}")
def warn(msg):    print(f"  {C.YELLOW}[!]{C.RESET} {msg}")
def error(msg):   print(f"  {C.RED}[✗]{C.RESET} {msg}")
def step(msg):    print(f"  {C.CYAN}[→]{C.RESET} {msg}")

def header(msg):
    print(f"\n{C.BOLD}{C.MAGENTA}{'─'*60}\n  {msg}\n{'─'*60}{C.RESET}")


def banner():
    """Print the application banner."""
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════════╗
║         PVE-EMU-RealPC  Config File Manager                    ║
║        Proxmox VM → Physical Machine Emulation                 ║
╠══════════════════════════════════════════════════════════════════╣
║  Based on: AICodo/pve-emu-realpc                               ║
║  Format:   ACPI Tables  ·  SMBIOS  ·  CPU Flags                ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}
""")


# ============================================================================
#  RANDOM GENERATORS
# ============================================================================

def random_serial(length=20):
    """Generate a random alphanumeric serial (default 20-char for SATA disks)."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


def random_hex_serial(length=8):
    """Generate a random hex serial (for RAM DIMMs, e.g., DF1EC466)."""
    return "".join(random.choices("0123456789ABCDEF", k=length))


def random_mac(prefix="D8:FC:93"):
    """Generate a random MAC address with the recommended D8:FC:93 prefix."""
    suffix = ":".join(f"{random.randint(0,255):02X}" for _ in range(3))
    return f"{prefix}:{suffix}"


def random_uuid():
    """Generate a random UUID v4."""
    import uuid
    return str(uuid.uuid4())
