from dataclasses import field
from rest_framework import serializers

from accounts.models import User
from .models import UserLikeTable, UserShareTable, ConnectionRewardValue

from content_ops.serializers import ArticleDataSerializer
from accounts.serializers import UserSerializer

rev_status_mapping = {
    0: 'shared',
    1: 'opened'
}


class UserLikeSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserLikeTable
        fields = ('article_id', 'like_count', 'is_liked')

    def get_article_id(self, obj):
        return obj.id

    def get_like_count(self, obj):
        return UserLikeTable.objects.filter(article=obj).count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return bool(UserLikeTable.objects.filter(article=obj, user=user).count())
        return False


class UserShareSerializer(serializers.ModelSerializer):
    article_info = ArticleDataSerializer(source='article', read_only=True)
    shared_by = serializers.SerializerMethodField(read_only=True)
    shared_with = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserShareTable
        fields = ('id', 'article_info', 'shared_by',
                  'shared_with', 'reward_earned', 'status')

    def get_shared_by(self, obj):
        return UserSerializer(obj.connection.user_a).data

    def get_shared_with(self, obj):
        return UserSerializer(obj.connection.user_b).data

    def get_status(self, obj):
        return rev_status_mapping.get(obj.status, 'shared')


class UserRewardSerializer(serializers.ModelSerializer):
    shared_with = serializers.SerializerMethodField(read_only=True)
    max_reward = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConnectionRewardValue
        fields = ('shared_with', 'max_reward')

    def get_shared_with(self, obj):
        user_id = obj['connection__user_b']
        user_obj = User.objects.filter(id=user_id).first()
        return UserSerializer(user_obj).data

    def get_max_reward(self, obj):
        return obj['max_reward']
