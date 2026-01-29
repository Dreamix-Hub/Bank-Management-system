import json
import random

class Bank:
    accounts = {}
    transactions = []
    
    def __init__(self):
        with open('record.json', 'r') as f:
            Bank.accounts = json.load(f)
    
    # write to record.json
    @staticmethod
    def write_data(data):
        with open('record.json', 'w') as w_f:
            json.dump(data,w_f, indent=4) 
            
    # create account
    @classmethod
    def create_account(cls, name, account_type, balance):
        account_number = random.randint(1,100)
        # creating an account (use string keys for JSON consistency)
        cls.accounts.update({str(account_number): {"name": name, "account_type": account_type, "balance": balance}})
        # writing back to the json file
        cls.write_data(cls.accounts)
        return str(account_number)
               
    # delete an account
    def delete_account(self, account_number):
        key = str(account_number)
        if key in Bank.accounts:
            del Bank.accounts[key]
            self.write_data(Bank.accounts) # write back to the file
            print(f"Deleted account {key}")
        else:
            print(f"Account {account_number} not found")
    
    # get account
    @classmethod
    def get_account(cls, account_number):
        acc_num = str(account_number)
        if acc_num in cls.accounts:
            print(cls.accounts[acc_num])
        else:
            print(f"account {acc_num} not found")
    
    @classmethod
    def list_accounts(cls):
        for acc_num, details in cls.accounts.items():
            print("Account number:", acc_num)
            # printing other details
            for keys, value in details.items():
                print(f"{keys.upper()}: {value}")
            print()


