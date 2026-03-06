# Drude Model Resistivity Calculator

A Python tool for computing the **electrical resistivity of metallic elements** using the classical Drude free-electron model. Element data is cleanly separated into a JSON database, keeping physics logic and raw data independent.

$$\rho = \frac{m}{n e^2 \tau}$$

| Symbol | Quantity | Unit |
|--------|----------|------|
| $m$ | Electron mass | kg |
| $n$ | Conduction electron density | m⁻³ |
| $e$ | Electron charge | C |
| $\tau$ | Relaxation (collision) time | s |

---

## Project Structure

```
resistivity-calculator/
├── main.py          # Physics logic, CLI, and display
├── elements.json    # Element database (lattice constants, τ, z, structure)
└── README.md
```

> **Design principle:** Data and logic are intentionally separated. You can add, edit, or remove elements in `elements.json` without ever touching the physics code in `main.py`.

---

## Physics Background

### The Drude Model

The Drude model (1900) treats conduction electrons as a classical ideal gas of free particles that undergo random collisions with ion cores. Between collisions, electrons accelerate freely under an applied electric field. The average time between collisions is the **relaxation time** τ.

This leads directly to the resistivity formula:

$$\rho = \frac{m}{n e^2 \tau}$$

### Electron Density from Crystal Structure

The conduction electron density *n* is estimated from the crystal lattice:

$$n = \frac{z \times N_{\text{cell}}}{a^3}$$

where:
- *z* = number of conduction electrons contributed per atom
- *N_cell* = number of atoms per unit cell (depends on crystal structure)
- *a* = lattice parameter (in metres)

| Structure | Atoms/Cell | Examples |
|-----------|-----------|---------|
| FCC | 4 | Cu, Ag, Au, Al, Pt, Ni |
| BCC | 2 | Fe, W, Mo, Na, K, Li |
| HCP | 2 | Mg, Ti, Zn, Co, Zr |
| ORTH | 2 | Ga, U (orthorhombic approximation) |

### Limitations

The Drude model is a **first-order classical estimate**. It:
- Overestimates resistivity for some elements
- Ignores Fermi–Dirac statistics (corrected by the Sommerfeld model)
- Does not account for band structure, phonon scattering, or impurities
- Works best for simple monovalent metals (Cu, Ag, Au, Na, K)

For a quantum-corrected treatment, see the **Sommerfeld free-electron model** in Ashcroft & Mermin, Chapter 2.

---

## Installation

No external dependencies — uses only Python's standard library.

```bash
git clone https://github.com/PaulGlory/resistivity-calculator.git
cd resistivity-calculator
python main.py
```

Requires **Python 3.10+**.

---

## Usage

### Interactive mode

```bash
python main.py
```

```
==================================================
  Drude Model Resistivity Calculator
  Formula: ρ = m / (n · e² · τ)
==================================================

  Commands:
    <element name>       — calculate resistivity
    list                 — show all elements
    compare Cu, Ag, Au   — side-by-side table
    quit / exit          — exit program

  Enter element (or command): copper

  ------------------------------------------
  Element              : Copper
  Crystal structure    : FCC (4 atoms/cell)
  Lattice constant     : 3.61 Å
  Relaxation time (τ)  : 2.70e-14 s
  Valence electrons (z): 1
  Electron density (n) : 3.448e+28 m⁻³
  Resistivity (ρ)      : 1.197e-08 Ω·m
  ------------------------------------------
```

### Compare multiple elements

```bash
python main.py --compare copper,silver,gold,aluminum
```

```
  Element          Struct  a (Å)    τ (s)       z   n (m⁻³)       ρ (Ω·m)
  ─────────────────────────────────────────────────────────────────────────
  Copper           FCC     3.61     2.70e-14    1   3.448e+28     1.197e-08
  Silver           FCC     4.09     4.00e-14    1   2.346e+28     1.184e-08
  Gold             FCC     4.08     3.00e-14    1   2.357e+28     1.578e-08
  Aluminum         FCC     4.05     8.00e-15    3   6.824e+28     1.487e-08
```

### List all elements

```bash
python main.py --list
```

### Import as a module

```python
from main import load_database, calculate_resistivity, compare_elements

db = load_database("elements.json")

# Single calculation (returns a dict)
result = calculate_resistivity("platinum", db)
print(f"Platinum resistivity: {result['rho']:.3e} Ω·m")

# Suppress terminal output
result = calculate_resistivity("iron", db, verbose=False)

# Batch comparison
compare_elements(["iron", "nickel", "cobalt"], db)
```

---

## Element Database (`elements.json`)

The database contains **55 metallic elements** spanning:

| Group | Elements |
|-------|----------|
| Alkali metals | Li, Na, K, Rb, Cs |
| Alkaline earth | Be, Mg, Ca, Sr, Ba |
| Groups 3–7 | Sc, Y, La, Ti, Zr, Hf, V, Nb, Ta, Cr, Mo, W, Mn, Re |
| Groups 8–10 | Fe, Ru, Os, Co, Rh, Ir, Ni, Pd, Pt |
| Coinage metals | Cu, Ag, Au |
| Group 12 | Zn, Cd, Hg |
| Post-transition | Al, Ga, In, Tl, Sn, Pb |
| Lanthanides | Ce, Pr, Nd, Gd, Tb, Dy, Er, Yb, Lu |
| Actinides | Th, U |

### Adding a new element

Open `elements.json` and add an entry:

```json
"rhodium": {
    "a": 3.80,
    "tau": 1.5e-14,
    "z": 1,
    "atoms_per_cell": 4,
    "structure": "FCC"
}
```

No changes to `main.py` are required.

---

## Data Sources

- Lattice constants: Kittel, C. *Introduction to Solid State Physics*, 8th ed.
- Relaxation times: Ashcroft, N. W. & Mermin, N. D. *Solid State Physics*.
- Valence electrons: Standard solid-state physics references.

---

## License

MIT License — free to use, modify, and distribute with attribution.

---

## Author

**Paul Glory**  
B.Sc. Physics, University of Ibadan | Aspiring Computational Scientist | Python & Data Analysis

[GitHub](https://github.com/PaulGlory)
