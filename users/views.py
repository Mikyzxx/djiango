from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if 'password' in request.data and request.data['password']:
            try:
                request.data['password'] = make_password(request.data['password'])
            except TypeError:
                data = request.data.copy()
                data['password'] = make_password(data['password'])
                request._full_data = data
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Actualiza el usuario. Si se envía una nueva contraseña, se cifra antes de guardar.
        Si no se envía contraseña, no se modifica la contraseña existente.
        """
        if 'password' in request.data and request.data['password']:
            try:
                request.data['password'] = make_password(request.data['password'])
            except TypeError:
                data = request.data.copy()
                data['password'] = make_password(data['password'])
                request._full_data = data
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Corrección de seguridad 2:
        En el código del manual original (pág. 10):
            if "password" in request.data:
                request.data["password"] = make_password(request.data["password"])
            else:
                request.data["password"] = request.user.password
        
        Falla de seguridad identificada:
        Al actualizar un usuario sin enviar contraseña, el manual le asignaba
        la contraseña (hash) de 'request.user' (quien hace la petición, típicamente el admin).
        
        Corrección implementada:
        Solo se modifica la contraseña cuando viene explícitamente en la petición.
        Si no viene en la petición, se mantiene intacta la contraseña del usuario objetivo.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
