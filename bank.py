import json
import random


class Bank:
    accounts = {}
    transactions = []
    
    def __init__(self):
        with open('record.json', 'r') as f:
            Bank.accounts = json.load(f)
            
    # create account
    def create_account(self, name, account_type, initial_balance):
        self.name = name
        self.account_type = account_type
        self.initial_balance = initial_balance
        self.account_number = random.randint(1,100)
        
        Bank.accounts.update({self.account_number: {"name": self.name, "account_type": self.account_type, "initial_balance":self.initial_balance}})    
        
        with open('record.json', 'w') as w_f:
            json.dump(Bank.accounts,w_f, indent=4)    
            
    @classmethod
    def print_account(cls):
        print(cls.accounts)
    
        

bnk_1 = Bank()
bnk_1.create_account('abdullah','current', 1000)
bnk_1.print_account()