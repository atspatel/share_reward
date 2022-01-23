from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from password_generator import PasswordGenerator

from .models import User, UserOTPTable
from .otp_utils import create_otp, send_otp_to_user, validate_otp

pwo = PasswordGenerator()


class TokenView(APIView):
    def get(self, request, token=None):
        if token:
            token_obj = Token.objects.filter(key=token).first()
            if token_obj:
                return Response({"status": True, "is_valid": True}, status=status.HTTP_200_OK)
            return Response({"status": True, "is_valid": False}, status=status.HTTP_200_OK)
        return Response({"status": False, "message": "token not given"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PhoneNumberView(APIView):
    def get(self, request, phone_number=None):
        if phone_number:
            user_obj = User.objects.filter(phone=phone_number).first()
            if user_obj:
                return Response({'isRegistered': True, "status": True}, status=status.HTTP_200_OK)
            return Response({'isRegistered': False, "status": True}, status=status.HTTP_200_OK)
        return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)


class OTPView(APIView):
    def get(self, request, phone_number=None):
        if phone_number:
            otp = create_otp()
            userOtp_obj, _ = UserOTPTable.objects.get_or_create(
                phone=phone_number, defaults={'otp': otp})
            otp = userOtp_obj.otp
            sent_response = send_otp_to_user(phone_number, otp)
            if sent_response['Status'] == "Success":
                return Response({"status": True, "message": "OTP Sent Successfully"}, status=status.HTTP_200_OK)
            return Response({"status": False, "message": "Error in Sending OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"status": False,  "message": "Phone Number not given"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def verify_otp(phone_number, otp):
        return validate_otp(phone_number, otp)


class LogInView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        data = request.data
        phone = data.get('phone', None)
        otp = data.get('otp', None)

        if phone and otp:
            if OTPView.verify_otp(phone, otp):
                user_obj = User.objects.get(phone=phone)
                token, created = Token.objects.get_or_create(user=user_obj)
                return Response({'status': True,
                                 'token': token.key,
                                 'message': 'Logged In Successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Invalid Phone or OTP '},
                                status=status.HTTP_200_OK)
        return Response({'status': False, 'message': 'Missing Phone or OTP in input'},
                        status=status.HTTP_400_BAD_REQUEST)


# class SignUpView(APIView):
#     def get(self, request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     def post(self, request):
#         data = request.data
#         phone = data.get('phone', None)
#         otp = data.get('otp', None)
#         first_name = data.get('first_name', None)

#         if phone and otp and first_name:
#             if OTPView.verify_otp(phone, otp):
#                 user_obj, created = User.objects.get_or_create(phone=phone,
#                                                                defaults={
#                                                                    "first_name": first_name,
#                                                                    "is_verified": True})
#                 if created:
#                     password = pwo.generate()
#                     user_obj.set_password(password)
#                     user_obj.save()

#                     token, _ = Token.objects.get_or_create(user=user_obj)
#                     return Response({'status': True,
#                                      'token': token.key,
#                                      'message': 'Signed Up Successfully'},
#                                     status=status.HTTP_200_OK)
#                 else:
#                     return Response({'status': False,
#                                      'message': 'User Already Exist. Log In using same number'},
#                                     status=status.HTTP_200_OK)
#             else:
#                 return Response({'status': False, 'message': 'Invalid Phone or OTP '},
#                                 status=status.HTTP_200_OK)
#         return Response({'status': False, 'message': 'Missing Phone or OTP or First Name in input'},
#                         status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user.auth_token.delete()
        return Response({
            'status': True,
            'message': 'Logged Out Successfully'
        })

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
