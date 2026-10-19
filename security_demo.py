import re

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("security-demo")

# fake notes kept only in memory, nothing real is stored
NOTES = {"n1": "buy milk", "n2": "call mentor", "n3": "finish report"}


@mcp.tool()
def list_notes() -> str:
    """List all saved notes. This tool only reads, it never changes anything."""
    return "\n".join(f"{k}: {v}" for k, v in NOTES.items())


@mcp.tool()
def delete_note(note_id: str, confirm: bool = False) -> str:
    """Delete ONE note by its id. Only use confirm=true after the user has clearly agreed."""
    # limit what this tool can touch: only ids like n1, n2
    if not re.fullmatch(r"n\d+", note_id):
        raise ValueError("Note id must look like n1")
    if note_id not in NOTES:
        raise ValueError("No note with that id")
    # confirmation step for anything that deletes
    if not confirm:
        return f"Please ask the user to confirm deleting '{note_id}' ({NOTES[note_id]}), then call again with confirm=true."
    del NOTES[note_id]
    return f"Deleted {note_id}"


if __name__ == "__main__":
    mcp.run(transport="stdio")