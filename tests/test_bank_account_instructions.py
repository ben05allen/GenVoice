import pytest

from genvoice.schedules.bank_instructions import BankInstructions


def test_mock_bank_instructions():
    bank_instructions = BankInstructions(
        bank_name="Mock Bank",
        branch="Main St",
        bank_code="1234",
        branch_code="012",
        swift_bic_code="MOCKBANK",
        recipient_type="Private",  # type: ignore
        account_number="1234567890",
        account_type="Futsuu",  # type: ignore
    )

    assert bank_instructions.bank_name == "Mock Bank"


def test_missing_account_number():
    with pytest.raises(ValueError):
        BankInstructions(
            bank_name="Mock Bank",
            branch="Main St",
            bank_code="1234",
            branch_code="012",
            swift_bic_code="MOCKBANK",
            recipient_type="Private",  # type: ignore
            # account_number="1234567890",
            account_type="Futsuu",  # type: ignore
        )
