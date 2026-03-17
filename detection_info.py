"""
Reference information: displays what the anti-detection patch covers
and known remaining detection vectors.
"""

from utils import C, header


def show_detection_vectors():
    """Show what the anti-detection patch covers."""
    header("Anti-Detection Coverage (QEMU Patch)")

    table = [
        ("CPUID Signature",    "KVMKVMKVM → masked",         "✅"),
        ("Hyper-V Vendor",     "Microsoft Hv → GenuineIntel", "✅"),
        ("ACPI OEM IDs",       "BOCHS/BXPC → INTEL/PC8086",  "✅"),
        ("ACPI FADT Vendor",   "QEMU → Intel",               "✅"),
        ("SMBIOS Type 0",      "VM flag bit cleared",         "✅"),
        ("SMBIOS Type 3",      "Other → Desktop chassis",    "✅"),
        ("SMBIOS Type 4",      "Realistic CPU params",        "✅"),
        ("SMBIOS Type 7",      "CPU L1/L2/L3 cache added",   "✅"),
        ("SMBIOS Type 17",     "Realistic RAM parameters",    "✅"),
        ("SMBIOS Types 22-39", "Battery/Fan/Temp/PSU added",  "✅"),
        ("VMGENID ACPI",       "Table generation skipped",    "✅"),
        ("Device Strings",     "All QEMU → vendor name",     "✅"),
        ("USB Descriptors",    "QEMU → vendor name",          "✅"),
        ("IDE/SCSI/NVMe",      "QEMU → vendor name",          "✅"),
        ("HDA Audio Vendor",   "0x1af4 → 0x8086",            "✅"),
        ("EDID Monitor",       "RHT → DEL, realistic IDs",   "✅"),
        ("SPD EEPROM",         "Kingston DDR3 data",           "✅"),
        ("FW_CFG DMA Sig",     "QEMU CFG hex → ASUS CFG",    "✅"),
        ("Boot Splash",        "Custom splash image",          "✅"),
    ]

    print(f"\n  {'Detection Vector':<22} {'Mitigation':<32} {'Status'}")
    print(f"  {'─'*22} {'─'*32} {'─'*6}")
    for vector, mitigation, status in table:
        print(f"  {C.WHITE}{vector:<22}{C.RESET} {mitigation:<32} {status}")

    print(f"\n  {C.YELLOW}Note: Device strings in the QEMU source patch use the vendor name")
    print(f"  from the selected profile. The .conf args provide VM-level config.{C.RESET}")
    print(f"\n  {C.CYAN}Remaining detection vectors (no known solution):{C.RESET}")
    print(f"  • Win32_Fan, Win32_CacheMemory, Win32_VoltageProbe via WMI")
    print(f"  • CIM_Sensor, CIM_TemperatureSensor, CIM_VoltageSensor")
    print(f"  • RDTSC timing (requires host kernel patch)")
