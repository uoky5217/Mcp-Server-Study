import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel import Server
import mcp.types as types 
from mcp.server.sse import SseServerTransport 
from starlette.applications import Starlette 
from starlette.routing import Mount, Route

sse = SseServerTransport("/messages")
# mcp = FastMCP("My App", transport=sse)
app = Server("mcp server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="calculate_sum",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        ),
        types.Tool(
            name="calculate_subtract",
            description="Subtract two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        ),
        types.Tool(
            name="calculate_multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            } 
        ),
        types.Tool(
            name="calculate_divide",
            description="Divide two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            } 
        )
    ]

@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "calculate_sum":
        a = arguments["a"]
        b = arguments["b"]
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/add", json={"a": a, "b": b})
            return [types.TextContent(type="text", text=response.text)]
    elif name == "calculate_subtract":
        a = arguments["a"]
        b = arguments["b"]
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/subtract", json={"a": a, "b": b})
            return [types.TextContent(type="text", text=response.text)]
    elif name == "calculate_multiply":
        a = arguments["a"]
        b = arguments["b"]
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/multiply", json={"a": a, "b": b})
            return [types.TextContent(type="text", text=response.text)]
    elif name == "calculate_divide":
        a = arguments["a"]
        b = arguments["b"]
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/divide", json={"a": a, "b": b})
            return [types.TextContent(type="text", text=response.text)]
    raise ValueError(f"Tool not found: {name}")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

starlette_app = Starlette(
    debug=True, 
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message)
        # Route("/messages", endpoint=handle_messages, methods=["POST"]),
        ]
)

import uvicorn
if __name__ == "__main__":
    uvicorn.run(starlette_app, host="127.0.0.1", port=8001)