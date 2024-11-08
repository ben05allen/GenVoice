from app.schedules.bank_instructions import BankInstructions


def test_mock_bank_instructions():
    BankInstructions(
        bank_name="Mock Bank",
        branch_name="Main St",
        bank_code="1234",
        branch_code="012",
        swift_bic_code="MOCKBANK",
        recipient_type="Private",
        account_number="1234567890",
        account_type="Futsuu",
    )
