from django.urls import path, include
from watchlist_app.api.views import (ReviewDetail, WatchDetailAV, WatchlistAV,Home,
                             StreamDetailAV,StreamListAV,ReviewList,ReviewCreate)

urlpatterns = [

    path('',Home.as_view(),name='homepage'),
    path('list/', WatchlistAV.as_view(), name='movie-list'),
    path('list/<int:pk>', WatchDetailAV.as_view(), name='movie-detail'),


    path('listplatform/', StreamListAV.as_view(), name='stream-list'),
    path('listplatform/<int:pk>', StreamDetailAV.as_view(), name='stream-detail'),


    path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='stream-detail'),
    path('stream/<int:pk>/review/', ReviewList.as_view(), name='stream-detail'),
    path('stream/review/<int:pk>', ReviewDetail.as_view(), name='stream-detail'),
]