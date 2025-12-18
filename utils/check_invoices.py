import sys
import sqlite3


database_file = sys.argv[1]


conn = sqlite3.connect(database_file)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
test_id = 1

# query = (
#     "SELECT id, invoicee, date, due_date, payment_link, bank_instructions, sender, start_date, end_date"
#     "FROM invoices WHERE id = ?"
# )
# cur.execute(query, (test_id,))

query = (
    "SELECT id, currency, amount, [url]"
    "FROM payment_links"
)
cur.execute(query)

row = cur.fetchone()
print(dict(row))    