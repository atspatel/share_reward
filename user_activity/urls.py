from django.urls import path

from .views import UserLikeView, UserShareView, RewardValueView

urlpatterns = [
    path('like/', UserLikeView.as_view(), name="post_like"),
    path('like/<article_id>', UserLikeView.as_view(), name="get_like"),


    path('share/', UserShareView.as_view(), name="share"),
    path('share/<share_id>', UserShareView.as_view(), name="share"),

    path('reward_value/<article_id>',
         RewardValueView.as_view(), name="reward_value")

]
