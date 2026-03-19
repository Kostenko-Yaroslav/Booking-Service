from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions

from users.models import CustomUser
from users.serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
@extend_schema_view(
    post=extend_schema(
        auth=[],
        examples=[
            OpenApiExample(
                'Valid Request Example',
                value={
                    'username': 'user',
                    'email': 'user@example.com',
                    'password': 'strongpassword123'
                },
                request_only=True,
            )
        ]
    )
)

class Register(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
