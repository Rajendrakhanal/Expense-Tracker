import uuid
from utils import hash_password, check_password

TIER_LIMITS = {
    "Tier1": 1000,
    "Tier2": 5000,
    "Tier3": 20000
}

class User:
    def __init__(self, id, username, password, tier, balance):
        self.id = id
        self.username = username
        self.password = password
        self.tier = tier
        self.balance = balance

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "tier": self.tier,
            "balance": self.balance
        }

    def authenticate(self, password):
        return check_password(password, self.password)

    def get_limit(self):
        return TIER_LIMITS[self.tier]

    def can_transact(self, amount):
        return amount <= self.balance and amount <= self.get_limit()

    def credit(self, amount):
        self.balance += amount

    def debit(self, amount):
        if self.can_transact(amount):
            self.balance -= amount
            return True
        return False
