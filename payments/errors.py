from django.db import IntegrityError


class InsufficientBalance(IntegrityError):
    """
    Raised when a wallet has insufficient balance to
    run an operation.

    """