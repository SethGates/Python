import requests
import os
import random
from dotenv import load_dotenv
load_dotenv()

TRANSACTION_PORT = os.getenv("TRANSACTION_PORT")
ACCOUNT_PORT = os.getenv("ACCOUNT_PORT")
AUTH = os.getenv("AUTH_TOKEN")

transactionMethods = ["ACH", "ATM", "CREDIT_CARD", "DEBIT_CARD", "APP"]
transactionState = ["CREATED", "PROCESSING", "POSTED"]
transactionType = ["DEPOSIT", "WITHDRAWAL", "TRANSFER_IN",
                   "TRANSFER_OUT", "PURCHASE", "PAYMENT", "REFUND", "VOID"]
transactionStatus = ["APPROVED", "DENIED", "PENDING"]

trans_amount = input("How many transactions would you like to create? ")
account_response = requests.get(f'{ACCOUNT_PORT}/accounts', headers={
    "Authorization": f"{AUTH}"
})

accounts = []

for x in account_response.json()['content']:
    account = {}
    account["accountNumber"] = x["accountNumber"]
    account["balance"] = x["balance"]
    accounts.append(account)

for x in accounts:
    print(x)

for i in range(int(trans_amount)):
    transaction = {}
    transaction["method"] = random.choice(transactionMethods)
    transaction["state"] = random.choice(transactionState)
    transaction["type"] = random.choice(transactionType)
    transaction["status"] = random.choice(transactionStatus)
    transaction["merchantCode"] = "NONE"
    amount = int(input("What is the amount of this transaction? "))
    transaction["amount"] = amount
    account = input(
        "What is the account number associated with the transaction? ")
    transaction["accountNumber"] = account
    respone = requests.post(f'{TRANSACTION_PORT}/transactions', json=transaction, headers={
        "Authorization": f"{AUTH}"
    })
    print(respone.json())
