from django.utils import timezone
import random
import os
from twilio.rest import Client
class Authentication():

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp(phone_number):
        otp = Authentication.generate_otp()
        # self.otp = otp
        # self.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

        # todo: dotenv# #done
        account_sid = os.getenv('account_sid')
        auth_token = os.getenv('auth_token')
        twilio_phone_number = os.getenv('twilio_phone_number')

        dist_phone_number = phone_number.replace("0", "+98", 1)

        client = Client(account_sid, auth_token)
        print("Phone Number:", dist_phone_number)
        message = client.messages.create(
            body=f'Your code is: {otp}',
            from_=twilio_phone_number,
            to=dist_phone_number
        )

        print("Twilio Response:", message)
        return otp, otp_expiry

    @staticmethod
    def check_otp(otp, otp_expiry, entered_otp):
        return otp == entered_otp and timezone.now() < otp_expiry
