"""
Model Context Protocol (MCP) Server Infrastructure
Implements lightweight MCP JSON-RPC protocol server for agentic tool discovery and execution.
"""

import json
from typing import Dict, Any, List
from src.mcp.tools import MCP_TOOL_MANIFEST, BMSToolHandler

class MCPServer:
    def __init__(self, simulation_engine):
        self.tool_handler = BMSToolHandler(simulation_engine)
        self.manifest = MCP_TOOL_MANIFEST

    def get_tool_manifest(self) -> List[Dict[str, Any]]:
        return self.manifest

    def process_rpc_request(self, json_rpc_payload: str) -> str:
        try:
            req = json.loads(json_rpc_payload)
            method = req.get("method")
            params = req.get("params", {})
            req_id = req.get("id", 1)

            if method == "tools/list":
                return json.dumps({"jsonrpc": "2.0", "result": {"tools": self.manifest}, "id": req_id})
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.tool_handler.execute_tool(name, arguments)
                return json.dumps({"jsonrpc": "2.0", "result": result, "id": req_id})
            else:
                return json.dumps({"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Method {method} not found"}, "id": req_id})
        except Exception as e:
            return json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": None})

    def direct_tool_call(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        return self.tool_handler.execute_tool(tool_name, kwargs)
