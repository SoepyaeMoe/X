from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email', 'image', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class HeartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heart
        fields = ['blog', 'user']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Comment
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    category = CategorySerializer(read_only=True, many=False)
    hearts = HeartSerializer(read_only=True, many=True, source='heart_set')
    comments = CommentSerializer(read_only=True, many=True, source='comment_set')
    class Meta:
        model = Blog
        fields = [
                'id','author', 'image', 
                'title', 'content', 'category', 
                'views', 'updated_at', 'created_at', 
                'comments', 'hearts'
            ]

