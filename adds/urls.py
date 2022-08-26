from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import *


urlpatterns = [

    path("Category", CategoryAPIView.as_view()),
    path('Subscription', SubscriptionApi.as_view()),
    path('New', NewAdApiView.as_view()),
    path('Ordering', FilterAPIView.as_view()),
    path('Filter', ProductList.as_view()),
    path('Search', SearchAPIListView.as_view()),
    path('filterCategory', PostFilterList.as_view()),
    path('sub/<int:pk>', SubcategoryAPIView.as_view()),
    # path('detailpost', DetailPostView.as_view()),
]