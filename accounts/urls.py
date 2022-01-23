from django.urls import path


from .views import LogInView, LogOutView
from .views import PhoneNumberView, OTPView,  TokenView

urlpatterns = [
    path('check_phone/<phone_number>', PhoneNumberView.as_view(),
         name="check_user_exists"),
    path('send_otp/<phone_number>', OTPView.as_view(),
         name="send OTP on number"),

    path('login/', LogInView.as_view(), name="login"),
    path('logout', LogOutView.as_view(), name="logout"),

    path('validate_token/<token>', TokenView.as_view(), name="validate token"),

    # path('signup/', SignUpView.as_view(), name="signup"),
]
