from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication


# Create your views here.


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    @action(methods=["POST"], detail=True)
    def rate_video(self, request, pk):
        if 'stars' in request.data:
            video = Video.objects.get(id=pk)
            stars = request.data['stars']
            comments = request.data['comments']
            user = request.user
            try:
                rating = Rating.objects.get(user=user.id, video=video.id)
                rating.stars = stars
                rating.comments = comments
                rating.save()

                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'rating has been updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, video=video, stars=stars, comments=comments)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'Please enter stars for the rating'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        response = {'message': 'message cannot be updated'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
