# pyright: basic

from contextlib import contextmanager
from dotenv import load_dotenv
import os
from pathlib import Path
import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {k: v for k, v in zip(fields, row)}


@contextmanager
def get_cursor():
    _ = load_dotenv()

    db_path = Path(os.environ.get("DB_PATH", "invoices.db"))
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory

    try:
        cursor = conn.cursor()
        yield cursor
    finally:
        conn.close()


def get_invoice(id: int):
    query = (
        "SELECT id, invoicee, date, due_date, bank_instructions, sender, start_date, end_date "
        "FROM invoices WHERE id = ?"
    )

    with get_cursor() as cur:
        cur.execute(query, (id,))
        row = cur.fetchone()

        return row


def get_sender(id: int):
    query = (
        "SELECT name, street_address, suburb, prefecture, postcode, country, email, phone "
        " FROM senders WHERE id = ?"
    )

    with get_cursor() as cur:
        cur.execute(query, (id,))
        row = cur.fetchone()

        return row


def get_bank_instructions(id: int):
    query = (
        "SELECT bank_name, branch, bic, recipient_type, bank_code, branch_code, account, account_type "
        "FROM bank_instructions WHERE id = ?"
    )

    with get_cursor() as cur:
        cur.execute(query, (id,))
        row = cur.fetchone()

        return row


def get_invoicee(id: int):
    query = (
        "SELECT name, contact_name, street_address, suburb, city, postcode, country, email, phone "
        "FROM invoicees WHERE id = ?"
    )

    with get_cursor() as cur:
        cur.execute(query, (id,))
        row = cur.fetchone()

        return row


def get_line_items(invoice_id: int):
    query = (
        "SELECT description, currency, quantity, price "
        "FROM line_items WHERE invoice_id = ?"
    )

    with get_cursor() as cur:
        cur.execute(query, (invoice_id,))
        rows = cur.fetchall()

        return rows
