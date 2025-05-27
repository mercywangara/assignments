class Account:
    minimum_balance = 0  

    def __init__(self, owner):
        self.owner = owner
        self.balance = 0
        self.transactions = []
        self.loan = 0
        self.frozen = False
        self.minimum_balance = self.__class__.minimum_balance
        self.closed = False

    def deposit(self, amount):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if amount <= 0:
            return "Deposit must be positive."
        self.balance += amount
        self.transactions.append(("deposit", amount))
        return f"Deposited {amount}. Balance: {self.balance}"

    def withdraw(self, amount):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if amount <= 0:
            return "Withdrawal must be positive."
        if self.balance - amount < self.minimum_balance:
            return "Not enough balance for minimum requirement."
        if amount > self.balance:
            return "Not enough balance."
        self.balance -= amount
        self.transactions.append(("withdrawal", amount))
        return f"Withdrew {amount}. Balance: {self.balance}"

    def transfer(self, target_account, amount):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if target_account.closed:
            return "Target account closed."
        if target_account.frozen:
            return "Target account frozen."
        if amount <= 0:
            return "Transfer must be positive."
        if self.balance - amount < self.minimum_balance:
            return "Not enough balance for minimum requirement."
        if amount > self.balance:
            return "Not enough balance."
        self.withdraw(amount)
        target_account.deposit(amount)
        return f"Transferred {amount} to {target_account.owner}. Balance: {self.balance}"

    def get_balance(self):
        return self.balance

    def request_loan(self, amount):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if amount <= 0:
            return "Loan must be positive."
        self.loan += amount
        self.balance += amount
        self.transactions.append(("loan", amount))
        return f"Loan {amount} added. Balance: {self.balance}"

    def repay_loan(self, amount):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if self.loan == 0:
            return "No loan to repay."
        if amount <= 0:
            return "Repay must be positive."
        pay = min(self.loan, amount)
        if self.balance < pay:
            return "Not enough balance to repay."
        self.balance -= pay
        self.loan -= pay
        self.transactions.append(("repay_loan", pay))
        return f"Repaid {pay}. Remaining loan: {self.loan}"

    def show_details(self):
        return f"Owner: {self.owner}, Balance: {self.balance}"

    def change_owner(self, new_owner):
        if self.closed:
            return "Account closed."
        if not new_owner:
            return "Owner name needed."
        old_owner = self.owner
        self.owner = new_owner
        return f"Owner changed from {old_owner} to {self.owner}."

    def statement(self):
        if not self.transactions:
            return "No transactions."
        lines = [f"Statement for {self.owner}:"]
        for t in self.transactions:
            lines.append(f"{t[0].capitalize()}: {t[1]}")
        lines.append(f"Current balance: {self.balance}")
        return "\n".join(lines)

    def add_interest(self):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        interest = self.balance * 0.05
        self.balance += interest
        self.transactions.append(("interest", interest))
        return f"Added interest: {interest}. Balance: {self.balance}"

    def freeze(self):
        self.frozen = True
        return "Account frozen."

    def unfreeze(self):
        self.frozen = False
        return "Account unfrozen."

    def set_minimum(self, amount):
        if amount < 0:
            return "Minimum cannot be negative."
        self.minimum_balance = amount
        return f"Minimum balance: {self.minimum_balance}"

    def close(self):
        self.balance = 0
        self.transactions = []
        self.loan = 0
        self.closed = True
        return "Account closed. Balance and transactions cleared."