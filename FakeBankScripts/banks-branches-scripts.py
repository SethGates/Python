import requests
import os
from dotenv import load_dotenv
from faker import Faker
from faker.providers import bank
fake = Faker()
fake.add_provider(bank)
load_dotenv()

BANK_PORT = os.getenv("BANK_PORT")
AUTH = os.getenv("AUTH_TOKEN")

bankinput = input("How many banks do you want to create? ")


for i in range(int(bankinput)):
    banks = {}
    address = fake.street_address()
    city = fake.city()
    state = fake.state()
    zipcode = fake.zipcode()
    routing = fake.aba()
    banks["address"] = address
    banks["city"] = city
    banks["state"] = state
    banks["zipcode"] = zipcode
    banks["routingNumber"] = routing
    bankResponse = requests.post(f'{BANK_PORT}/banks', json=banks, headers={
        "Authorization": f"{AUTH}"})
    bankId = bankResponse.json()["id"]
    print(bankResponse.json())
    branchinput = input(
        "How many branches do you want to create for this bank? ")
    for j in range(int(branchinput)):
        branch = {}
        phone = fake.msisdn()[0:-3]
        phone = f'({phone[:3]}) {phone[3:6]}-{phone[6:]}'
        if j == 0:
            name = 'Main Branch'
            branch["name"] = name
            branch["address"] = address
            branch["city"] = city
            branch["state"] = state
            branch["zipcode"] = zipcode
            branch["bankID"] = bankId
            branch["phone"] = phone
            response = requests.post(f'{BANK_PORT}/branches', json=branch, headers={
                "Authorization": f"{AUTH}"})
            print(response.json())

        else:
            branchstreet = fake.street_address()
            branchname = ''.join([i for i in branchstreet
                                  if not i.isdigit()]).strip() + " Branch"
            branch["address"] = branchstreet
            branch["name"] = branchname
            branch["city"] = city
            branch["state"] = state
            branch["zipcode"] = zipcode
            branch["bankID"] = bankId
            branch["phone"] = phone
            response = requests.post(f'{BANK_PORT}/branches', json=branch, headers={
                "Authorization": f"{AUTH}"})
            print(response.json())
