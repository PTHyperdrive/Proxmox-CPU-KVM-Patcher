"""
Motherboard vendor profile definitions and selection/customization logic.

Each profile contains manufacturer-accurate SMBIOS strings for
types 0 (BIOS), 1 (System), 2 (Board), 3 (Chassis), 4 (CPU), 17 (RAM).
Designed to match the AICodo/pve-emu-realpc args format.
"""

from utils import C, info, warn, error, header


# ============================================================================
#  VENDOR PROFILES
# ============================================================================

VENDOR_PROFILES = {
    "Maxsun B760M (Intel 12th)": {
        "bios_vendor":      "American Megatrends International LLC.",
        "bios_version":     "H3.7G",
        "bios_date":        "02/21/2023",
        "bios_release":     "3.7",
        "sys_manufacturer": "Maxsun",
        "sys_product":      "MS-Terminator B760M",
        "sys_version":      "VER:H3.7G(2022/11/29)",
        "sys_serial":       "Default string",
        "sys_sku":          "Default string",
        "sys_family":       "Default string",
        "board_manufacturer": "Maxsun",
        "board_product":    "MS-Terminator B760M",
        "board_version":    "VER:H3.7G(2022/11/29)",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Default string",
        "chassis_version":  "Default string",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "12th Gen Intel(R) Core(TM) i7-12700",
        "cpu_socket":       "LGA1700",
        "cpu_max_speed":    4900,
        "cpu_cur_speed":    3800,
        "ram_manufacturer": "KINGSTON",
        "ram_speed":        3200,
        "ram_part":         "SED3200U1888S",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU FAN",            "external": "Not Specified"},
            {"internal": "J3C1 - GMCH FAN",    "external": "Not Specified"},
            {"internal": "J2F1 - LAI FAN",     "external": "Not Specified"},
        ],
    },
    "ASUS ROG Z690 (Intel 12th)": {
        "bios_vendor":      "American Megatrends Inc.",
        "bios_version":     "2103",
        "bios_date":        "05/12/2023",
        "bios_release":     "5.17",
        "sys_manufacturer": "ASUS",
        "sys_product":      "System Product Name",
        "sys_version":      "System Version",
        "sys_serial":       "Default string",
        "sys_sku":          "SKU",
        "sys_family":       "Default string",
        "board_manufacturer": "ASUSTeK COMPUTER INC.",
        "board_product":    "ROG STRIX Z690-A GAMING WIFI D4",
        "board_version":    "Rev 1.xx",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Default string",
        "chassis_version":  "Default string",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "12th Gen Intel(R) Core(TM) i9-12900K",
        "cpu_socket":       "LGA1700",
        "cpu_max_speed":    5200,
        "cpu_cur_speed":    4900,
        "ram_manufacturer": "Kingston",
        "ram_speed":        3200,
        "ram_part":         "KHX3200C16D4/16GX",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU FAN",     "external": "Not Specified"},
            {"internal": "CHA FAN",     "external": "Not Specified"},
        ],
    },
    "Gigabyte B660M (Intel 12th)": {
        "bios_vendor":      "American Megatrends International, LLC.",
        "bios_version":     "F6",
        "bios_date":        "08/30/2022",
        "bios_release":     "5.19",
        "sys_manufacturer": "Gigabyte Technology Co., Ltd.",
        "sys_product":      "B660M DS3H DDR4",
        "sys_version":      "Default string",
        "sys_serial":       "Default string",
        "sys_sku":          "Default string",
        "sys_family":       "Default string",
        "board_manufacturer": "Gigabyte Technology Co., Ltd.",
        "board_product":    "B660M DS3H DDR4",
        "board_version":    "x.x",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Default string",
        "chassis_version":  "Default string",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "12th Gen Intel(R) Core(TM) i5-12400",
        "cpu_socket":       "LGA1700",
        "cpu_max_speed":    4400,
        "cpu_cur_speed":    2500,
        "ram_manufacturer": "Corsair",
        "ram_speed":        3200,
        "ram_part":         "CMK16GX4M2E3200C16",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU_FAN",     "external": "Not Specified"},
            {"internal": "SYS_FAN1",    "external": "Not Specified"},
            {"internal": "SYS_FAN2",    "external": "Not Specified"},
        ],
    },
    "MSI B760M (Intel 13th)": {
        "bios_vendor":      "American Megatrends International, LLC.",
        "bios_version":     "7D42vA7",
        "bios_date":        "09/21/2023",
        "bios_release":     "5.19",
        "sys_manufacturer": "Micro-Star International Co., Ltd.",
        "sys_product":      "MS-7D42",
        "sys_version":      "1.0",
        "sys_serial":       "Default string",
        "sys_sku":          "Default string",
        "sys_family":       "Default string",
        "board_manufacturer": "Micro-Star International Co., Ltd.",
        "board_product":    "MAG B760M MORTAR WIFI DDR4 (MS-7D42)",
        "board_version":    "1.0",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Micro-Star International Co., Ltd.",
        "chassis_version":  "Default string",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "13th Gen Intel(R) Core(TM) i7-13700K",
        "cpu_socket":       "LGA1700",
        "cpu_max_speed":    5400,
        "cpu_cur_speed":    3400,
        "ram_manufacturer": "G.Skill",
        "ram_speed":        3200,
        "ram_part":         "F4-3200C16D-32GVK",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU_FAN1",    "external": "Not Specified"},
            {"internal": "PUMP_FAN1",   "external": "Not Specified"},
            {"internal": "SYS_FAN1",    "external": "Not Specified"},
        ],
    },
    "ASRock B660M (Intel 12th)": {
        "bios_vendor":      "American Megatrends International, LLC.",
        "bios_version":     "13.02",
        "bios_date":        "07/14/2023",
        "bios_release":     "5.19",
        "sys_manufacturer": "ASRock",
        "sys_product":      "B660M Pro RS",
        "sys_version":      " ",
        "sys_serial":       "Default string",
        "sys_sku":          "Default string",
        "sys_family":       "Default string",
        "board_manufacturer": "ASRock",
        "board_product":    "B660M Pro RS",
        "board_version":    " ",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Default string",
        "chassis_version":  "Default string",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "12th Gen Intel(R) Core(TM) i5-12400F",
        "cpu_socket":       "LGA1700",
        "cpu_max_speed":    4400,
        "cpu_cur_speed":    2500,
        "ram_manufacturer": "Samsung",
        "ram_speed":        3200,
        "ram_part":         "M378A2G43AB3-CWE",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU_FAN1",    "external": "Not Specified"},
            {"internal": "CHA_FAN1",    "external": "Not Specified"},
        ],
    },
    "Dell OptiPlex 7090 (Intel 11th)": {
        "bios_vendor":      "Dell Inc.",
        "bios_version":     "1.14.0",
        "bios_date":        "03/15/2023",
        "bios_release":     "1.14",
        "sys_manufacturer": "Dell Inc.",
        "sys_product":      "OptiPlex 7090",
        "sys_version":      " ",
        "sys_serial":       "Default string",
        "sys_sku":          "0991",
        "sys_family":       "OptiPlex",
        "board_manufacturer": "Dell Inc.",
        "board_product":    "0CRF2K",
        "board_version":    "A00",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Dell Inc.",
        "chassis_version":  " ",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "11th Gen Intel(R) Core(TM) i7-11700",
        "cpu_socket":       "LGA1200",
        "cpu_max_speed":    4900,
        "cpu_cur_speed":    2500,
        "ram_manufacturer": "SK Hynix",
        "ram_speed":        3200,
        "ram_part":         "HMA82GU6DJR8N-XN",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU FAN",     "external": "Not Specified"},
        ],
    },
    "HP EliteDesk 800 G8 (Intel 11th)": {
        "bios_vendor":      "HP",
        "bios_version":     "S07 Ver. 02.05.01",
        "bios_date":        "06/20/2023",
        "bios_release":     "2.5",
        "sys_manufacturer": "HP",
        "sys_product":      "HP EliteDesk 800 G8 Small Form Factor PC",
        "sys_version":      " ",
        "sys_serial":       "Default string",
        "sys_sku":          "Default string",
        "sys_family":       "103C_53307J HP EliteDesk",
        "board_manufacturer": "HP",
        "board_product":    "8877",
        "board_version":    "KBC Version 11.32.08",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "HP",
        "chassis_version":  " ",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version":      "11th Gen Intel(R) Core(TM) i7-11700",
        "cpu_socket":       "LGA1200",
        "cpu_max_speed":    4900,
        "cpu_cur_speed":    2500,
        "ram_manufacturer": "Micron",
        "ram_speed":        3200,
        "ram_part":         "MTA8ATF2G64AZ-3G2F1",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU FAN",     "external": "Not Specified"},
        ],
    },
    "AMD Ryzen B550M (Gigabyte)": {
        "bios_vendor":      "American Megatrends International, LLC.",
        "bios_version":     "F16e",
        "bios_date":        "12/01/2022",
        "bios_release":     "5.17",
        "sys_manufacturer": "Gigabyte Technology Co., Ltd.",
        "sys_product":      "B550M DS3H",
        "sys_version":      "Default string",
        "sys_serial":       "Default string",
        "sys_sku":          "Default string",
        "sys_family":       "Default string",
        "board_manufacturer": "Gigabyte Technology Co., Ltd.",
        "board_product":    "B550M DS3H",
        "board_version":    "x.x",
        "board_serial":     "Default string",
        "board_asset":      "Default string",
        "board_location":   "Default string",
        "chassis_manufacturer": "Default string",
        "chassis_version":  "Default string",
        "chassis_serial":   "Default string",
        "chassis_asset":    "Default string",
        "chassis_sku":      "Default string",
        "cpu_manufacturer": "Advanced Micro Devices, Inc.",
        "cpu_version":      "AMD Ryzen 7 5800X 8-Core Processor",
        "cpu_socket":       "AM4",
        "cpu_max_speed":    4850,
        "cpu_cur_speed":    3800,
        "ram_manufacturer": "Corsair",
        "ram_speed":        3600,
        "ram_part":         "CMK32GX4M2D3600C18",
        "ram_bank":         "BANK 0",
        "ram_loc_pfx":      "Controller0-ChannelA-DIMM",
        "ram_asset":        "9876543210",
        "port_entries": [
            {"internal": "CPU_FAN",     "external": "Not Specified"},
            {"internal": "SYS_FAN1",    "external": "Not Specified"},
        ],
    },
}


