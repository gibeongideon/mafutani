from django.db import IntegrityError

class InsufficientTokens(IntegrityError):
    """Raised when a wallet has insufficient tokens to
    run an operation.

    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """
        
class NegativeBalance(Exception):
    pass


class NotEnoughBalance(Exception):
    pass    


class NegativeTokens(Exception):
    pass
