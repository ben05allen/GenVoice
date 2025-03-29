import sqlite3

database_file = "your_invoice.db"


conn = sqlite3.connect(database_file)
try:
    cursor = conn.cursor()

    # set up bank instructions table
    _ = cursor.execute("""
            CREATE TABLE bank_instructions( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bank_name TEXT NOT NULL DEFAULT 'Bank Name',
                branch TEXT NOT NULL DEFAULT 'Branch',
                bic TEXT NOT NULL DEFAULT 'Bank BIC',
                recipient_type TEXT,
                bank_code TEXT,
                branch_code TEXT,
                account TEXT NOT NULL DEFAULT 'Account No',
                account_type TEXT)
            """)

    # set up invoicee table
    _ = cursor.execute("""
            CREATE TABLE invoicees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT 'Invoicees organization',
                contact_name TEXT DEFAULT 'Name of contact person',
                street_address TEXT DEFAULT '987 Main St',
                suburb TEXT DEFAULT 'Suburb',
                city TEXT DEFAULT 'City',
                postcode TEXT DEFAULT 'Postcode',
                country TEXT DEFAULT 'Country',
                email TEXT DEFAULT 'Invoicee Email',
                phone TEXT DEFAULT 'Invoicees phone no')
        """)

    # set up senders table
    _ = cursor.execute("""
            CREATE TABLE senders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT 'Your Name',
                street_address TEXT NOT NULL DEFAULT '123 Street St',
                suburb TEXT NOT NULL DEFAULT 'Suburb',
                prefecture TEXT NOT NULL DEFAULT 'Prefecture',
                postcode TEXT NOT NULL DEFAULT 'Postcode',
                country TEXT NOT NULL DEFAULT 'Country',
                email TEXT NOT NULL DEFAULT 'Your email',
                phone TEXT NOT NULL DEFAULT 'Your phone no')
        """)

    # set up invoices table
    _ = cursor.execute("""
            CREATE TABLE invoices(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoicee INTEGER NOT NULL DEFAULT 1,
                date TEXT NOT NULL DEFAULT '2020-01-01',
                due_date TEXT NOT NULL DEFAULT '2020-01-15',
                bank_instructions INTEGER NOT NULL DEFAULT 1,
                sender INTEGER NOT NULL DEFAULT 1,
                start_date TEXT,
                end_date TEXT,
                FOREIGN KEY(bank_instructions) REFERENCES bank_instructions(id),
                FOREIGN KEY(invoicee) REFERENCES invoicees(id),
                FOREIGN KEY(sender) REFERENCES senders(id))
        """)

    # set up some invoice line items table
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

    conn.commit()

except sqlite3.Error as e:
    print(f"Database error: {e}")
    conn.rollback()
    raise

finally:
    conn.close()
