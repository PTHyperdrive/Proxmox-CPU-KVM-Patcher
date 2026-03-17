"""
Vendor profile definitions and selection/customization logic.

Each profile contains manufacturer-accurate device strings for
SMBIOS, USB, HDA, and other hardware identifiers.
"""

from utils import C, info, warn, error, header


# ============================================================================
#  VENDOR PROFILES — Preset device string packages
# ============================================================================

VENDOR_PROFILES = {
    "ASUS": {
        "manufacturer":       "ASUS",
        "product":            "ROG STRIX Z690-A GAMING WIFI",
        "bios_vendor":        "American Megatrends Inc.",
        "bios_version":       "2103",
        "system_product":     "System Product Name",
        "system_version":     "System Version",
        "board_product":      "ROG STRIX Z690-A GAMING WIFI",
        "board_version":      "Rev 1.xx",
        "chassis_vendor":     "Default string",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "Kingston",
        "ram_part":           "KHX3200C16D4/16GX",
        "ram_speed":          3200,
        "cpu_socket":         "LGA1700",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "DEL",
        "monitor_name":       "DELL U2722D",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "ASUS",
    },
    "Gigabyte": {
        "manufacturer":       "Gigabyte Technology Co., Ltd.",
        "product":            "Z790 AORUS ELITE AX",
        "bios_vendor":        "American Megatrends International, LLC.",
        "bios_version":       "F8a",
        "system_product":     "Z790 AORUS ELITE AX",
        "system_version":     "Default string",
        "board_product":      "Z790 AORUS ELITE AX",
        "board_version":      "x.x",
        "chassis_vendor":     "Default string",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "Corsair",
        "ram_part":           "CMK32GX5M2B5600C36",
        "ram_speed":          5600,
        "cpu_socket":         "LGA1700",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "SAM",
        "monitor_name":       "Samsung Odyssey G5",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "GBT",
    },
    "MSI": {
        "manufacturer":       "Micro-Star International Co., Ltd.",
        "product":            "MAG B660 TOMAHAWK WIFI DDR4",
        "bios_vendor":        "American Megatrends International, LLC.",
        "bios_version":       "7D42vA7",
        "system_product":     "MS-7D42",
        "system_version":     "1.0",
        "board_product":      "MAG B660 TOMAHAWK WIFI DDR4 (MS-7D42)",
        "board_version":      "1.0",
        "chassis_vendor":     "Micro-Star International Co., Ltd.",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "G.Skill",
        "ram_part":           "F4-3200C16D-32GVK",
        "ram_speed":          3200,
        "cpu_socket":         "LGA1700",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "VSC",
        "monitor_name":       "ViewSonic VX2718-2KPC",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "MSI",
    },
    "ASRock": {
        "manufacturer":       "ASRock",
        "product":            "B660M Pro RS",
        "bios_vendor":        "American Megatrends International, LLC.",
        "bios_version":       "13.02",
        "system_product":     "B660M Pro RS",
        "system_version":     " ",
        "board_product":      "B660M Pro RS",
        "board_version":      " ",
        "chassis_vendor":     "Default string",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "Samsung",
        "ram_part":           "M378A2G43AB3-CWE",
        "ram_speed":          3200,
        "cpu_socket":         "LGA1700",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "BNQ",
        "monitor_name":       "BenQ EX2780Q",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "ASR",
    },
    "Dell": {
        "manufacturer":       "Dell Inc.",
        "product":            "OptiPlex 7090",
        "bios_vendor":        "Dell Inc.",
        "bios_version":       "1.14.0",
        "system_product":     "OptiPlex 7090",
        "system_version":     " ",
        "board_product":      "0CRF2K",
        "board_version":      "A00",
        "chassis_vendor":     "Dell Inc.",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "SK Hynix",
        "ram_part":           "HMA82GU6DJR8N-XN",
        "ram_speed":          3200,
        "cpu_socket":         "LGA1200",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "DEL",
        "monitor_name":       "DELL P2422H",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "DELL",
    },
    "HP": {
        "manufacturer":       "HP",
        "product":            "HP EliteDesk 800 G8 SFF",
        "bios_vendor":        "HP",
        "bios_version":       "S07 Ver. 02.05.01",
        "system_product":     "HP EliteDesk 800 G8 Small Form Factor PC",
        "system_version":     " ",
        "board_product":      "8877",
        "board_version":      "KBC Version 11.32.08",
        "chassis_vendor":     "HP",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "Micron",
        "ram_part":           "MTA8ATF2G64AZ-3G2F1",
        "ram_speed":          3200,
        "cpu_socket":         "LGA1200",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "HWP",
        "monitor_name":       "HP E24 G4",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "HP",
    },
    "Lenovo": {
        "manufacturer":       "LENOVO",
        "product":            "ThinkCentre M90q Gen 3",
        "bios_vendor":        "LENOVO",
        "bios_version":       "M4CKT39A",
        "system_product":     "11U1CTO1WW",
        "system_version":     "ThinkCentre M90q Gen 3",
        "board_product":      "330B",
        "board_version":      "SDK0T76461 WIN",
        "chassis_vendor":     "LENOVO",
        "chassis_type":       "Desktop",
        "ram_manufacturer":   "Samsung",
        "ram_part":           "M471A2K43EB1-CWE",
        "ram_speed":          3200,
        "cpu_socket":         "LGA1700",
        "hv_vendor_id":       "GenuineIntel",
        "monitor_vendor":     "LEN",
        "monitor_name":       "Lenovo T24i-30",
        "hda_vendor_id":      "0x8086",
        "serial_prefix":      "LNV",
    },
}


