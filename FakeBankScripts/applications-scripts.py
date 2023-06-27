import requests
import os
from dotenv import load_dotenv
load_dotenv()

UNDERWRITER_PORT = os.getenv("UNDERWRITER_PORT")
AUTH = os.getenv("AUTH_TOKEN")

app_type = {
    "1": "CHECKING",
    "2": "SAVINGS",
    "3": "CHECKING_AND_SAVINGS",
    "4": "CREDIT_CARD",
    "5": "LOAN"
}

app_status = {
    "1": "APPROVED",
    "2": "DENIED",
    "3": "PENDING"
}

response = requests.get(f"{UNDERWRITER_PORT}/applicants?size=30", headers={
                        "Authorization": f"{AUTH}"})

data = response.json()["content"]

applicants = []


for x in data:
    applicants.append(
        f'ID: {x["id"]}    First Name: {x["firstName"]}    Last Name: {x["lastName"]}')


print(app_type)
inputType = input("What type of account will this be? ")

print(app_status)
inputStatus = input("What is the status of this account? ")

for x in applicants:
    print(x)
inputApp = input(
    "Which applicants will be attached to this application? (Please enter their id(s) seperated by only a space) ").split()
inputApp = [int(i) for i in inputApp]

application = {}

application["applicationType"] = app_type[inputType]
application["applicantIds"] = inputApp
application["applicationStatus"] = app_status[inputStatus]

response = requests.post(f'{UNDERWRITER_PORT}/applications', json=application, headers={
    "Authorization": f"{AUTH}"})
print(response.json())
