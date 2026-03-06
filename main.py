"""
main.py — Drude Model Electrical Resistivity Calculator
=========================================================
Calculates electrical resistivity using the Drude free-electron model:

    rho = m / (n * e^2 * tau)

    m   = electron mass (kg)
    n   = conduction electron density (m^-3), derived from crystal structure
    e   = electron charge (C)
    tau = relaxation time (s)

Element data is loaded from elements.json (same directory).

Usage:
    python main.py                   # interactive mode
    python main.py --list            # list all elements in database
    python main.py --compare Cu,Ag,Au  # compare multiple elements

Author: Paul Glory
"""

import json
import os
import sys

# ── Physical Constants ─────────────────────────────────────────────────────────
ELECTRON_CHARGE = 1.602e-19   # C
ELECTRON_MASS   = 9.109e-31   # kg


# ── Database Loader ────────────────────────────────────────────────────────────

def load_database(filepath="elements.json"):
    """
    Load the element database from a JSON file.

    Parameters
    ----------
    filepath : str
        Path to the JSON database file.

    Returns
    -------
    dict or None
        Parsed element data, or None if the file is missing or malformed.
    """
    if not os.path.exists(filepath):
        print(f"[Error] Database file '{filepath}' not found.")
        print("        Make sure elements.json is in the same folder as main.py.")
        return None

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        print(f"[Error] Could not parse '{filepath}': {exc}")
        return None


# ── Core Physics ───────────────────────────────────────────────────────────────

def calculate_resistivity(element_name, elements_db, verbose=True):
    """
    Calculate Drude resistivity for a given element.

    Parameters
    ----------
    element_name : str
        Element name (case-insensitive).
    elements_db : dict
        Loaded element database.
    verbose : bool
        Print formatted output if True.

    Returns
    -------
    dict with result fields, or None if element is not found.
    """
    key = element_name.strip().lower()

    if key not in elements_db:
        print(f"\n  [!] '{element_name}' not found in database.")
        print(f"      Type 'list' to see all {len(elements_db)} available elements.")
        return None

    data          = elements_db[key]
    a_m           = data["a"] * 1e-10          # Å → metres
    tau           = data["tau"]
    z             = data["z"]
    atoms_per_cell= data["atoms_per_cell"]
    structure     = data.get("structure", "N/A")

    # Electron number density: n = (z * atoms_per_cell) / a^3
    n   = (z * atoms_per_cell) / (a_m ** 3)

    # Drude model: rho = m / (n * e^2 * tau)
    rho = ELECTRON_MASS / (n * ELECTRON_CHARGE**2 * tau)

    result = {
        "element":        key.capitalize(),
        "structure":      structure,
        "a_angstrom":     data["a"],
        "tau":            tau,
        "z":              z,
        "atoms_per_cell": atoms_per_cell,
        "n":              n,
        "rho":            rho,
    }

    if verbose:
        _print_single(result)

    return result


def _print_single(r):
    """Print a formatted single-element result block."""
    bar = "-" * 42
    print(f"\n  {bar}")
    print(f"  Element              : {r['element']}")
    print(f"  Crystal structure    : {r['structure']} ({r['atoms_per_cell']} atoms/cell)")
    print(f"  Lattice constant     : {r['a_angstrom']} Å")
    print(f"  Relaxation time (τ)  : {r['tau']:.2e} s")
    print(f"  Valence electrons (z): {r['z']}")
    print(f"  Electron density (n) : {r['n']:.3e} m⁻³")
    print(f"  Resistivity (ρ)      : {r['rho']:.3e} Ω·m")
    print(f"  {bar}")


# ── Utility Commands ───────────────────────────────────────────────────────────

def list_elements(elements_db):
    """Print all elements in the database, 5 per row."""
    keys = sorted(elements_db.keys())
    print(f"\n  Database: {len(keys)} elements\n")
    for i in range(0, len(keys), 5):
        print("  " + "  ".join(f"{k.capitalize():<16}" for k in keys[i:i+5]))
    print()


def compare_elements(names, elements_db):
    """Print a side-by-side comparison table."""
    header = (f"  {'Element':<16} {'Struct':<6} {'a (Å)':<8} "
              f"{'τ (s)':<11} {'z':<3} {'n (m⁻³)':<13} {'ρ (Ω·m)'}")
    print(f"\n{header}")
    print("  " + "─" * (len(header) - 2))

    for name in names:
        key = name.strip().lower()
        if key not in elements_db:
            print(f"  {name.capitalize():<16} [not in database]")
            continue
        r = calculate_resistivity(key, elements_db, verbose=False)
        print(f"  {r['element']:<16} {r['structure']:<6} {r['a_angstrom']:<8} "
              f"{r['tau']:<11.2e} {r['z']:<3} {r['n']:<13.3e} {r['rho']:.3e}")
    print()


# ── Entry Point ────────────────────────────────────────────────────────────────

def print_banner():
    print("=" * 50)
    print("  Drude Model Resistivity Calculator")
    print("  Formula: ρ = m / (n · e² · τ)")
    print("=" * 50)


def interactive_mode(elements_db):
    """Run the interactive REPL loop."""
    print("\n  Commands:")
    print("    <element name>       — calculate resistivity")
    print("    list                 — show all elements")
    print("    compare Cu, Ag, Au   — side-by-side table")
    print("    quit / exit          — exit program\n")

    while True:
        user_input = input("  Enter element (or command): ").strip()

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ("quit", "exit", "q"):
            print("  Goodbye.\n")
            break
        elif cmd == "list":
            list_elements(elements_db)
        elif cmd.startswith("compare"):
            # Allow "compare Cu, Ag" or just "Cu, Ag" after typing 'compare' prompt
            rest = user_input[len("compare"):].strip().lstrip(":").strip()
            if not rest:
                rest = input("  Enter comma-separated elements: ").strip()
            names = [n.strip() for n in rest.split(",") if n.strip()]
            compare_elements(names, elements_db)
        else:
            calculate_resistivity(user_input, elements_db)


def main():
    print_banner()

    # ── CLI flag support ───────────────────────────────────────────────────────
    args = sys.argv[1:]

    elements_db = load_database()
    if not elements_db:
        sys.exit(1)

    if "--list" in args:
        list_elements(elements_db)

    elif "--compare" in args:
        idx = args.index("--compare")
        if idx + 1 >= len(args):
            print("[Error] --compare requires a comma-separated list of elements.")
            print("  Example: python main.py --compare copper,silver,gold")
            sys.exit(1)
        names = [n.strip() for n in args[idx + 1].split(",") if n.strip()]
        compare_elements(names, elements_db)

    else:
        interactive_mode(elements_db)


if __name__ == "__main__":
    main()
