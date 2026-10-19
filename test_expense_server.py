import pytest

import expense_server as es


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    # every test uses a fresh empty database, so expenses.db is never touched
    monkeypatch.setattr(es, "DB_PATH", tmp_path / "test.db")


def test_add_expense_saves():
    result = es.add_expense(250, "Food", "lunch", "2026-10-19")
    assert "Saved" in result
    assert "food" in result


def test_negative_amount_rejected():
    with pytest.raises(ValueError):
        es.add_expense(-5, "food")


def test_monthly_total():
    es.add_expense(100, "food", "", "2026-10-01")
    es.add_expense(50, "transport", "", "2026-10-02")
    assert "150" in es.monthly_total("2026-10")


def test_top_categories_order():
    es.add_expense(100, "food", "", "2026-10-01")
    es.add_expense(400, "books", "", "2026-10-02")
    first_line = es.top_categories("2026-10").splitlines()[0]
    assert first_line.startswith("books")


def test_bad_month_rejected():
    with pytest.raises(ValueError):
        es.monthly_total("October")