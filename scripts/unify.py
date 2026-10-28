import re
from pathlib import Path

# Target uniform pin order for all SRAM cells
UNIFORM_PINS = ["vdd", "gnd", "wl", "bl", "blb", "q", "qb"]

def standardize_subckt(input_path: str, target_subckt_name: str) -> str:
    """
    Reads an extracted Magic SPICE file, locates the top-level .subckt line,
    and reorders its port list to match UNIFORM_PINS: (vdd gnd wl bl blb q qb).
    Leaves helper subcircuits (like PCell wrappers) untouched.
    """
    content = Path(input_path).read_text()
    
    # Match the specific top-level .subckt line
    pattern = rf"^(\.subckt\s+{re.escape(target_subckt_name)}\s+)(.+)$"
    
    def replacer(match):
        prefix = match.group(1)
        existing_pins = match.group(2).strip().split()
        # Verify all expected pins exist (case-insensitive check)
        lower_map = {p.lower(): p for p in existing_pins}
        missing = [p for p in UNIFORM_PINS if p not in lower_map]
        if missing:
            raise ValueError(f"Missing pins {missing} in {target_subckt_name} (found: {existing_pins})")
        ordered_actual_pins = [lower_map[p] for p in UNIFORM_PINS]
        print(f"[OK] Standardized '{target_subckt_name}':")
        print(f"     Old pins: {' '.join(existing_pins)}")
        print(f"     New pins: {' '.join(ordered_actual_pins)}")
        return prefix + " ".join(ordered_actual_pins)

    updated_content, count = re.subn(pattern, replacer, content, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"Could not find '.subckt {target_subckt_name}' in {input_path}")
    return updated_content

def main():
    # 1. Standardize both files and combine into one library file
    compact_clean = standardize_subckt("/home/tarran/github/DICD-Project/spice/para/sram_compact.spice", "sram_compact")
    pcell_clean   = standardize_subckt("/home/tarran/github/DICD-Project/spice/para/sram_p.spice", "sram_p")

    combined_netlist = (
        "* ==================================================================\n"
        "* Auto-Generated Uniform 6T SRAM Extracted Netlists\n"
        "* Standard Port Order: vdd gnd wl bl blb q qb\n"
        "* ==================================================================\n\n"
        f"{compact_clean.strip()}\n\n"
        f"{pcell_clean.strip()}\n"
    )
    Path("/home/tarran/github/DICD-Project/tb/sram_models_uniform.spice").write_text(combined_netlist)
    print("\n[SUCCESS] Wrote standardized cells to 'sram_models_uniform.spice'")

if __name__ == "__main__":
    main()