# ============================================================================
#  PROFILE SELECTION
# ============================================================================

def select_vendor_profile():
    """Let user choose a vendor preset or enter custom strings."""
    header("Select Motherboard / Vendor Profile")

    vendors = list(VENDOR_PROFILES.keys())
    for idx, name in enumerate(vendors, 1):
        p = VENDOR_PROFILES[name]
        print(f"  {C.CYAN}{idx:2d}.{C.RESET} {C.BOLD}{name}{C.RESET}")
        print(f"      {C.DIM}{p['board_manufacturer']} {p['board_product']}{C.RESET}")

    custom_n = len(vendors) + 1
    print(f"  {C.YELLOW}{custom_n:2d}.{C.RESET} {C.BOLD}Custom (enter manually){C.RESET}")
    print()

    while True:
        try:
            choice = int(input(f"  {C.CYAN}Select [1-{custom_n}]: {C.RESET}").strip())
            if 1 <= choice <= len(vendors):
                profile = VENDOR_PROFILES[vendors[choice - 1]].copy()
                # deep-copy port_entries list
                profile["port_entries"] = [e.copy() for e in profile["port_entries"]]
                info(f"Selected: {C.BOLD}{vendors[choice - 1]}{C.RESET}")

                customize = input(
                    f"\n  {C.YELLOW}Customize individual fields? [y/N]: {C.RESET}"
                ).strip().lower()
                if customize == 'y':
                    profile = customize_profile(profile)
                return profile

            elif choice == custom_n:
                return build_custom_profile()
            else:
                error("Invalid choice.")
        except ValueError:
            error("Please enter a number.")


