# Sudoku SAT Solver

### This is a Course (CS228) project under Prof. S. Krishna.
A powerful Sudoku solver that uses **Boolean Satisfiability (SAT)** to solve any valid 9×9 Sudoku puzzle. This implementation encodes Sudoku rules as a CNF (Conjunctive Normal Form) formula and uses the PySAT library with the Glucose solver.

## How It Works

The solver encodes Sudoku rules as boolean clauses:

1. **Each cell contains exactly one value** (1-9)
2. **Each row contains each digit exactly once**
3. **Each column contains each digit exactly once**
4. **Each 3×3 box contains each digit exactly once**
5. **Given clues are fixed**

These constraints are converted into CNF format and solved using a SAT solver.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install python-sat
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Interactive Input

Run the program and enter your puzzle row by row:

```bash
python sudoku_solver.py
```

You'll be prompted to enter 9 rows. Use:
- Numbers `1-9` for given clues
- `0` or `.` for empty cells

**Example input:**
```
Row 1: 5 3 0 0 7 0 0 0 0
Row 2: 6 0 0 1 9 5 0 0 0
Row 3: 0 9 8 0 0 0 0 6 0
...
```

### Method 2: Example Puzzle

Run with the built-in example:

```bash
python sudoku_solver.py --example
```

### Sample Output

```
==================================================
         SUDOKU SOLVER (SAT-based)
==================================================

INPUT PUZZLE:
=====================================
 5  3  .  |  .  7  .  |  .  .  . 
 6  .  .  |  1  9  5  |  .  .  . 
 .  9  8  |  .  .  .  |  .  6  . 
-------------------------------------
 8  .  .  |  .  6  .  |  .  .  3 
 4  .  .  |  8  .  3  |  .  .  1 
 7  .  .  |  .  2  .  |  .  .  6 
-------------------------------------
 .  6  .  |  .  .  .  |  2  8  . 
 .  .  .  |  4  1  9  |  .  .  5 
 .  .  .  |  .  8  .  |  .  7  9 

Solving... ✓ SOLVED!

SOLUTION:
=====================================
 5  3  4  |  6  7  8  |  9  1  2 
 6  7  2  |  1  9  5  |  3  4  8 
 1  9  8  |  3  4  2  |  5  6  7 
-------------------------------------
 8  5  9  |  7  6  1  |  4  2  3 
 4  2  6  |  8  5  3  |  7  9  1 
 7  1  3  |  9  2  4  |  8  5  6 
-------------------------------------
 9  6  1  |  5  3  7  |  2  8  4 
 2  8  7  |  4  1  9  |  6  3  5 
 3  4  5  |  2  8  6  |  1  7  9 

✓ Puzzle solved successfully!
```

## Project Structure

```
sudoku-sat-solver/
├── sudoku_solver.py       # Main solver implementation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Algorithm Details

### Variable Encoding

Each boolean variable represents: **"Cell (r, c) contains value v"**

Variables are encoded as integers:
```
var(r, c, v) = r × 81 + c × 9 + v + 1
```
where r, c, v ∈ {0, 1, ..., 8}

### CNF Clauses

The solver generates approximately 11,000 clauses encoding:
- Cell constraints: ~1,500 clauses
- Row constraints: ~2,900 clauses  
- Column constraints: ~2,900 clauses
- Box constraints: ~2,900 clauses
- Given clues: variable (depends on puzzle)


## License

This project is open source and available under the MIT License.

## References

- [PySAT Documentation](https://pysathq.github.io/)
- [SAT Solving](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)
- [Sudoku as SAT](https://baldur.iti.kit.edu/sat/files/2018/l02.pdf)

## Author

Created with ❤️ using SAT solving techniques

---

**Star this repo if you find it useful!** ⭐
