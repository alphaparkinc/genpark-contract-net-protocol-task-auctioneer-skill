import sys
import json
from client import ContractNetProtocol

cnp = ContractNetProtocol()
cnp.register_agent("worker_alpha", 2.0)
cnp.register_agent("worker_beta", 1.8)

def handle_rpc(line):
    global cnp
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-contract-net-protocol-task-auctioneer-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "auction_task",
                    "description": "Broadcast task announcement and award to lowest-cost agent contractor",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "task_name": {"type": "string"},
                            "required_effort": {"type": "number"}
                        },
                        "required": ["task_name", "required_effort"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "auction_task":
            name = args.get("task_name")
            eff = args.get("required_effort", 1.0)
            data = cnp.announce_and_award(name, eff)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
