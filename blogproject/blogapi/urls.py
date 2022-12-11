from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

from .views import UserCreateView, user_login_view, refresh_token_view,block_user_view

router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')


urlpatterns = [

    #code Here


    path('user/create-user/', UserCreateView.as_view(), name="create_user"),
    path('user/login/', user_login_view, name='user_login'),
    path('user/refresh-token/', refresh_token_view, name='merchant_refresh_token'),
    path('user/block-user/', block_user_view, name='block_user_view'),


# end code

]

urlpatterns += router.urls