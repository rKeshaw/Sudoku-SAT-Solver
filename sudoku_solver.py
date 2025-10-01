"""
sudoku_solver.py

A Sudoku solver using SAT (Boolean Satisfiability) with PySAT library.
Solves any valid 9x9 Sudoku puzzle by encoding it as a CNF formula.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List, Optional
import sys


def solve_sudoku(grid: List[List[int]]) -> Optional[List[List[int]]]:
    """
    Solves a Sudoku puzzle using a SAT solver.
    
    Args:
        grid: 9x9 2D list with integers 1-9 (given clues) and 0 (empty cells)
    
    Returns:
        Solved 9x9 grid, or None if no solution exists
    """
    
    # Variable encoding: var(r, c, v) represents "cell (r,c) contains value v"
    # Map to unique integer: (r * 81) + (c * 9) + v + 1
    # where r, c, v are 0-indexed (0-8)
    def var(r, c, v):
        return r * 81 + c * 9 + v + 1
    
    cnf = CNF()
    
    # Rule 1: Each cell contains at least one value
    for r in range(9):
        for c in range(9):
            cnf.append([var(r, c, v) for v in range(9)])
    
    # Rule 2: Each cell contains at most one value
    for r in range(9):
        for c in range(9):
            for v1 in range(9):
                for v2 in range(v1 + 1, 9):
                    cnf.append([-var(r, c, v1), -var(r, c, v2)])
    
    # Rule 3: Each row contains each value exactly once
    for r in range(9):
        for v in range(9):
            cnf.append([var(r, c, v) for c in range(9)])
            for c1 in range(9):
                for c2 in range(c1 + 1, 9):
                    cnf.append([-var(r, c1, v), -var(r, c2, v)])
    
    # Rule 4: Each column contains each value exactly once
    for c in range(9):
        for v in range(9):
            cnf.append([var(r, c, v) for r in range(9)])
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    cnf.append([-var(r1, c, v), -var(r2, c, v)])
    
    # Rule 5: Each 3x3 box contains each value exactly once
    for box_r in range(3):
        for box_c in range(3):
            for v in range(9):
                cells = []
                for r in range(box_r * 3, box_r * 3 + 3):
                    for c in range(box_c * 3, box_c * 3 + 3):
                        cells.append(var(r, c, v))
                cnf.append(cells)
                
                for i in range(len(cells)):
                    for j in range(i + 1, len(cells)):
                        cnf.append([-cells[i], -cells[j]])
    
    # Rule 6: Add constraints for the given clues
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                v = grid[r][c] - 1
                cnf.append([var(r, c, v)])
    
    # Solve using SAT solver
    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        
        if solver.solve():
            model = solver.get_model()
            
            # Decode solution
            solution = [[0] * 9 for _ in range(9)]
            for lit in model:
                if lit > 0:
                    lit -= 1
                    r = lit // 81
                    c = (lit % 81) // 9
                    v = lit % 9
                    solution[r][c] = v + 1
            
            return solution
        else:
            return None


def print_grid(grid: List[List[int]], title: str = ""):
    """Pretty print a Sudoku grid."""
    if title:
        print(f"\n{title}")
        print("=" * 37)
    
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("-" * 37)
        
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            row_str += f" {num if num != 0 else '.'} "
        
        print(row_str)
    print()


def parse_input() -> List[List[int]]:
    """Parse Sudoku input from user."""
    print("\n" + "="*50)
    print("         SUDOKU SOLVER (SAT-based)")
    print("="*50)
    print("\nEnter your Sudoku puzzle row by row.")
    print("Use numbers 1-9 for clues and 0 (or .) for empty cells.")
    print("Format: space-separated values (e.g., '5 3 0 0 7 0 0 0 0')")
    print("-" * 50)
    
    grid = []
    for i in range(9):
        while True:
            try:
                row_input = input(f"Row {i+1}: ").strip()
                row = []
                
                for char in row_input.replace(',', ' ').split():
                    if char == '.':
                        row.append(0)
                    else:
                        num = int(char)
                        if num < 0 or num > 9:
                            raise ValueError
                        row.append(num)
                
                if len(row) != 9:
                    print(f"  Error: Expected 9 values, got {len(row)}. Try again.")
                    continue
                
                grid.append(row)
                break
                
            except ValueError:
                print("  Error: Invalid input. Use numbers 0-9 only. Try again.")
    
    return grid


def main():
    """Main function to run the Sudoku solver."""
    
    # Check if puzzle provided via command line argument
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        # Use example puzzle
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        print("\n" + "="*50)
        print("         SUDOKU SOLVER (SAT-based)")
        print("="*50)
        print("\nUsing example puzzle...")
    else:
        # Get input from user
        grid = parse_input()
    
    # Display input puzzle
    print_grid(grid, "INPUT PUZZLE:")
    
    # Solve
    print("Solving... ", end="", flush=True)
    solution = solve_sudoku(grid)
    
    if solution:
        print("✓ SOLVED!\n")
        print_grid(solution, "SOLUTION:")
        print("✓ Puzzle solved successfully!")
    else:
        print("✗ FAILED\n")
        print("No solution exists for this puzzle.")
        print("Please check if the input is valid.")
    
    print()


if __name__ == "__main__":
    main()
