import datetime
from bank import Bank

class Transaction:
    temp = 0
    def __init__(self,acc_number, trans_type, amount):
        self.trans_id = Transaction.temp + 1
        Transaction.temp = self.trans_id
        self.acc_num = acc_number
        self.tran_type = trans_type 
        self.amount = amount
        self.date_time = datetime.datetime.now()
        Bank.transactions.append({"trans_id":self.trans_id,"account_num": self.acc_num, "trans_type":self.tran_type,"amount": self.amount,"time": str(self.date_time)})
        
    def get_transaction_details(self):
        print("Transaction detail of account:", self.acc_num)
        print(Bank.transactions)

