"""MCP stdio server for ROBDD Engine."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import BDDManager

mgr = BDDManager(["a", "b", "c", "d", "e"])

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "check_equivalence_bdd",
                        "description": "Check if two Boolean expressions are canonically equivalent via ROBDD",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "variables": {"type": "array", "items": {"type": "string"}},
                                "op": {"type": "string", "enum": ["xor_equivalence", "demorgan_equivalence"]}
                            },
                            "required": ["op"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "check_equivalence_bdd":
            op = args.get("op")
            m = BDDManager(["a", "b"])
            a = m.var("a")
            b = m.var("b")
            if op == "xor_equivalence":
                f1 = m.bdd_xor(a, b)
                f2 = m.bdd_or(m.bdd_and(a, m.bdd_not(b)), m.bdd_and(m.bdd_not(a), b))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"equivalent": (f1 == f2), "node_id": f1}}
            elif op == "demorgan_equivalence":
                f1 = m.bdd_not(m.bdd_and(a, b))
                f2 = m.bdd_or(m.bdd_not(a), m.bdd_not(b))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"equivalent": (f1 == f2), "node_id": f1}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "unsupported op"}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
