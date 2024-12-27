class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.account = []

    def add_account(self, account):
        self.account.append(account)

    def get_total_balance(self):
        return sum(account.get_balance() for account in self.account)