from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.
from django.core.paginator import Paginator, EmptyPage

from .models import ArticleData
from .serializers import ArticleDataSerializer


PAGE_FEED_CONSTANT = 10


class FeedView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, article_id=None):
        if article_id:
            feed_list = ArticleData.objects.filter(id=article_id)
            data = ArticleDataSerializer(feed_list, many=True).data
            return Response({"data": data, 'next_p': None, 'status': True}, status=status.HTTP_200_OK)

        page_n = request.GET.get('p', 1)
        feed_list = ArticleData.objects.order_by('-creation_time')
        feed_paginator = Paginator(feed_list, PAGE_FEED_CONSTANT)

        try:
            page_data = feed_paginator.page(page_n)

        except EmptyPage as e:
            return Response({"data": [], 'next_p': None, 'status': True},
                            status=status.HTTP_200_OK)

        next_p = page_data.next_page_number() if page_data.has_next() else None
        data = ArticleDataSerializer(page_data, many=True).data
        return Response({"data": data, 'next_p': next_p, 'status': True}, status=status.HTTP_200_OK)

    def post(self, request):
        pass
