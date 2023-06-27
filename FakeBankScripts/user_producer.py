import requests
import os
from dotenv import load_dotenv
from random import randint, choice
from faker import Faker
from faker.providers import phone_number, date_time
fake = Faker()
fake.add_provider(phone_number)
fake.add_provider(date_time)
load_dotenv()

USER_PORT = os.getenv("USER_PORT")
AUTH = os.getenv("AUTH_TOKEN")
UNDERWRITER_PORT = os.getenv("UNDERWRITER_PORT")
BANK_PORT = os.getenv("BANK_PORT")

sc = ["@", "$", "!", "%", "*", "?", "&"]

roleOptions = {
    "1": "admin",
    "2": "member"
}

print(roleOptions)
roleInput = input("Would you like to create an admin or a member? ")
if roleOptions[roleInput] == "admin":
    userAmount = input("How many users would you like to create? ")
    role = "admin"

    for i in range(int(userAmount)):
        firstName = fake.first_name()
        lastName = fake.last_name()
        email = firstName + "." + lastName + "@email.com"
        username = firstName + "." + lastName
        password = firstName + lastName + \
            f"{randint(10,99)}" + choice(sc) + choice(sc)
        phone = fake.msisdn()[0:-3]
        phone = f'({phone[:3]}) {phone[3:6]}-{phone[6:]}'

        user = {}
        user["role"] = role
        user["username"] = username
        user["password"] = password
        user["email"] = email
        user["firstName"] = firstName
        user["lastName"] = lastName
        user["phone"] = phone

        print(user)
        response = requests.post(f'{USER_PORT}/users/registration', json=user, headers={
            "Authorization": f"{AUTH}"})
        print(response.json())
else:
    user = {}
    role = "member"
    members = requests.get(f'{BANK_PORT}/members', headers={
        "Authorization": f"{AUTH}"
    })
    memberIds = []
    for x in members.json()["content"]:
        member = {}
        member["membershipId"] = x["membershipId"]
        member["firstName"] = x["applicant"]["firstName"]
        member["lastName"] = x["applicant"]["lastName"]
        member["social"] = x["applicant"]["socialSecurity"]
        memberIds.append(member)
    for x in memberIds:
        print(x)
    user["role"] = role
    memberId = input("Please enter the applicants membershipId: ")
    index = [member for member in memberIds if member["membershipId"] == memberId]
    print(index)
    user["membershipId"] = index[0]["membershipId"]
    user["lastFourOfSSN"] = index[0]["social"][7:]
    user["username"] = f'{index[0]["firstName"]}.{index[0]["lastName"]}'
    user["password"] = index[0]["firstName"] + index[0]["lastName"] + \
        f'{randint(10,99)}' + choice(sc) + choice(sc)
    print(user)
    response = requests.post(f'{USER_PORT}/users/registration', json=user, headers={
        "Authorization": f"{AUTH}"})
    print(response.json())
