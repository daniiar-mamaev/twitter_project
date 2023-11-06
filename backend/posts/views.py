import datetime

from rest_framework import viewsets
from rest_framework import request
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail
from django.conf import settings

from posts.models import Tweet, Reply, Reaction, ReactionType, ReactionToReply
from posts.serializers import TweetSerializer, ReplySerializer, ReactionSerializer, ReactionTypeSerializer, \
    ReactionToReplySerializer
from .permissions import IsAuthorOrIsAuthenticated, IsAdminOrReadOnly
from . import paginations


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrIsAuthenticated, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # pagination_class = paginations.TweetNumberPagination
    pagination_class = LimitOffsetPagination
    search_fields = ['text', 'profile__user__username']
    ordering_fields = ['updated_at', 'profile__user_id']

    def perform_create(self, serializer):
        send_mail(
            "Создание публикации",
            f"Поздравляем, вы успешно опубликовали пост!</br> "
            f"Текст вашего поста {serializer.validated_data['text']}",
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            fail_silently=False,
        )
        serializer.save(profile=self.request.user.profile)

    # @action(methods=['GET'], detail=False, url_path='reaction_url')
    # def reaction(self, request, pk=None):
    #     return Response({'key': 'value'})

    @action(
        methods=['GET'],
        detail=False,
    )
    def recent(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(created_at__gte=datetime.date.today()-datetime.timedelta(days=1)),
            many=True)
        return Response(serializer.data)

    @action(
        methods=['POST'],
        detail=True,
        serializer_class=ReactionSerializer,
        permission_classes=[IsAuthenticated, ],
    )
    def reaction(self, request, pk=None):
        serializer = ReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile=self.request.user.profile,
                tweet=self.get_object()
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# class ReplyViewSet(viewsets.ModelViewSet):
#     queryset = Reply.objects.all()
#     serializer_class = ReplySerializer
#     authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthorOrIsAuthenticated, ]
#
#     def perform_create(self, serializer):
#         serializer.save(profile=self.request.user.profile)


class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])


class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # pagination_class = paginations.TweetNumberPagination
    pagination_class = LimitOffsetPagination
    search_fields = ['text', 'profile__user__username']
    ordering_fields = ['updated_at', 'profile__user_id']

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile, tweet_id=self.kwargs['tweet_id'])


class ReactionTypeViewSet(viewsets.ModelViewSet):
    queryset = ReactionType.objects.all()
    serializer_class = ReactionTypeSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class ReactionToReplyCreateAPIView(generics.CreateAPIView):
    queryset = ReactionToReply.objects.all()
    serializer_class = ReactionToReplySerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            reply=generics.get_object_or_404(Reply, pk=self.kwargs['reply_id'])
        )


# class ReactionCreateAPIView(generics.CreateAPIView):
#     queryset = Reaction.objects.all()
#     serializer_class = ReactionSerializer
#     authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(
#             profile=self.request.user.profile,
#             tweet_id=self.kwargs['tweet_id']
#         )
