"""
Utility functions: colors, terminal formatting, serial/MAC generators.
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
def header(msg):  print(f"\n{C.BOLD}{C.MAGENTA}{'─'*60}\n  {msg}\n{'─'*60}{C.RESET}")


def banner():
    """Print the application banner."""
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════════╗
║       Proxmox VE Anti-VM Detection Config Patcher              ║
║                     PVE 9.1.x Edition                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Based on: zhaodice/proxmox-ve-anti-detection                  ║
║  Patches: VM Config  ·  CPU Models  ·  QEMU Build              ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}
""")


# ============================================================================
#  GENERATORS
# ============================================================================

def random_serial(prefix="OEM", length=10):
    """Generate a random serial number."""
    chars = string.ascii_uppercase + string.digits
    return prefix + "-" + "".join(random.choices(chars, k=length))


def random_mac():
    """Generate a random MAC address (locally administered)."""
    mac = [0x02, random.randint(0, 255), random.randint(0, 255),
           random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    return ":".join(f"{b:02X}" for b in mac)
