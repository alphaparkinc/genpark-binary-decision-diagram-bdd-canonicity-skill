# ROBDD Canonical Decision Diagram Skill

Reduced Ordered Binary Decision Diagram (ROBDD) engine featuring hash-consed unique tables and the ITE operator.

```mermaid
flowchart TD
    Var["Variable Order (x1 < x2 < x3)"] --> Table["Unique Table & Computed Cache"]
    Table --> ITE["Shannon ITE Expansion: f = v*f1 + ~v*f0"]
    ITE --> Canonicity["Canonical Node Identification"]
    Canonicity --> Equiv["O(1) Formal Equivalence Verification"]
```

## Features
- **100% Python Standard Library**: Pure memoized recursive data structure.
- **Canonical Representation**: Equivalence checking reduces to pointer/ID equality.
- **Complete Boolean Algebra**: AND, OR, NOT, XOR, and ITE operations.
