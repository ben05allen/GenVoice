from enum import StrEnum

from . import BaseModel


class ReceipientTypeEnum(StrEnum):
    PRIVATE = "Private"
    BUSINESS = "Business"


class AccountTypeEnum(StrEnum):
    GENERAL = "General/Futsuu"
    FUTSUU = "Futsuu"


class BankInstructions(BaseModel):
    bank_name: str
    branch_name: str
    branch_code: str | None = None
    swift_bic_code: str
    recipient_type: ReceipientTypeEnum
    bank_code: str
    account_number: str
    account_type: AccountTypeEnum