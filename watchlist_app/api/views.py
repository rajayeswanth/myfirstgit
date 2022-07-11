from rest_framework import status
from rest_framework.exceptions import ValidationError
from watchlist_app.models import StreamPlatform,WatchList,Review
from django.http import JsonResponse
from rest_framework import generics
from watchlist_app.api.serializers import WatchlistSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewOwnerOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
     
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist = watchlist,review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this one.")
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)

        # if watchlist.number_rating == 0:   
        # else:
        #    watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2 
           

class ReviewList(generics.ListAPIView):
    permission_classes = [AdminOrReadOnly]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Review.objects.all()
    permission_classes = [ReviewOwnerOrReadOnly]
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(pk=pk)

    def perform_destroy(self,serializer):
        pk = self.kwargs['pk']
        review = Review.objects.get(pk = pk)
        w_id = review.watchlist_id
        watchlist = WatchList.objects.get(pk=w_id)
        watchlist.number_rating = watchlist.number_rating - 1
        review.delete()
        watchlist.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class WatchlistAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        watchlists = WatchList.objects.all()   
        serializer = WatchlistSerializer(watchlists,many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)   
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):

    def get(self, request,pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'watchlist not found'},status=status.HTTP_404_NOT_FOUND )
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request,pk):
        if request.method == 'PUT':
            watchlist = WatchList.objects.get(pk=pk)
            serializer = WatchlistSerializer(watchlist,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    def delete(self, request,pk):
        if request.method == 'DELETE':
            watchlist = WatchList.objects.get(pk=pk)
            watchlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class Home(APIView):
    def home(self, request):
        return Response({"home":"this is my home"})

class StreamListAV(APIView):
    def get(self, request):
        watchlists = StreamPlatform.objects.all()   
        serializer = StreamPlatformSerializer(watchlists,many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)   
        else:
            return Response(serializer.errors)

class StreamDetailAV(APIView):
    def get(self, request,pk):
        try:
            watchlist = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'watchlist not found'},status=status.HTTP_404_NOT_FOUND )
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request,pk):
        if request.method == 'PUT':
            watchlist = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(watchlist,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    def delete(self, request,pk):
        if request.method == 'DELETE':
            watchlist = StreamPlatform.objects.get(pk=pk)
            watchlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)





















# @api_view(['GET', 'POST'])
# def watchlist_list(request):
#     if request.method == 'GET':
#         watchlists = watchlist.objects.all()
#         serializer = WatchlistSerializer(watchlists,many = True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = WatchlistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def watchlist_details(request, pk):
#     if request.method == 'GET':
#         watchlist = watchlist.objects.get(pk=pk)
#         serializer = WatchlistSerializer(watchlist)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         watchlist = watchlist.objects.get(pk=pk)
#         serializer = WatchlistSerializer(watchlist,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     if request.method == 'DELETE':
#         watchlist = watchlist.objects.get(pk=pk)
#         watchlist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

