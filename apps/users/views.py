from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def register_user(request):
    data = {
        'username': request.data.get('username'),
        'password': request.data.get('password'),
        'email': request.data.get('email')
    }
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)