from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hello-server")


@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")