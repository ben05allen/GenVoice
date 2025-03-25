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
        "SELECT invoicee, date, due_date, bank_instructions, sender, start_date, end_date "
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
    cur = get_cursor()

    return cur.execute("SELECT * FROM bank_instructions WHERE id = ?", (id,)).fetchone()


def get_invoicee(id: int):
    cur = get_cursor()

    return cur.execute("SELECT * FROM invoicees WHERE id = ?", (id,)).fetchone()


def get_line_items(invoice_id: int):
    cur = get_cursor()

    return cur.execute(
        "SELECT * FROM line_items WHERE invoice_id = ?", (invoice_id,)
    ).fetchall()


if __name__ == "__main__":
    print(get_sender(1))
