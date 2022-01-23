import random
from .models import UserOTPTable


def create_otp():
    return random.randint(1000, 9999)


def validate_otp(phone_number, otp):
    user_otp_info = UserOTPTable.objects.filter(
        phone__iexact=phone_number).first()
    if user_otp_info:
        user_otp = str(user_otp_info.otp)
        if user_otp == str(otp):
            user_otp_info.delete()
            return True
    return False


def send_otp_to_user(phone_number, otp):
    res = {'Status': 'Success', 'Details': 1}
    return res
