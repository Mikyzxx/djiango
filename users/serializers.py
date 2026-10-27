from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'telefono',
            'password',
            'is_active',
            'is_staff'
        ]
        extra_kwargs = {
            # Corrección de seguridad 1: La contraseña nunca se retorna en las respuestas de la API
            'password': {
                'write_only': True,
                'required': False,
            },
            'username': {
                'required': False,
            }
        }
