"""Reduced Ordered Binary Decision Diagram (ROBDD) Engine.
100% Python Standard Library.
"""

class BDDManager:
    """Manages canonical reduced ordered binary decision diagrams."""
    def __init__(self, var_order):
        self.var_order = {var: idx for idx, var in enumerate(var_order)}
        self.unique_table = {}
        self.nodes = {0: (None, 0, 0), 1: (None, 1, 1)}
        self.next_id = 2
        self.computed_cache = {}

    def get_node(self, var, low, high):
        if low == high:
            return low
        key = (var, low, high)
        if key in self.unique_table:
            return self.unique_table[key]
        nid = self.next_id
        self.next_id += 1
        self.unique_table[key] = nid
        self.nodes[nid] = (var, low, high)
        return nid

    def var(self, name):
        return self.get_node(name, 0, 1)

    def ite(self, f, g, h):
        """Shannon expansion synthesis: if f then g else h."""
        if f == 1:
            return g
        if f == 0:
            return h
        if g == 1 and h == 0:
            return f
        if g == h:
            return g
        key = (f, g, h)
        if key in self.computed_cache:
            return self.computed_cache[key]

        vars_involved = [self.nodes[node][0] for node in (f, g, h) if self.nodes[node][0] is not None]
        top_var = min(vars_involved, key=lambda v: self.var_order[v])

        def cofactor(node, v):
            nv, low, high = self.nodes[node]
            if nv == v:
                return low, high
            return node, node

        f0, f1 = cofactor(f, top_var)
        g0, g1 = cofactor(g, top_var)
        h0, h1 = cofactor(h, top_var)

        low_child = self.ite(f0, g0, h0)
        high_child = self.ite(f1, g1, h1)
        res = self.get_node(top_var, low_child, high_child)
        self.computed_cache[key] = res
        return res

    def bdd_and(self, f, g):
        return self.ite(f, g, 0)

    def bdd_or(self, f, g):
        return self.ite(f, 1, g)

    def bdd_not(self, f):
        return self.ite(f, 0, 1)

    def bdd_xor(self, f, g):
        return self.ite(f, self.bdd_not(g), g)
