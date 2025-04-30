from services import WalletService

def main():
    wallet = WalletService()
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            wallet.register_user()
        elif choice == "2":
            user = wallet.login_user()
            if user:
                user_menu(wallet, user)
        elif choice == "3":
            break
        else:
            print("Invalid choice")

def user_menu(wallet, user):
    while True:
        print("\n1. Balance\n2. Add Money\n3. Transfer\n4. Pay Merchant\n5. Mobile Top-up\n6. Logout")
        choice = input("Choose: ")
        if choice == "1":
            print(f"Balance: ${user.balance}")
        elif choice == "2":
            amount = float(input("Amount to add: "))
            user.credit(amount)
            wallet.update_user(user)
            print("Money added.")
        elif choice == "3":
            wallet.peer_transfer(user)
        elif choice == "4":
            wallet.pay_merchant(user)
        elif choice == "5":
            wallet.mobile_topup(user)
        elif choice == "6":
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()
