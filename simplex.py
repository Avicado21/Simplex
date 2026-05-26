'''
Avinash Kottakota
A simple simplex custom implementation in python
Derived from my experience in Introduction to Optimization
'''

# simple simplex imports
from typing import Optional
from enum import Enum
from dataclasses import dataclass
import numpy as np


# custom data class for the system
# using these to make returns cleaner and more informative

class SimplexStatus(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"
    INVALID = "invalid"

# a lot like a C struct for returning results from the simplex function 
@dataclass
class SimplexResult:
    status: SimplexStatus
    x: Optional[np.ndarray]
    objective: Optional[float]
    basis: Optional[list]
    iterations: int
    message: str = ""


# input handling
# have to handle terminal array input efficiently

def getArrayInput(prompt):
    
    print(prompt)
    
    array = []
    
    rows = input("enter number of rows: ")
    cols = input("enter number of columns: ")
    
    row = int(rows)
    col = int(cols)
    
    for i in range(row):
        r = input(f"enter row {i+1} values separated by space: ")
        vals = list(float(x) for x in r.split())
        if len(vals) != col:
            print(f"Error: expected {col} values, got {len(vals)}. Please try again.")
            return getArrayInput(prompt)
        array.append(vals)
        
    np_array = np.array(array, dtype=float)
    
    return np_array

# for vector input, with optional length check
# this is for b and c vectors, where we want to ensure correct dimensions
def getVectorInput(prompt, expected_length=None):
    
    print(prompt)
    line = input("> ").strip()
    vals = [float(x) for x in line.split()]
    
    if expected_length and len(vals) != expected_length:
        print(f"Error: expected {expected_length} values, got {len(vals)}. Please try again.")
        return getVectorInput(prompt, expected_length)
    
    return np.array(vals, dtype=float)

# main function to get problem input interactively
# we ask the user for the objective type, then for A, b, c matrices/vectors
'''
    interactive problem input for simplex
    returns A, b, c, minimize flag
'''
def getProblemInput():
    print("\n" + "="*50)
    print("SIMPLEX SOLVER - Problem Input")
    print("="*50)
    
    # get objective type
    print("\nMaximize or minimize? (max/min): ", end="")
    obj_type = input().strip().lower()
    minimize = obj_type.startswith("min")
    
    # get A matrix
    A = getArrayInput("\nEnter matrix A (constraint matrix):")
    rows, cols = A.shape
    
    # get b vector
    b = getVectorInput(f"Enter vector b (right-hand side, {rows} values):", expected_length=rows)
    
    # get c vector
    c = getVectorInput(f"Enter vector c (objective coefficients, {cols} values):", expected_length=cols)
    
    print("\n" + "-"*50)
    print("Problem received:")
    print(f"  {'Minimize' if minimize else 'Maximize'} c^T x")
    print(f"  Subject to: Ax = b, x >= 0")
    print(f"  A: {rows}x{cols}, b: {rows} entries, c: {cols} entries")
    print("-"*50)
    
    return A, b, c, minimize


# Validation
# arrays are finicky so this lets us make sure all the pieces fit

'''
    check that inputs are valid for simplex
    returns (is_valid, error_message)
'''
def validateInputs(A, b, c):
    # check A is 2D
    if A.ndim != 2:
        return False, "A must be a 2D matrix"
    
    rows, cols = A.shape
    
    # check b dimensions
    if b.ndim != 1 or len(b) != rows:
        return False, f"b must be 1D array of length {rows}, got length {len(b)}"
    
    # check c dimensions
    if c.ndim != 1 or len(c) != cols:
        return False, f"c must be 1D array of length {cols}, got length {len(c)}"
    
    # check for negative b entries
    if np.any(b < 0):
        return False, "b has negative entries — multiply those constraint rows by -1 first"
    
    # check rank
    if np.linalg.matrix_rank(A) < rows:
        return False, "A does not have full row rank — redundant or inconsistent constraints"
    
    return True, ""


# some lovely helpers for the simplex algorithm basically just checking if we need two-phase or not

# alright 2 phase simplex check:
def needs_two_phase(A):
    row, col = A.shape
    
    # Check if last m columns form identity matrix
    I_check = A[:, -row:]
    
    if np.allclose(I_check, np.eye(row)):
        return False  # Easy basis exists, one-phase is fine
    else:
        return True   # Need two-phase


# core simplex

def doSimplex(A, b, c, basis=None, verbose=True):
    # we take the inputs and then run the simplex until our reduced costs are all negative
    # that is, for the maximization route
    
    row, col = A.shape
    
    # step 0: find a basic feasible point
    if basis is None:
        # assume identity matrix in last m columns
        basis = list(range(col - row, col))
    else:
        # use provided basis
        basis = list(basis)  # copy to avoid mutating original
    
    # nonbasis is everything not in basis
    nonbasis = [i for i in range(col) if i not in basis]
    
    # get our x vector
    x = np.zeros(col)
    AB = A[:, basis]
    x[basis] = np.linalg.solve(AB, b)  # handles non-identity basis too
    
    if verbose:
        print(f"\nInitial x = {np.round(x, 4)}, objective = {c @ x:.4f}")
    
    # step 1: reduced costs
    # r = cNT − cBT AB-1 AN
    
    done = False
    iteration = 0
    
    # while not done, we keep on doing each pivot and iteration
    # this is maximizing route
    while not done:
        iteration += 1
        
        # extract current basis and nonbasis matrices from A
        AB = A[:, basis]
        AN = A[:, nonbasis]
        cB = c[basis]
        cN = c[nonbasis]
        
        # reduced costs: how much objective improves per unit increase in each nonbasic var
        costs = cN - cB @ np.linalg.solve(AB, AN)
        
        # for maximization: all reduced costs <= 0 means optimal
        # using small tolerance for numerical stability
        if np.all(costs <= 1e-10):
            done = True
            
        else:
            # find the entering variable (largest positive reduced cost)
            entering_idx = np.argmax(costs)       # index within nonbasis list
            entering = nonbasis[entering_idx]     # actual column index in A
            
            # get the direction vector
            # d = B⁻¹ * a_j tells us how basic vars change per unit increase in entering var
            d = np.linalg.solve(AB, A[:, entering])
            
            # unboundedness check: if no positive d entries, we can go to infinity
            if np.all(d <= 1e-10):
                if verbose:
                    print("Problem is unbounded!")
                return SimplexResult(
                    status=SimplexStatus.UNBOUNDED,
                    x=None,
                    objective=np.inf,
                    basis=basis,
                    iterations=iteration,
                    message="Objective can increase without bound"
                )
            
            # now we have the direction vector, we need to find the step size
            # we do this by finding the minimum ratio of xB / dB for all positive entries in dB
            x_B = x[basis]
            ratios = np.full(row, np.inf)
            
            for i in range(row):
                if d[i] > 1e-10:
                    ratios[i] = x_B[i] / d[i]
                    
            step_size = np.min(ratios)
            leaving_idx = np.argmin(ratios)   # index within basis list
            leaving = basis[leaving_idx]       # actual column index in A
            
            # now we update our x vector
            # basic vars decrease along direction d
            x[basis] -= step_size * d
            # entering var was 0, now becomes step_size
            x[entering] = step_size
            # leaving var becomes 0 (now nonbasic)
            x[leaving] = 0
            
            # swap the entering and leaving variables in our index lists
            basis[leaving_idx] = entering
            nonbasis[entering_idx] = leaving
            
            # print iteration details
            if verbose:
                print(f"Iteration {iteration}: x{entering+1} enters, x{leaving+1} leaves | objective = {c @ x:.4f}")
    
    # clean up near-zero values for nicer output
    x = np.where(np.abs(x) < 1e-10, 0, x)
    
    if verbose:
        print(f"\nOptimal: x = {x}, objective = {c @ x:.4f}")
    
    return SimplexResult(
        status=SimplexStatus.OPTIMAL,
        x=x,
        objective=c @ x,
        basis=basis,
        iterations=iteration
    )

# need the phase 2
'''
    two-phase simplex for problems without obvious starting basis
    Phase I: find a basic feasible solution (or prove infeasible)
    Phase II: optimize the original objective
'''
def two_phase_simplex(A, b, c, verbose=True):
    row, col = A.shape
    
    if verbose:
        print("\n" + "="*50)
        print("PHASE I: Finding initial basic feasible solution")
        print("="*50)
    
    # Phase I: build augmented problem
    # add artificial variables to get an identity basis
    A_phase1 = np.hstack([A, np.eye(row)])
    c_phase1 = np.concatenate([np.zeros(col), -np.ones(row)])
    
    # Run simplex on Phase I
    result_phase1 = doSimplex(A_phase1, b, c_phase1, verbose=verbose)
    
    # Check feasibility
    # if we can't get artificials to zero, original problem is infeasible
    if not np.isclose(result_phase1.objective, 0, atol=1e-8):
        if verbose:
            print("\nProblem is infeasible!")
        return SimplexResult(
            status=SimplexStatus.INFEASIBLE,
            x=None,
            objective=None,
            basis=None,
            iterations=result_phase1.iterations,
            message="No feasible solution exists"
        )
    
    if verbose:
        print("\n" + "="*50)
        print("PHASE II: Optimizing original objective")
        print("="*50)
    
    # Phase II: extract basis indices that are in original problem (< col)
    # Filter out any artificial variables still in basis
    basis_for_phase2 = [i for i in result_phase1.basis if i < col]
    
    # If artificials still in basis at zero value, need to handle
    if len(basis_for_phase2) < row:
        if verbose:
            print("Warning: artificial variable in basis (degenerate case)")
        # For now, just proceed — advanced handling needed for full robustness
    
    result_phase2 = doSimplex(A, b, c, basis=basis_for_phase2, verbose=verbose)
    result_phase2.iterations += result_phase1.iterations
    
    return result_phase2


# the main simplex function that handles both maximization and minimization, and decides whether to use two-phase or not based on the input

'''
    main simplex solver entry point
    handles both maximization (default) and minimization
'''
def simplex(A, b, c, minimize=False, verbose=True):
    # validate inputs first
    valid, error = validateInputs(A, b, c)
    if not valid:
        if verbose:
            print(f"\nInput error: {error}")
        return SimplexResult(
            status=SimplexStatus.INVALID,
            x=None,
            objective=None,
            basis=None,
            iterations=0,
            message=error
        )
    
    # minimization: negate c, maximize, negate result
    c_use = -c if minimize else c
    
    if verbose:
        print("\n" + "="*50)
        print(f"SIMPLEX SOLVER: {'Minimize' if minimize else 'Maximize'}")
        print("="*50)
    
    # choose one-phase or two-phase based on whether we have easy identity basis
    if needs_two_phase(A):
        result = two_phase_simplex(A, b, c_use, verbose=verbose)
    else:
        result = doSimplex(A, b, c_use, verbose=verbose)
    
    # negate objective back for minimization
    if minimize and result.objective is not None:
        result.objective = -result.objective
    
    return result


# main method to run the simplex solver with interactive input or predefined test cases

def main():
    print("\n" + "="*60)
    print("  SIMPLEX ALGORITHM IMPLEMENTATION")
    print("  Avinash Kottakota - Introduction to Optimization")
    print("="*60)
    
    print("\nChoose input method:")
    print("  1. Enter problem manually")
    print("  2. Run test: basic feasible (identity basis)")
    print("  3. Run test: unbounded problem")
    print("  4. Run test: two-phase required")
    print("  5. Run test: infeasible problem")
    
    choice = input("\nChoice (1-5): ").strip()
    
    if choice == "1":
        A, b, c, minimize = getProblemInput()
        result = simplex(A, b, c, minimize=minimize)
    
    elif choice == "2":
        # basic feasible check
        print("\nTest: Maximize 3x₁ + 2x₂")
        print("      s.t. x₁ + x₂ ≤ 4, x₁ ≤ 3, x₂ ≤ 2")
        A = np.array([[1, 1, 1, 0, 0],
                      [1, 0, 0, 1, 0],
                      [0, 1, 0, 0, 1]], dtype=float)
        b = np.array([4, 3, 2], dtype=float)
        c = np.array([3, 2, 0, 0, 0], dtype=float)
        result = simplex(A, b, c)
    
    elif choice == "3":
        # unbounded check
        print("\nTest: Maximize 2x₁ + x₂")
        print("      s.t. -x₁ + x₂ ≤ 1, x₁ - x₂ ≤ 1")
        A = np.array([[-1, 1, 1, 0],
                      [1, -1, 0, 1]], dtype=float)
        b = np.array([1, 1], dtype=float)
        c = np.array([2, 1, 0, 0], dtype=float)
        result = simplex(A, b, c)
    
    elif choice == "4":
        # two-phase required
        print("\nTest: Maximize x₁ + x₂")
        print("      s.t. x₁ + 2x₂ = 4, 2x₁ + x₂ = 5")
        A = np.array([[1, 2],
                      [2, 1]], dtype=float)
        b = np.array([4, 5], dtype=float)
        c = np.array([1, 1], dtype=float)
        result = simplex(A, b, c)
    
    elif choice == "5":
        # infeasible check
        print("\nTest: Maximize x₁ + x₂")
        print("      s.t. x₁ + x₂ = 1, x₁ + x₂ = 2 (impossible!)")
        A = np.array([[1, 1],
                      [1, 1]], dtype=float)
        b = np.array([1, 2], dtype=float)
        c = np.array([1, 1], dtype=float)
        result = simplex(A, b, c)
    
    else:
        print("Invalid choice, bruh")
        return
    
    # final summary
    print("\n" + "="*50)
    print("RESULT SUMMARY")
    print("="*50)
    print(f"  Status: {result.status.value}")
    if result.x is not None:
        print(f"  Solution: {result.x}")
    if result.objective is not None:
        print(f"  Objective: {result.objective:.4f}")
    print(f"  Iterations: {result.iterations}")
    if result.message:
        print(f"  Message: {result.message}")


if __name__ == "__main__":
    main()