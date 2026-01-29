from bank import Bank
from transaction import Transaction

class Account(Bank, Transaction):

    def __init__(self, account_number):
        acc = Bank.accounts.get(str(account_number))
        if not acc:
            raise ValueError(f"Account {account_number} not found")
        self.holder_name = acc.get('name')
        self.acc_type = acc.get('account_type')
        self.acc_num = str(account_number)
        self.__balance = acc.get('balance', 0) # private balance

    @property
    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            acc = Bank.accounts.get(self.acc_num) # fetching the account 
            acc['balance'] = self.__balance
            Bank.write_data(Bank.accounts)
            Transaction(self.acc_num, 'deposit', amount)
            print(f"{amount} Deposited")
        else:
            print("Invalid amount!")
    
    def withdraw(self, amount):
        if amount > 0:
            self.__balance -= amount
            acc = Bank.accounts.get(self.acc_num)
            acc['balance'] = self.__balance
            Bank.write_data(Bank.accounts)
            Transaction(self.acc_num, 'withdraw', amount)
            print(f"{amount} withdraw")
        else:
            print("Invalid amount!")

    def get_details(self):
        print("Account number:", self.acc_num)
        print("Holder name:", self.holder_name)
        print("Account type:", self.acc_type)
        print("Balance:", self.get_balance, '\n')


# Create account (returns the account number as string),
# then instantiate `Account` to access instance methods.
# acct_1 = Account.create_account('bob', 'current', 20)
# acct_2 = Account.create_account('alice', 'saving', 100)
# customer_1 = Account(acct_1)
# customer_2 = Account(acct_2)

# # print(customer_2.get_balance)


# # customer_1.get_details()
# customer_1.deposit(100)
# # customer_1.get_details()
# customer_1.withdraw(10)
# # customer_1.get_details()

# customer_1.get_transaction_details()