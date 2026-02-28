"""Different Validators for string checking."""

import ipaddress

from email_validator import EmailNotValidError, validate_email
from textual.validation import ValidationResult, Validator


class IPv4Validator(Validator):
    """Checks if given string is a valid IPv4 address."""

    def validate(self, value: str) -> ValidationResult:
        if self.is_ipv4(value):
            return self.success()
        else:
            return self.failure("Not an IPv4 address.")

    @staticmethod
    def is_ipv4(value: str) -> bool:
        """Checks if given string is a valid IPv4 address."""
        try:
            ipaddress.IPv4Address(value)
            return True
        except ValueError:
            return False


class IPv6Validator(Validator):
    """Checks if given string is a valid IPv6 address."""

    def validate(self, value: str) -> ValidationResult:
        if self.is_ipv6(value):
            return self.success()
        else:
            return self.failure("Not an IPv6 address.")

    @staticmethod
    def is_ipv6(value: str) -> bool:
        """Checks if given string is a valid IPv6 address."""
        try:
            ipaddress.IPv6Address(value)
            return True
        except ValueError:
            return False


class EMailValidator(Validator):
    """Uses email-validator package to check if a string is a valid email address."""

    def __init__(self, check_deliverability: bool = False):
        super().__init__()
        self.check_deliverability = check_deliverability
        self.failure_description = "Not a valid email address"

    def validate(self, value: str) -> ValidationResult:
        if self.is_email(value, check_deliverability=self.check_deliverability):
            return self.success()
        else:
            return self.failure(self.failure_description)

    def is_email(self, value: str, check_deliverability: bool = False) -> bool:
        """Checks if given string is a valid email address."""
        try:
            validate_email(value, check_deliverability=check_deliverability)
            return True
        except EmailNotValidError as e:
            self.failure_description = str(e)
            return False
