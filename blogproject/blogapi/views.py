from rest_framework import status, generics


from .models import BlogUser, CreatePost, CountHistory

from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from .authentication import SafeJWTAuthentication, generate_access_token, generate_refresh_token
from .serializers import UserCreateSerializer,UserListSerializer, CreatePostSerializer
#
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes

import jwt
import bcrypt
from django.conf import settings

from django.core.signals import request_finished
from django.dispatch import receiver, Signal

mysignal = Signal()

#

@api_view(['POST'])
@permission_classes((AllowAny,))
def user_login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = BlogUser.objects.filter(email=email, is_active=True).first()
    serializer = UserListSerializer(user)
    if user is None:
        return Response({
            "status": False,
            "data": "User not found"
        }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({
                "status": True,
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": serializer.data
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": True,
                "data": "Password is Invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def refresh_token_view(request):
    refresh_token = request.data.get('refresh_token')

    if refresh_token is None:
        return Response({
            "status": False,
            "data": "Please provide refresh token"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({
            "status": False,
            "data": "Refresh token expired, please login again."
        }, status=status.HTTP_401_UNAUTHORIZED)
    user = BlogUser.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        return Response({
            "status": False,
            "data": "User not found"
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response({
            "status": False,
            "data": "User not active"
        }, status=status.HTTP_400_BAD_REQUEST)

    access_token = generate_access_token(user)
    return Response({
        "status": True,
        "data": {
            "access_token": access_token
        }
    })


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        print("View files")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(request.data.get('password'), 'utf-8'), salt)
        data = {

            'username': request.data.get('username'),
            'password': hash_password.decode('utf-8'),
            'email': request.data.get('email'),
            'first_name': request.data.get('first_name') or None,
            'last_name': request.data.get('last_name') or None,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            print(serializer.is_valid())
            serializer.save()
            return Response({"status": True, "data": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))
def block_user_view(request):
    user_id = request.data['user_id']
    print("dd",user_id)
    user_obj = BlogUser.objects.filter(id=user_id).first()
    if user_obj:
        user_obj.is_active = False
        user_obj.save()
        return Response({"status": True, "data": "User block successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": True, "data": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ViewSet):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='create-post')
    def create_post(self, request):
        data = request.data
        serializer = CreatePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": "Data saved successfully"}, status=status.HTTP_200_OK)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='get-allpost-state')
    def get_allpost_by_state(self, request):
        state = request.data['state']
        queryset = CreatePost.objects.filter(state=state,is_active=True)
        serializer = CreatePostSerializer(queryset, many=True)
        if queryset:
            mysignal.send(sender= BlogUser, name= request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": True, "data": "Post data not found. "}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='get-allpost')
    def get_allpost(self, request):
        queryset = CreatePost.objects.all()
        serializer = CreatePostSerializer(queryset, many=True)
        if queryset:
            mysignal.send(sender= BlogUser, name= request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": True, "data": "Post data not found. "}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='post-by-user')
    def get_post_by_user(self, request):
        user_id = request.data['user_id']
        queryset = CreatePost.objects.filter(user_id=user_id,is_active=True)
        serializer = CreatePostSerializer(queryset, many=True)
        if queryset:
            mysignal.send(sender= BlogUser, name= request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": True, "data": "Post data not found. "}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='get-post')
    def get_post_id(self, request):
        post_id = request.data['post_id']
        queryset = CreatePost.objects.filter(id=post_id, is_active=True)
        serializer = CreatePostSerializer(queryset, many=True)
        if queryset:
            mysignal.send(sender=BlogUser, name=request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": True, "data": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='post-archive')
    def post_archive(self, request):
        post_id = request.data['post_id']
        queryset = CreatePost.objects.get(id=post_id, is_active=True)
        if queryset:
            if queryset.state != 'Archived':
                queryset.state = 'Archived'
                queryset.save()
                serializer = CreatePostSerializer(queryset, many=True)
                return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": True, "data": "Post is already in archived"}, status=status.HTTP_200_OK)

        else:
            return Response({"status": True, "data": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put', 'patch'], detail=False, url_path='update-post/(?P<pk>[^/.]+)')
    def update_post(self, request, pk):
        queryset = CreatePost.objects.filter(pk=pk).first()
        if queryset:
            serializer = CreatePostSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": True, "data": "Data updated successfully"}, status=status.HTTP_200_OK)
            return Response({"status": False, "data": serializer.errors}, status=status.HTTP_200_OK)
        return Response({"status": False, "data": "Data not found"}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='delete-post')
    def delete_post(self, request):
        post_id = request.data['post_id']
        queryset = CreatePost.objects.filter(id=post_id, is_active=True)
        if queryset:
            queryset.delete()
            return Response({"status": True, "data": "Post Delete successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": True, "data": "Post not found"}, status=status.HTTP_404_NOT_FOUND)



@receiver(mysignal)
def count(sender, **kwargs):
    for k, v in kwargs.items():
        if k == 'name':
            print(v)
    countObj = CountHistory.objects.filter(user= v).first()

    if countObj == None:
        count = 1
        CountHistory.objects.create(hit_count= count,user=v)
    else:
        count = countObj.hit_count + 1
        countObj.hit_count = count
        # countObj.user = v
        countObj.save()



