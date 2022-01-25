from django.db.models import Q, F, Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from content_ops.models import ArticleData
from accounts.models import User
from .models import UserLikeTable, ConnectionTable, UserShareTable, ConnectionRewardValue
from .serializers import UserLikeSerializer, UserShareSerializer, UserRewardSerializer


class UserLikeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, article_id=None):
        if article_id:
            article_obj = ArticleData.objects.filter(id=article_id).first()
            serializer = UserLikeSerializer(
                article_obj, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "please provide article id"})

    def post(self, request):
        article_id = request.data.get('article_id', None)
        if article_id:
            article_obj = ArticleData.objects.filter(id=article_id).first()
            if article_obj:
                user_obj = request.user
                like_obj = UserLikeTable.objects.filter(
                    article=article_obj, user=user_obj).first()
                if like_obj:
                    like_obj.delete()
                else:
                    like_obj = UserLikeTable.objects.create(
                        article=article_obj, user=user_obj)
                return self.get(request, article_id)
            else:
                return Response({
                    "success": False,
                    "message": "Article id not valid"})
        else:
            return Response({
                "success": False,
                "message": "Article id not provided"})


class UserShareView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def create_share_obj(connection_obj, article_obj, reward_earned=1):
        user_share_obj, created = UserShareTable.objects.get_or_create(connection=connection_obj,
                                                                       article=article_obj,
                                                                       defaults={"reward_earned": reward_earned})
        if created:
            categories = article_obj.categories.all()
            for category_obj in categories:
                reward_obj, _ = ConnectionRewardValue.objects.get_or_create(
                    connection=connection_obj, category=category_obj)
                reward_obj.article_shared = reward_obj.article_shared + 1
                reward_obj.save()
        return user_share_obj

    @staticmethod
    def update_share_obj(share_obj):
        if share_obj.status == 0:
            connection_obj = share_obj.connection
            article_obj = share_obj.article
            categories = article_obj.categories.all()
            for category_obj in categories:
                reward_obj, _ = ConnectionRewardValue.objects.get_or_create(
                    connection=connection_obj, category=category_obj)
                reward_obj.article_opened = reward_obj.article_opened + 1
                reward_obj.save()
        share_obj.status = 1
        share_obj.save()
        return share_obj

    @staticmethod
    def delete_share_obj(share_obj):
        connection_obj = share_obj.connection
        article_obj = share_obj.article
        categories = article_obj.categories.all()
        for category_obj in categories:
            reward_obj, _ = ConnectionRewardValue.objects.get_or_create(
                connection=connection_obj, category=category_obj)
            reward_obj.article_shared = max(reward_obj.article_shared - 1, 0)
            reward_obj.save()

        share_obj.delete()
        return True

    def get(self, request):
        user = request.user
        shared_by_me = UserShareTable.objects.filter(connection__user_a=user)
        shared_with_me = UserShareTable.objects.filter(connection__user_b=user)
        data = {
            "shared_by_me": UserShareSerializer(shared_by_me, many=True).data,
            "shared_with_me": UserShareSerializer(shared_with_me, many=True).data,

        }
        return Response({'data': data, 'status': True}, status=status.HTTP_200_OK)

    def post(self, request):
        user_a = request.user
        user_b_phone = request.data.get('shared_with', None)
        article_id = request.data.get('article_id', None)
        reward_earned = request.data.get('article_id', 1)
        if user_b_phone and article_id:
            user_b = User.objects.filter(phone=user_b_phone).first()
            if user_b:
                connection_obj, _ = ConnectionTable.objects.get_or_create(
                    user_a=user_a, user_b=user_b)
                article_obj = ArticleData.objects.filter(id=article_id).first()

                if article_obj:
                    # user_share_obj, _ = UserShareTable.objects.get_or_create(connection=connection_obj,
                    #                                                          article=article_obj,
                    #                                                          defaults={"reward_earned": 1})
                    user_share_obj = self.create_share_obj(
                        connection_obj, article_obj, reward_earned=reward_earned)
                    return Response({"status": True,
                                     "message": "shared successfully",
                                     "share_id": user_share_obj.id})
                else:
                    return Response({"status": False, "message": "Article id is not valid"})
            else:
                return Response({'status': False, "message": "User does not exist, Invite."},
                                status=status.HTTP_200_OK)
        return Response({"status": False, "message": "shared_with or article_id not given"})

    def put(self, request, share_id):
        user = request.user
        share_obj = UserShareTable.objects.filter(
            Q(id=share_id) & Q(connection__user_b=user)).first()
        if share_obj:
            share_obj = self.update_share_obj(share_obj)
            return Response({'status': True, "status": "updated successfully"}, status=status.HTTP_200_OK)
        return Response({'status': False, 'message': 'invalid share_id'})

    def delete(self, request, share_id):
        user = request.user
        share_obj = UserShareTable.objects.filter(
            Q(id=share_id) & Q(connection__user_a=user))
        if share_obj:
            self.delete_share_obj(share_obj)
            # share_obj.delete()
            return Response({'status': True, "status": "deleted successfully"}, status=status.HTTP_200_OK)
        return Response({'status': False, 'message': 'invalid share_id'})


class RewardValueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, article_id=None):
        if article_id:
            article_obj = ArticleData.objects.filter(id=article_id).first()
            if article_obj:
                user = request.user
                categories = article_obj.categories.all()
                connection_reward_obj = ConnectionRewardValue.objects.filter(
                    Q(connection__user_a=user) & Q(category__in=categories)).annotate(
                        total_reward=1.6*F('article_opened') +
                    1.2*F('article_shared')
                ).values('connection__user_b').annotate(max_reward=Max('total_reward'))
                data = UserRewardSerializer(
                    connection_reward_obj, many=True).data
                return Response({'status': True, 'data': data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'message': 'article_id not given'}, status=status.HTTP_200_OK)

    def post(self, request):
        pass
