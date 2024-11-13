from jinja2 import Template

data = {
    "invoice_date": "2024-11-13",
    "invoice_number": "INV-001",
    "client_name": "John Doe",
    "client_address": "123 Main Street, Anytown, USA",
    "items": [
        {
            "name": "Item A",
            "description": "Description for Item A",
            "quantity": 2,
            "unit_price": 50,
        },
        {
            "name": "Item B",
            "description": "Description for Item B",
            "quantity": 1,
            "unit_price": 100,
        },
    ],
    "total": 200,
}

template = Template(open("invoice_template.html").read())
output = template.render(data)
