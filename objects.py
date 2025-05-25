class Account:
    def __init__(self, owner, minimum_balance=0):
        self.owner = owner
        self.transactions = []
        self.balance = 0
        self.loan = 0
        self.frozen = False
        self.minimum_balance = minimum_balance
        self.closed = False

    def deposit(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Deposit amount must be positive."
        self.transactions.append({'type': 'deposit', 'amount': amount})
        self.balance += amount
        return f"Deposit successful. New balance: {self.balance}"

    def withdraw(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.balance - amount < self.minimum_balance:
            return "Cannot withdraw: minimum balance requirement not met."
        if amount > self.balance:
            return "Insufficient funds."
        self.transactions.append({'type': 'withdrawal', 'amount': amount})
        self.balance -= amount
        return f"Withdrawal successful. New balance: {self.balance}"

    def transfer_funds(self, target_account, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if target_account.closed:
            return "Target account is closed."
        if target_account.frozen:
            return "Target account is frozen."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.balance - amount < self.minimum_balance:
            return "Cannot transfer: minimum balance requirement not met."
        if amount > self.balance:
            return "Insufficient funds."
        self.withdraw(amount)
        target_account.deposit(amount)
        return f"Transferred {amount} to {target_account.owner}. Your new balance: {self.balance}"

    def get_balance(self):
        return self.balance

    def request_loan(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Loan amount must be positive."
        self.loan += amount
        self.transactions.append({'type': 'loan', 'amount': amount})
        self.balance += amount
        return f"Loan of {amount} approved. New balance: {self.balance}"

    def repay_loan(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Repayment amount must be positive."
        if self.loan == 0:
            return "No loan to repay."
        repay_amount = min(amount, self.loan)
        if self.balance < repay_amount:
            return "Insufficient funds to repay loan."
        self.balance -= repay_amount
        self.loan -= repay_amount
        self.transactions.append({'type': 'repay_loan', 'amount': repay_amount})
        return f"Repayment of {repay_amount} successful. Remaining loan: {self.loan}"

    def view_account_details(self):
        return f"Owner: {self.owner}, Balance: {self.balance}"

    def change_account_owner(self, new_owner):
        if self.closed:
            return "Account is closed."
        if not new_owner:
            return "New owner name cannot be empty."
        old_owner = self.owner
        self.owner = new_owner
        return f"Account owner changed from {old_owner} to {self.owner}."

    def account_statement(self):
        if not self.transactions:
            return "No transactions found."
        statement = f"Account Statement for {self.owner}:\n"
        for t in self.transactions:
            statement += f"{t['type'].capitalize()}: {t['amount']}\n"
        statement += f"Current Balance: {self.balance}\n"
        return statement

    def apply_interest(self):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        interest = self.balance * 0.05
        self.balance += interest
        self.transactions.append({'type': 'interest', 'amount': interest})
        return f"Interest applied: {interest}. New balance: {self.balance}"

    def freeze_account(self):
        self.frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.minimum_balance = amount
        return f"Minimum balance set to {self.minimum_balance}"

    def close_account(self):
        self.balance = 0
        self.transactions.clear()
        self.loan = 0
        self.closed = True
        return "Account has been closed. All balances set to zero and transactions cleared."