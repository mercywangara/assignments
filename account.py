from datetime import datetime

class Transaction:
    def __init__(self, date_time, narration, amount, transaction_type):
        self.date_time = date_time
        self.narration = narration
        self.amount = amount
        self.transaction_type = transaction_type

    def __str__(self):
        return f"{self.date_time} | {self.transaction_type.capitalize()} | {self.narration}: {self.amount}"

class Account:
    minimum_balance = 0  

    def __init__(self, owner, account_number=None):
        self.owner = owner
        self.__balance = 0               
        self.__account_number = account_number  
        self.transactions = []
        self.loan = 0
        self.frozen = False
        self.minimum_balance = self.__class__.minimum_balance
        self.closed = False

    def deposit(self, amount, narration="Deposit"):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if amount <= 0:
            return "Deposit must be positive."
        self.__balance += amount
        transact = Transaction(datetime.now(), narration, amount, "deposit")
        self.transactions.append(transact)
        return f"Deposited {amount}. Balance: {self.__balance}"

    def withdraw(self, amount, narration="Withdrawal"):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if amount <= 0:
            return "Withdrawal must be positive."
        if self.__balance - amount < self.minimum_balance:
            return "Not enough balance for minimum requirement."
        if amount > self.__balance:
            return "Not enough balance."
        self.__balance -= amount
        transact = Transaction(datetime.now(), narration, amount, "withdrawal")
        self.transactions.append(transact)
        return f"Withdrew {amount}. Balance: {self.__balance}"

    def transfer(self, target_account, amount, narration="Transfer"):
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
        if self.__balance - amount < self.minimum_balance:
            return "Not enough balance for minimum requirement."
        if amount > self.__balance:
            return "Not enough balance."
        self.withdraw(amount, f"Transfer to {target_account.owner}")
        target_account.deposit(amount, f"Transfer from {self.owner}")
        return f"Transferred {amount} to {target_account.owner}. Balance: {self.__balance}"

    def get_balance(self):
        balance = 0
        for transact in self.transactions:
            if transact.transaction_type == "deposit" or transact.transaction_type == "loan" or transact.transaction_type == "interest":
                balance += transact.amount
            elif transact.transaction_type == "withdrawal" or transact.transaction_type == "repay_loan":
                balance -= transact.amount
        return balance

    def get_balance_direct(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def request_loan(self, amount, narration="Loan"):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if amount <= 0:
            return "Loan must be positive."
        self.loan += amount
        self.__balance += amount
        transact = Transaction(datetime.now(), narration, amount, "loan")
        self.transactions.append(transact)
        return f"Loan {amount} added. Balance: {self.__balance}"

    def repay_loan(self, amount, narration="Repay Loan"):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        if self.loan == 0:
            return "No loan to repay."
        if amount <= 0:
            return "Repay must be positive."
        pay = min(self.loan, amount)
        if self.__balance < pay:
            return "Not enough balance to repay."
        self.__balance -= pay
        self.loan -= pay
        transact = Transaction(datetime.now(), narration, pay, "repay_loan")
        self.transactions.append(transact)
        return f"Repaid {pay}. Remaining loan: {self.loan}"

    def show_details(self):
        return f"Owner: {self.owner}, Balance: {self.__balance}"

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
        for transact in self.transactions:
            lines.append(str(transact))
        lines.append(f"Current balance: {self.__balance}")
        return "\n".join(lines)

    def add_interest(self, narration="Interest"):
        if self.closed:
            return "Account closed."
        if self.frozen:
            return "Account frozen."
        interest = self.__balance * 0.05
        self.__balance += interest
        transact = Transaction(datetime.now(), narration, interest, "interest")
        self.transactions.append(transact)
        return f"Added interest: {interest}. Balance: {self.__balance}"

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
        self.__balance = 0
        self.transactions = []
        self.loan = 0
        self.closed = True
        return "Account closed. Balance and transactions cleared."