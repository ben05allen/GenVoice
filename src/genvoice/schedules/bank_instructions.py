# pyright: basic

from enum import StrEnum
from pydantic import AliasChoices, Field

from genvoice.schedules import Base


class ReceipientTypeEnum(StrEnum):
    PRIVATE = "Private"
    BUSINESS = "Business"


class AccountTypeEnum(StrEnum):
    GENERAL = "General/Futsuu"
    FUTSUU = "Futsuu"


class BankInstructions(Base):
    bank_name: str
    branch: str
    bank_code: str
    branch_code: str | None = None
    swift_bic_code: str = Field(
        validation_alias=AliasChoices(
            "swift_bic_code",
            "bic",
        )
    )
    recipient_type: ReceipientTypeEnum
    account_number: str = Field(
        validation_alias=AliasChoices(
            "account_number",
            "account",
        )
    )
    account_type: AccountTypeEnum
