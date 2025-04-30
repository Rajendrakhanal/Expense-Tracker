import uuid
import datetime
from models import User
from utils import load_data, save_data, hash_password

DATA_FILE = "wallet.json"

class WalletService:
    def __init__(self):
        self.data = load_data(DATA_FILE)

    def save(self):
        save_data(DATA_FILE, self.data)

    def register_user(self):
        username = input("Username: ")
        if any(u["username"] == username for u in self.data["users"]):
            print("Username already exists.")
            return

        password = input("Password: ")
        tier = input("Tier (Tier1/Tier2/Tier3): ")
        if tier not in ["Tier1", "Tier2", "Tier3"]:
            print("Invalid tier.")
            return

        user = User(
            id=str(uuid.uuid4()),
            username=username,
            password=hash_password(password),
            tier=tier,
            balance=0.0
        )
        self.data["users"].append(user.to_dict())
        self.save()
        print("Registration successful.")

    def login_user(self):
        username = input("Username: ")
        password = input("Password: ")
        user_dict = next((u for u in self.data["users"] if u["username"] == username), None)
        if user_dict is None:
            print("User not found.")
            return None

        user = User.from_dict(user_dict)
        if user.authenticate(password):
            print(f"Welcome {user.username} ({user.tier})")
            return user
        else:
            print("Invalid credentials.")
            return None

    def update_user(self, user: User):
        for i, u in enumerate(self.data["users"]):
            if u["id"] == user.id:
                self.data["users"][i] = user.to_dict()
                self.save()
                break

    def find_user_by_username(self, username):
        user_dict = next((u for u in self.data["users"] if u["username"] == username), None)
        return User.from_dict(user_dict) if user_dict else None

    def record_transaction(self, sender_id, receiver_id, tx_type, amount):
        tx = {
            "id": str(uuid.uuid4()),
            "sender": sender_id,
            "receiver": receiver_id,
            "type": tx_type,
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.data["transactions"].append(tx)
        self.save()

    def peer_transfer(self, sender: User):
        recipient_name = input("Recipient username: ")
        recipient = self.find_user_by_username(recipient_name)
        if not recipient:
            print("Recipient not found.")
            return

        amount = float(input("Amount: "))
        if sender.debit(amount):
            recipient.credit(amount)
            self.update_user(sender)
            self.update_user(recipient)
            self.record_transaction(sender.id, recipient.id, "P2P", amount)
            print("Transfer successful.")
        else:
            print("Transfer failed due to insufficient balance or limit.")

    def pay_merchant(self, sender: User):
        merchant = input("Merchant name: ")
        amount = float(input("Amount: "))
        if sender.debit(amount):
            self.update_user(sender)
            self.record_transaction(sender.id, "MERCHANT", "MerchantPayment", amount)
            print(f"Paid {merchant} successfully.")
        else:
            print("Payment failed.")

    def mobile_topup(self, sender: User):
        mobile = input("Mobile number: ")
        amount = float(input("Top-up amount: "))
        if sender.debit(amount):
            self.update_user(sender)
            self.record_transaction(sender.id, "MOBILE", "TopUp", amount)
            print(f"Top-up successful to {mobile}.")
        else:
            print("Top-up failed.")
