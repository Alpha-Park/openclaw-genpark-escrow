# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Escrow MCP Server
Exposes cryptographic milestone escrow and multi-signature verification tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import OpenClawGenParkEscrow

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "openclaw-genpark-escrow", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_escrow_settlement",
                        "description": "Verifies milestone deliverables and authorizes tranche release upon multisig quorum.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "escrow_id": {"type": "string"},
                                "total_escrow_amount_usd": {"type": "number"},
                                "required_quorum_count": {"type": "integer"}
                            },
                            "required": ["escrow_id", "total_escrow_amount_usd"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "evaluate_escrow_settlement":
            escrow = OpenClawGenParkEscrow()
            res = escrow.evaluate_escrow_settlement(
                escrow_id=args.get("escrow_id", "ESCROW-001"),
                total_escrow_amount_usd=args.get("total_escrow_amount_usd", 10000.0),
                required_quorum_count=args.get("required_quorum_count", 2)
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        e = OpenClawGenParkEscrow()
        test_res = e.evaluate_escrow_settlement("TEST-ESC", 5000.0)
        print(f"Test Quorum: {test_res['multisig_quorum_satisfied']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
