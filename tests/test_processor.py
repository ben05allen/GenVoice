# pyright: basic

import pytest
import sqlite3
import tempfile

from genvoice.processor import get_template_data
from genvoice.db import dict_factory


@pytest.fixture(scope="module")
def tmp_db():
    with tempfile.NamedTemporaryFile(suffix="db") as tmp_db_file:
        conn = sqlite3.connect(tmp_db_file.name)
        conn.row_factory = dict_factory

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
                "0123456789",
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
            yield tmp_db_file.name

        finally:
            conn.close()


def test_get_template_data(tmp_db, monkeypatch):
    tmp_db_file = tmp_db
    monkeypatch.setenv("DB_PATH", tmp_db_file)

    template_data = get_template_data(1)
    assert template_data["sender"]["name"] == "Alice Jones"
    assert template_data["invoicee"]["name"] == "Acme Corp"
    assert template_data["bank_instructions"]["account_number"] == "0123456789"
    assert len(template_data["items"]) == 2
    assert template_data["total"] == "$1,700.00"
