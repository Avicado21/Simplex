# Simplex Algorithm Implementation

A from-scratch implementation of the simplex method for solving linear programming problems, built in Python with NumPy.

## Overview

This project implements the simplex algorithm for solving linear programs of the form:

**Maximize/Minimize** c^T x  
**Subject to:** Ax = b, x ≥ 0

Developed as derivation from my coursework in Introduction to Optimization at the University of Pittsburgh.

## Features

- **Core simplex algorithm** with reduced cost computation and basis pivoting
- **Two-phase method** for problems without obvious starting basis
- **Unboundedness detection** — identifies when objective can increase without bound
- **Infeasibility detection** — identifies when no feasible solution exists
- **Minimization support** — handles both max and min problems
- **Interactive CLI** — enter custom problems or run built-in test cases

## Requirements

- Python 3.8+
- NumPy

```bash
pip install numpy
```

## Usage

```bash
python simplex.py
```

Then choose from:
1. Enter problem manually
2. Run test: basic feasible (identity basis)
3. Run test: unbounded problem
4. Run test: two-phase required
5. Run test: infeasible problem

### Programmatic Usage

```python
import numpy as np
from simplex import simplex

A = np.array([[1, 1, 1, 0, 0],
              [1, 0, 0, 1, 0],
              [0, 1, 0, 0, 1]], dtype=float)
b = np.array([4, 3, 2], dtype=float)
c = np.array([3, 2, 0, 0, 0], dtype=float)

result = simplex(A, b, c)
print(result.x)          # [3. 1. 0. 0. 1.]
print(result.objective)  # 11.0
```

## Example Output
### ==================================================
### SIMPLEX SOLVER: Maximize
### Initial x = [0. 0. 4. 3. 2.], objective = 0.0000
### Iteration 1: x1 enters, x3 leaves | objective = 9.0000
### Iteration 2: x2 enters, x5 leaves | objective = 11.0000
### Optimal: x = [3. 1. 0. 0. 1.], objective = 11.0000
### ==================================================
### RESULT SUMMARY
### Status: optimal
### Solution: [3. 1. 0. 0. 1.]
### Objective: 11.0000
### Iterations: 2

## How It Works

1. **Initialization** — Find starting basic feasible solution (identity basis or two-phase)
2. **Reduced costs** — Compute improvement potential for each nonbasic variable
3. **Pivot selection** — Choose entering variable (largest positive reduced cost)
4. **Ratio test** — Determine leaving variable (minimum ratio)
5. **Basis update** — Swap entering/leaving, update solution
6. **Repeat** — Until optimal, unbounded, or infeasible

## Project Structure
Simplex/
├── simplex.py      # Main implementation
└── README.md       # This file

## Limitations

- Bland's rule not implemented (cycling possible on degenerate problems)
- Degenerate artificial-in-basis case has basic handling only

## License

MIT

## Author

Avinash Kottakota  
University of Pittsburgh, B.S. Computer Science & Data Science