# ============================================================================
#  PROFILE SELECTION
# ============================================================================

def select_vendor_profile():
    """Let user choose a vendor preset or enter custom strings."""
    header("Select Device Vendor Profile")

    vendors = list(VENDOR_PROFILES.keys())
    for idx, name in enumerate(vendors, 1):
        p = VENDOR_PROFILES[name]
        print(f"  {C.CYAN}{idx}.{C.RESET} {C.BOLD}{name}{C.RESET}  ({p['product']})")

    print(f"  {C.YELLOW}{len(vendors)+1}.{C.RESET} {C.BOLD}Custom (enter manually){C.RESET}")
    print()

    while True:
        try:
            choice = int(input(f"  {C.CYAN}Select [1-{len(vendors)+1}]: {C.RESET}").strip())
            if 1 <= choice <= len(vendors):
                profile = VENDOR_PROFILES[vendors[choice - 1]].copy()
                info(f"Selected: {C.BOLD}{vendors[choice - 1]}{C.RESET}")

                customize = input(f"\n  {C.YELLOW}Customize individual fields? [y/N]: {C.RESET}").strip().lower()
                if customize == 'y':
                    profile = customize_profile(profile)

                return profile
            elif choice == len(vendors) + 1:
                return build_custom_profile()
            else:
                error("Invalid choice.")
        except ValueError:
            error("Please enter a number.")


def customize_profile(profile):
    """Let user override specific fields in a preset profile."""
    header("Customize Profile Fields (press Enter to keep default)")

    editable_fields = [
        ("manufacturer",     "Manufacturer"),
        ("product",          "Product Name"),
        ("bios_vendor",      "BIOS Vendor"),
        ("bios_version",     "BIOS Version"),
        ("board_product",    "Board Product"),
        ("ram_manufacturer", "RAM Manufacturer"),
        ("ram_part",         "RAM Part Number"),
        ("ram_speed",        "RAM Speed (MHz)"),
        ("cpu_socket",       "CPU Socket"),
        ("hv_vendor_id",     "HV Vendor ID (12 chars max)"),
        ("serial_prefix",    "Serial Prefix"),
    ]

    for key, label in editable_fields:
        current = profile[key]
        val = input(f"  {label} [{C.DIM}{current}{C.RESET}]: ").strip()
        if val:
            if key == "ram_speed":
                try:
                    profile[key] = int(val)
                except ValueError:
                    warn(f"Invalid number, keeping {current}")
            else:
                profile[key] = val

    return profile


def build_custom_profile():
    """Build a completely custom vendor profile from scratch."""
    header("Custom Vendor Profile — Enter All Fields")

    profile = {}
    fields = [
        ("manufacturer",     "Manufacturer",               "Custom OEM"),
        ("product",          "Product Name",                "Custom Motherboard"),
        ("bios_vendor",      "BIOS Vendor",                 "American Megatrends Inc."),
        ("bios_version",     "BIOS Version",                "1.0"),
        ("system_product",   "System Product",              "Custom System"),
        ("system_version",   "System Version",              "1.0"),
        ("board_product",    "Board Product",               "Custom Board"),
        ("board_version",    "Board Version",               "1.0"),
        ("chassis_vendor",   "Chassis Vendor",              "Default string"),
        ("chassis_type",     "Chassis Type",                "Desktop"),
        ("ram_manufacturer", "RAM Manufacturer",            "Kingston"),
        ("ram_part",         "RAM Part Number",             "KHX3200C16D4/16GX"),
        ("ram_speed",        "RAM Speed (MHz)",             "3200"),
        ("cpu_socket",       "CPU Socket",                  "LGA1700"),
        ("hv_vendor_id",     "HV Vendor ID (12 chars max)", "GenuineIntel"),
        ("monitor_vendor",   "Monitor Vendor (3-char)",     "DEL"),
        ("monitor_name",     "Monitor Name",                "DELL Monitor"),
        ("hda_vendor_id",    "HDA Vendor ID (hex)",         "0x8086"),
        ("serial_prefix",    "Serial Prefix",               "OEM"),
    ]

    for key, label, default in fields:
        val = input(f"  {label} [{C.DIM}{default}{C.RESET}]: ").strip()
        if key == "ram_speed":
            try:
                profile[key] = int(val) if val else int(default)
            except ValueError:
                profile[key] = int(default)
        else:
            profile[key] = val if val else default

    return profile