# ============================================================================
#  CUSTOMIZATION
# ============================================================================

# Fields shown in the customize flow — (key, label, is_int)
_EDITABLE = [
    ("bios_vendor",          "BIOS Vendor",           False),
    ("bios_version",         "BIOS Version",          False),
    ("bios_date",            "BIOS Date (MM/DD/YYYY)",False),
    ("sys_manufacturer",     "System Manufacturer",   False),
    ("sys_product",          "System Product",        False),
    ("board_manufacturer",   "Board Manufacturer",    False),
    ("board_product",        "Board Product",         False),
    ("chassis_manufacturer", "Chassis Manufacturer",  False),
    ("cpu_manufacturer",     "CPU Manufacturer",      False),
    ("cpu_version",          "CPU Version String",    False),
    ("cpu_socket",           "CPU Socket",            False),
    ("cpu_max_speed",        "CPU Max Speed (MHz)",   True),
    ("cpu_cur_speed",        "CPU Current Speed (MHz)",True),
    ("ram_manufacturer",     "RAM Manufacturer",      False),
    ("ram_speed",            "RAM Speed (MHz)",       True),
    ("ram_part",             "RAM Part Number",       False),
]


def customize_profile(profile):
    """Let user override specific fields in a preset profile."""
    header("Customize Profile Fields  (Enter = keep default)")

    for key, label, is_int in _EDITABLE:
        current = profile.get(key, "")
        val = input(f"  {label} [{C.DIM}{current}{C.RESET}]: ").strip()
        if val:
            if is_int:
                try:
                    profile[key] = int(val)
                except ValueError:
                    warn(f"Invalid number, keeping {current}")
            else:
                profile[key] = val

    return profile


