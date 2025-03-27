# pyright: basic

from contextlib import contextmanager
import pytest
import sqlite3

import genvoice.db as db


@contextmanager
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = db.dict_factory

    cursor = conn.cursor()

    # set up test bank instructions
    _ = cursor.execute("""
        CREATE TABLE bank_instructions( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_name TEXT NOT NULL,
            branch TEXT NOT NULL,
            bic TEXT NOT NULL,
            recipient_type TEXT,
            bank_code TEXT,
            branch_code TEXT,
            account TEXT,
            account_type TEXT)
        """)

    bank_instructions = [
        (
            "Mock Bank",
            "Main St",
            "MOCKBANK",
            "Private",
            "1234",
            "012",
            "1234567890",
            "Futsuu",
        )
    ]

    _ = cursor.executemany(
        """
        INSERT INTO bank_instructions (
            bank_name, branch, bic, recipient_type, bank_code, branch_code, account, account_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        bank_instructions,
    )

    # set up test invoicee
    _ = cursor.execute("""
        CREATE TABLE invoicees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_name TEXT,
            street_address TEXT,
            suburb TEXT,
            city TEXT,
            postcode TEXT,
            country TEXT,
            email TEXT,
            phone TEXT)
    """)

    invoicee = [
        (
            "Acme Corp",
            "John Smith",
            "123 Main St",
            "Downtown",
            "Big Smoke",
            "1234",
            "Atlantis",
            "john@email.com",
            "01-234-5678",
        )
    ]

    _ = cursor.executemany(
        """
        INSERT INTO invoicees (
            name, contact_name, street_address, suburb, city, postcode, country, email, phone
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
        """,
        invoicee,
    )

    # set up test sender
    _ = cursor.execute("""
        CREATE TABLE senders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            street_address TEXT NOT NULL,
            suburb TEXT NOT NULL,
            prefecture TEXT NOT NULL,
            postcode TEXT NOT NULL,
            country TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL)
    """)

    sender = [
        (
            "Alice Jones",
            "10 Pleasant Place",
            "Sunnyville",
            "South State",
            "9876",
            "Bigland",
            "Alice@theinternet.com",
            "09-876-5432",
        )
    ]

    _ = cursor.executemany(
        """
        INSERT INTO senders (
            name, street_address, suburb, prefecture, postcode, country, email, phone
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sender,
    )

    # set up test invoice
    _ = cursor.execute("""
        CREATE TABLE invoices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoicee INTEGER NOT NULL,
            date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            bank_instructions INTEGER NOT NULL,
            sender INTEGER NOT NULL,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY(bank_instructions) REFERENCES bank_instructions(id),
            FOREIGN KEY(invoicee) REFERENCES invoicees(id),
            FOREIGN KEY(sender) REFERENCES senders(id))
    """)

    invoice = [
        (
            1,
            "2020-01-01",
            "2020-01-15",
            1,
            1,
            "2019-12-01",
            "2019-12-31",
        )
    ]

    _ = cursor.executemany(
        """
        INSERT INTO invoices (
            invoicee, date, due_date, bank_instructions, sender, start_date, end_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        invoice,
    )

    # set up some test invoice line items
    _ = cursor.execute(""" 
        CREATE TABLE line_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL DEFAULT 1,
            description TEXT,
            currency TEXT,
            quantity NUMERIC,
            price NUMERIC,
            FOREIGN KEY("invoice_id") REFERENCES "invoices"("id"))
    """)

    line_items = [
        (1, "Services Rendered", "JPY", 100, 5),
        (1, "Professional Services", "JPY", 200, 6),
    ]

    _ = cursor.executemany(
        """
        INSERT INTO line_items (
            invoice_id, description, currency, quantity, price
        ) VALUES (?, ?, ?, ?, ?)
        """,
        line_items,
    )

    try:
        conn.commit()
        yield cursor

    finally:
        conn.close()


def test_fetch_bank_instructions(monkeypatch):
    monkeypatch.setattr(db, "get_cursor", in_memory_db)

    row = db.get_bank_instructions(1)
    print(row)
    with pytest.raises(KeyError):
        assert row["id"] == 1

    assert isinstance(row, dict)
    assert row["bank_name"] == "Mock Bank"
    assert row["bank_code"] == "1234"
    assert row["recipient_type"] == "Private"
    assert row["bic"] == "MOCKBANK"
    assert row["branch"] == "Main St"
    assert row["branch_code"] == "012"
    assert row["account"] == "1234567890"
    assert row["account_type"] == "Futsuu"


def test_fetch_invoicee(monkeypatch):
    monkeypatch.setattr(db, "get_cursor", in_memory_db)

    row = db.get_invoicee(1)
    with pytest.raises(KeyError):
        assert row["id"] == 1

    assert isinstance(row, dict)
    assert row["name"] == "Acme Corp"
    assert row["contact_name"] == "John Smith"
    assert row["street_address"] == "123 Main St"
    assert row["suburb"] == "Downtown"
    assert row["city"] == "Big Smoke"
    assert row["postcode"] == "1234"
    assert row["country"] == "Atlantis"
    assert row["email"] == "john@email.com"
    assert row["phone"] == "01-234-5678"


def test_fetch_sender(monkeypatch):
    monkeypatch.setattr(db, "get_cursor", in_memory_db)

    row = db.get_sender(1)
    with pytest.raises(KeyError):
        assert row["id"] == 1

    assert isinstance(row, dict)
    assert row["name"] == "Alice Jones"
    assert row["street_address"] == "10 Pleasant Place"
    assert row["suburb"] == "Sunnyville"
    assert row["prefecture"] == "South State"
    assert row["postcode"] == "9876"
    assert row["country"] == "Bigland"
    assert row["email"] == "Alice@theinternet.com"
    assert row["phone"] == "09-876-5432"


def test_fetch_invoice(monkeypatch):
    monkeypatch.setattr(db, "get_cursor", in_memory_db)

    row = db.get_invoice(1)
    assert isinstance(row, dict)
    assert row["id"] == 1
    assert row["invoicee"] == 1
    assert row["date"] == "2020-01-01"
    assert row["due_date"] == "2020-01-15"
    assert row["bank_instructions"] == 1
    assert row["sender"] == 1
    assert row["start_date"] == "2019-12-01"
    assert row["end_date"] == "2019-12-31"


def test_fetch_line_items(monkeypatch):
    monkeypatch.setattr(db, "get_cursor", in_memory_db)

    rows = db.get_line_items(1)
    assert len(rows) == 2
    with pytest.raises(KeyError):
        assert rows[0]["id"] == 1

    assert isinstance(rows[1], dict)
    assert rows[0]["description"] == "Services Rendered"
    assert rows[0]["currency"] == "JPY"
    assert rows[0]["quantity"] == 100
    assert rows[0]["price"] == 5
