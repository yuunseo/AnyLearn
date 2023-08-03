from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from users.models import User
from . import serializers

class Me(APIView):
    permission_classes = [IsAuthenticated] # /me가 
#로그인한 user의 정보를 보여줘야하는데 private해야 함

		#나에 대한 정보를 볼 수 있다!!
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        #PrivateUserSerializer도 방금 만들었음
        return Response(serializer.data)

    #근데 is_superuser같은 부분은 수정하면 안 되니까
		# serializer에서 제외시켜주기
    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data = request.data,
            partial = True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(
                user
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Users(APIView):

    def post(self, request):
		# step1) user가 보낸 data에서 password를 가져옴
        password = request.data.get('password')
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data = request.data)
        #password에 대한 검증만 해주면 돼
        if serializer.is_valid():
			# step2) user를 db에 저장
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class PublicUser(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

# 인증되지 않은 사용자가 url을 호출하지 못하도록 막을 것임
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError

class LogIn(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise ParseError
        user = authenticate(
            request,
            email=email,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})