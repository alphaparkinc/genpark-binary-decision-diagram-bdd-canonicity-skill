"""Example demonstrating ROBDD canonicity and equivalence."""
from client import BDDManager

def main():
    mgr = BDDManager(["x", "y"])
    x = mgr.var("x")
    y = mgr.var("y")
    
    # De Morgan's Law verification: NOT(x AND y) == (NOT x) OR (NOT y)
    lhs = mgr.bdd_not(mgr.bdd_and(x, y))
    rhs = mgr.bdd_or(mgr.bdd_not(x), mgr.bdd_not(y))
    print(f"LHS Node ID: {lhs}")
    print(f"RHS Node ID: {rhs}")
    print(f"Canonical Identity: {lhs == rhs} (Provably Equivalent!)")

if __name__ == "__main__":
    main()