def build_custom_profile():
    """Build a completely custom profile from scratch."""
    header("Custom Profile — Enter All Fields  (Enter = use default)")

    defaults = VENDOR_PROFILES["Maxsun B760M (Intel 12th)"]
    profile = {}

    all_fields = [
        ("bios_vendor",          "BIOS Vendor",           False),
        ("bios_version",         "BIOS Version",          False),
        ("bios_date",            "BIOS Date (MM/DD/YYYY)",False),
        ("bios_release",         "BIOS Release",          False),
        ("sys_manufacturer",     "System Manufacturer",   False),
        ("sys_product",          "System Product",        False),
        ("sys_version",          "System Version",        False),
        ("sys_serial",           "System Serial",         False),
        ("sys_sku",              "System SKU",            False),
        ("sys_family",           "System Family",         False),
        ("board_manufacturer",   "Board Manufacturer",    False),
        ("board_product",        "Board Product",         False),
        ("board_version",        "Board Version",         False),
        ("board_serial",         "Board Serial",          False),
        ("board_asset",          "Board Asset Tag",       False),
        ("board_location",       "Board Location",        False),
        ("chassis_manufacturer", "Chassis Manufacturer",  False),
        ("chassis_version",      "Chassis Version",       False),
        ("chassis_serial",       "Chassis Serial",        False),
        ("chassis_asset",        "Chassis Asset Tag",     False),
        ("chassis_sku",          "Chassis SKU",           False),
        ("cpu_manufacturer",     "CPU Manufacturer",      False),
        ("cpu_version",          "CPU Version String",    False),
        ("cpu_socket",           "CPU Socket",            False),
        ("cpu_max_speed",        "CPU Max Speed (MHz)",   True),
        ("cpu_cur_speed",        "CPU Current Speed (MHz)",True),
        ("ram_manufacturer",     "RAM Manufacturer",      False),
        ("ram_speed",            "RAM Speed (MHz)",       True),
        ("ram_part",             "RAM Part Number",       False),
        ("ram_bank",             "RAM Bank",              False),
        ("ram_loc_pfx",          "RAM Locator Prefix",    False),
        ("ram_asset",            "RAM Asset Tag",         False),
    ]

    for key, label, is_int in all_fields:
        default = defaults.get(key, "Default string")
        val = input(f"  {label} [{C.DIM}{default}{C.RESET}]: ").strip()
        if is_int:
            try:
                profile[key] = int(val) if val else int(default)
            except ValueError:
                profile[key] = int(default)
        else:
            profile[key] = val if val else default

    # Port entries
    profile["port_entries"] = []
    print(f"\n  {C.CYAN}Port / Fan Connector Entries  (type 8){C.RESET}")
    print(f"  {C.DIM}Enter blank internal name to stop adding.{C.RESET}")
    idx = 1
    while True:
        internal = input(f"    Port {idx} internal name: ").strip()
        if not internal:
            break
        external = input(f"    Port {idx} external name [{C.DIM}Not Specified{C.RESET}]: ").strip()
        profile["port_entries"].append({
            "internal": internal,
            "external": external or "Not Specified",
        })
        idx += 1

    if not profile["port_entries"]:
        profile["port_entries"] = [{"internal": "CPU FAN", "external": "Not Specified"}]

    return profile
