import sqlite3
from datetime import date, datetime
from pathlib import Path

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("expense-tracker")
DB_PATH = Path(__file__).parent / "expenses.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS expenses ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "amount REAL NOT NULL, category TEXT NOT NULL, "
        "note TEXT, spent_on TEXT NOT NULL)"
    )
    return conn


def pick_month(month):
    if not month:
        return date.today().strftime("%Y-%m")
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("Month must look like 2026-10")
    return month


@mcp.tool()
def add_expense(amount: float, category: str, note: str = "", spent_on: str = "") -> str:
    """Save one expense. spent_on is optional (YYYY-MM-DD), default is today."""
    if amount <= 0:
        raise ValueError("Amount must be more than 0")
    if not category.strip():
        raise ValueError("Category cannot be empty")
    if not spent_on:
        spent_on = date.today().isoformat()
    try:
        datetime.strptime(spent_on, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must look like 2026-10-19")
    with get_db() as db:
        db.execute(
            "INSERT INTO expenses (amount, category, note, spent_on) VALUES (?, ?, ?, ?)",
            (amount, category.strip().lower(), note, spent_on),
        )
    return f"Saved: {amount} on {category.strip().lower()} ({spent_on})"


@mcp.tool()
def monthly_total(month: str = "") -> str:
    """Total money spent in a month. month looks like 2026-10, default is this month."""
    month = pick_month(month)
    with get_db() as db:
        row = db.execute(
            "SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM expenses WHERE spent_on LIKE ?",
            (month + "%",),
        ).fetchone()
    return f"Total for {month}: {row[0]} across {row[1]} expenses"


@mcp.tool()
def top_categories(month: str = "", limit: int = 3) -> str:
    """Categories where the most money was spent in a month."""
    month = pick_month(month)
    if limit < 1:
        raise ValueError("Limit must be at least 1")
    with get_db() as db:
        rows = db.execute(
            "SELECT category, SUM(amount) FROM expenses WHERE spent_on LIKE ? "
            "GROUP BY category ORDER BY SUM(amount) DESC LIMIT ?",
            (month + "%", limit),
        ).fetchall()
    if not rows:
        return f"No expenses found for {month}"
    return "\n".join(f"{c}: {t}" for c, t in rows)


@mcp.resource("expenses://this-month")
def this_month_expenses() -> str:
    """All expenses of the current month."""
    month = date.today().strftime("%Y-%m")
    with get_db() as db:
        rows = db.execute(
            "SELECT spent_on, category, amount, note FROM expenses "
            "WHERE spent_on LIKE ? ORDER BY spent_on",
            (month + "%",),
        ).fetchall()
    if not rows:
        return "No expenses this month"
    return "\n".join(f"{d} | {c} | {a} | {n}" for d, c, a, n in rows)


@mcp.prompt(name="budget-summary")
def budget_summary(month: str = "") -> str:
    """Ask for a short budget summary of a month."""
    return (
        f"Use monthly_total and top_categories for month '{month or 'this month'}'. "
        "Then write a short budget summary with 3 simple saving tips."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")