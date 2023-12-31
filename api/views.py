from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny


from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from chat.models import *
from chat.serializers import *

from library.models import *
from library.serializers import *




class ListCategories(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        """
        Return a list of all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = request.data
        
        serializer = CategorySerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            data = {
                'status': True,
                'message': 'Category was successfully created'
            }
            
            return Response(data)

        else:
            return Response(serializer.errors)
            
    
        
        
class ListAuthors(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorSerializer
    
    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        print(request.data)
        
        return Response({'status': 200})


class ListBooks(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = BookSerializer 
    
    def get(self, request, format=None):
        import time
        # time.sleep(5)
        
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
        
    
    def post(self, request, format=None):
        user: User = request.user
        data = request.data
        
        if user.is_staff:
            
            serializers = BookSerializer(data=data)
            
            if serializers.is_valid():
                serializers.save()
                
                return Response({'status:' : 201}, status=201)
            
            else:
                return Response(serializers.errors)
        else:
            return Response({'status': 403}, status=403)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth_token(request):
    string_token = request.META.get('HTTP_AUTHORIZATION').split('Token')[1].strip() if request.META.get('HTTP_AUTHORIZATION') else False
    
    if string_token:
        token:Token = Token.objects.filter(key=string_token) 
        
        if token.exists():
            user = token[0].user

            sr = UserSerializer(user)
            
            
            return Response(sr.data, status=200)
        
        
    return Response({'status': 403}, status=403)
    
    
    

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    sr = UserSerializer(data=data)
    
    if sr.is_valid():
        user = sr.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key})
    
    return Response({'status': 400}, status=400)
    
    
    

@api_view(['GET'])
@permission_classes([AllowAny])
def chat_info(request, name):
    
    sr = GroupSerializer(Group.objects.get(name=name))

    return Response(sr.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def ms_info(request):
    
    sr = MessageSerializer(Message.objects.all(), many=True)

    return Response(sr.data)


