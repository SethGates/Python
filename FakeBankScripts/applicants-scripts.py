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

UNDERWRITER_PORT = os.getenv("UNDERWRITER_PORT")
AUTH = os.getenv("AUTH_TOKEN")

genders = ["MALE", "FEMALE"]

app_input = input("How many applicants would you like to create? ")

for i in range(int(app_input)):
    applicant = {}
    gender = choice(genders)
    if gender == "MALE":
        firstName = fake.first_name_male()
    else:
        firstName = fake.first_name_female()
    lastName = fake.last_name()
    address = fake.street_address()
    city = fake.city()
    state = fake.state()
    zipcode = fake.zipcode()
    ssn = fake.ssn()
    phone = fake.msisdn()[0:-3]
    phone = f'({phone[:3]}) {phone[3:6]}-{phone[6:]}'
    Dl = f'DL{randint(100000, 999999)}'
    DoB = fake.date_of_birth(None, 18, 80)
    income = int(f'{randint(2000,3000)}000')
    applicant["mailingAddress"] = address
    applicant["mailingCity"] = city
    applicant["mailingState"] = state
    applicant["mailingZipcode"] = zipcode
    applicant["socialSecurity"] = ssn
    applicant["email"] = firstName + "." + lastName + "@email.com"
    applicant["income"] = income
    applicant["firstName"] = firstName
    applicant["lastName"] = lastName
    applicant["gender"] = gender
    applicant["driversLicense"] = Dl
    applicant["dateOfBirth"] = str(DoB)
    applicant["address"] = address
    applicant["city"] = city
    applicant["state"] = state
    applicant["zipcode"] = zipcode
    applicant["phone"] = phone
    response = requests.post(f'{UNDERWRITER_PORT}/applicants', json=applicant, headers={
                             "Authorization": f"{AUTH}"})
    print(response.json())
