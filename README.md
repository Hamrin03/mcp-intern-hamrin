# Expense Tracker MCP Server

A small MCP (Model Context Protocol) server that lets an AI app like Claude Desktop save and read my daily expenses. The data is stored in a local SQLite file. Built by Hamrin as part of the MCP intern project.

## What it has

**Tools**
- `add_expense` - save one expense (amount, category, note, optional date)
- `monthly_total` - total money spent in a month (default: this month)
- `top_categories` - categories with the highest spending in a month

**Resource**
- `expenses://this-month` - all expenses of the current month

**Prompt**
- `budget-summary` - asks the model to write a short budget summary with 3 saving tips

## Host, client and server

- Host: Claude Desktop, the app I talk to.
- Client: lives inside the host and talks to my server using MCP.
- Server: `expense_server.py`. It wraps the SQLite database and shows it as tools, a resource and a prompt.

The model never talks to the server directly. The host decides which calls run.

## Setup (about 5 minutes)

You need Python 3.10 or higher.

```
git clone https://github.com/Hamrin03/mcp-intern-hamrin.git
cd mcp-intern-hamrin
python -m venv venv
venv\Scripts\activate
pip install "mcp[cli]" pytest
```

Note: this project uses MCP Python SDK 2.x, so the server class is `MCPServer` (it was `FastMCP` in version 1).

## Try it in MCP Inspector

```
npx @modelcontextprotocol/inspector python expense_server.py
```

Click Connect, open the Tools tab and run `add_expense`.

## Connect to Claude Desktop

Open Settings, Developer, Edit Config. Add this inside `mcpServers` (change the paths to your own folder):

```
"expense-tracker": {
  "command": "C:\\path\\to\\mcp-intern-hamrin\\venv\\Scripts\\python.exe",
  "args": ["C:\\path\\to\\mcp-intern-hamrin\\expense_server.py"]
}
```

Save the file, fully close Claude Desktop and open it again. Then ask: "Add an expense of 180 for transport today."

## Run the tests

```
pytest -v
```

5 tests check saving, bad amounts, monthly total, top categories order and bad month format. Tests use a temporary database, so your real `expenses.db` is not touched.

## Input checks

Bad input gives a clear error message instead of a crash. For example, an amount of 0 or less, an empty category, a wrong date format, or a month like "October" instead of `2026-10`.

## Files

- `expense_server.py` - the MCP server
- `test_expense_server.py` - tests
- `hello_server.py` - my first practice server (`add_numbers`)