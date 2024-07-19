from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .paginations import BlogsPagination
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .decorators import login_required, owner_only
from .helper import success_response, error_response
from .forms import UserSignupForm, LoginForm, PasswordChangeForm
from rest_framework_simplejwt.tokens import RefreshToken
import os

@api_view(['GET'])
def routes(request):
    data = [
        'POST / login/',
        'POST / signup/',
        'GET / auth-user/',
        'GET / blogs/',
        'GET / blogs/:id',
        'POST / create-blog',
        'GET / category/',
        'and more urls see in base/urls.py'
    ]
    return Response(data)

@api_view(['POST'])
def login(request):
    data = request.data
    form = LoginForm(data)

    email = data.get('email')
    password = data.get('password')
    if form.is_valid():
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializers = UserSerializer(user, many=False)
            return Response(success_response({
                'user': serializers.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }))
        else:
            return Response(error_response({'password': ['Invalid password']}))
    else:
        return Response(error_response(form.errors))


@api_view(['POST'])
def signup(request):
    data = request.data
    form = UserSignupForm(data)

    if form.is_valid():
        user = form.save()
        serializers = UserSerializer(user, many=False)
        message = "Sing up success. Please login."
        return Response(success_response(serializers.data, message ))
    else:
        return Response(error_response(form.errors))

@api_view(['POST'])
@login_required
def logout(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(success_response('Logout success'))
    except Exception as e:
        return Response(error_response(str(e)))
    
@api_view(['GET', 'PUT'])
@login_required
def auth_user(request):
    user = request.user

    if request.method == 'PUT':

        if request.data.get('name') == '' and request.data.get('email') == user.email:
            return Response(error_response({'name':'This Fields is required.'}))
        
        old_image = ''

        if user.image != 'default_profile.svg' and user.image:
            old_image = user.image.path

        serializers = UserSerializer(instance=user, data=request.data)
        if serializers.is_valid():
            if os.path.exists(old_image):
                os.remove(old_image)
            serializers.save() 
    serializers = UserSerializer(user, many=False)
    return Response(success_response(serializers.data))

@api_view(['GET'])
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    if user is None:
        return Response(error_response("User not found"))
    serializers = UserSerializer(user, many=False)
    return Response(success_response(serializers.data))
    
@api_view(['POST'])
@login_required
def change_password(request):
    user = request.user 
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    form = PasswordChangeForm(request.data)
    if form.is_valid():
        if not user.check_password(old_password):
            return Response(error_response({'old_password': ['Wroung old password']}))
        else:
            user.password = make_password(new_password)
            user.save()
            return Response(success_response('Password change success'))
    else:
        return Response(error_response(form.errors))

@api_view(['GET', 'POST'])
def category(request):
    category = Category.objects.all()
    serializers = CategorySerializer(category, many=True)
    return Response(success_response(serializers.data))

@api_view(['GET', 'POST'])
def blogs(request):
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.saved()
    query = request.GET.get('query')
    user_id = request.GET.get('id')

    pagination_class = BlogsPagination()
    if query is None:
        query = ''
    blogs = Blog.objects.filter( 
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(category__name__icontains=query) |
        Q(author__email__icontains=query) 
    )

    if user_id is not None:
        blogs = Blog.objects.filter(
            Q(author__id=user_id) &
            Q(category__name__icontains=query)
        )

    pages = pagination_class.paginate_queryset(blogs, request)
    if pages is not None:
        serializer = BlogSerializer(pages, many=True)
        return pagination_class.get_paginated_response(serializer.data)
    serializer = BlogSerializer(blogs, many=True)
    return Response(success_response(serializer.data))

@api_view(['GET'])
def top_blogs(request):
    top_blogs = Blog.objects.all().order_by('-views')[:4]
    serializers = BlogSerializer(top_blogs, many=True)
    return Response(success_response(serializers.data))


@api_view(['GET'])
def blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(error_response('Blog does not exist'))
    blog.views += 1
    blog.save()
    serializers = BlogSerializer(blog, many=False)
    return Response(success_response(serializers.data))

@api_view(['POST'])
@login_required
def create_blog(request):
    data = request.data
    author = request.user
    category, created = Category.objects.get_or_create(name=data['category'])
    try:
        image = request.FILES['image']
        blog = Blog(author=author, category=category, image=image, title=data['title'], content=data['content'])
    except:
        blog = Blog(author=author, category=category, title=data['title'], content=data['content'])
    blog.save()
    serializer = BlogSerializer(blog, many=False)
    return Response(success_response(serializer.data, message="Blog create successful"))

@api_view(['PUT'])
@login_required
@owner_only(Blog)
def update_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(error_response('Blog does not exist'))

    data = request.data
    blog.title = data['title']
    blog.content = data['content']
    blog.category, created = Category.objects.get_or_create(name=data['category'])
    try:
        image = request.FILES['image']
        old_image = blog.image.path
        if os.path.exists(old_image) and blog.image != 'default_blog_image.png':
            os.remove(old_image)
        blog.image = image
    except:
        pass
    blog.save()
    serializer = BlogSerializer(blog, many=False)
    return Response(success_response(serializer.data))

@api_view(['DELETE'])
@login_required
@owner_only(Blog)
def delete_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(error_response('Blog does not exist'))
    old_image = blog.image.path
    if os.path.exists(old_image) and blog.image != 'default_blog_image.png':
        os.remove(old_image)
    blog.delete()
    return Response(success_response('Blog deleted'))


@api_view(['POST'])
@login_required
def heart_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(error_response('Blog does not exist'))
    
    heart = Heart.objects.filter(blog=blog, user=request.user)
    if not heart.exists():
        heart = Heart.objects.create(blog=blog, user=request.user)
        serializers = HeartSerializer(heart, many=False)
        return Response(success_response(serializers.data, message="Heart added"))
    else:
        heart = heart.delete()
        serializers = HeartSerializer(heart, many=False)
        return Response(success_response(heart, message='Heart removed'))


@api_view(['POST'])
@login_required
def views_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(error_response('Blog does not exist'))
    blog.views += 1
    blog.save()
    serializer = BlogSerializer(blog, many=False)
    return Response(success_response(serializer.data))

# get comments from a blog
@api_view(['GET'])
def comments_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(error_response('Blog does not exist'))
    comments = Comment.objects.filter(blog=blog)
    serializers = CommentSerializer(comments, many=True)
    return Response(success_response(serializers.data))

# send comment to a blog
@api_view(['POST'])
@login_required
def comment_blog(request, pk):
    if request.method == 'POST':
        data = request.data
        try:
            blog = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response(error_response('Blog does not exist'))
        comment = Comment.objects.create(
            blog=blog,
            author=request.user,
            content=data['content']
        )
        serializers = CommentSerializer(comment)
        return Response(success_response(serializers.data))
    
@api_view(['PUT', 'DELETE'])
@login_required
@owner_only(Comment)
def comment_update(request, pk):
    if request.method == 'PUT':
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response(error_response('Comment does not exist'))
        
        comment.content = request.data['content']
        comment.save()
        serializers = CommentSerializer(comment, many=False)
        return Response(success_response(serializers.data))
    
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response(error_response('Comment does not exist'))
        comment.delete()
        return Response(success_response('Comment deleted'))
        
@api_view(['POST'])
@login_required
def delete_all_blogs(request):
    user = request.user
    if user.check_password(request.data.get('password')):
        blogs = Blog.objects.filter( Q(author__id = user.id))
        blogs.delete()
        return Response(success_response('Your blogs has been deleted.'))
    else:
        return Response(error_response('Wroung password'))
    
@api_view(['POST'])
@login_required
def delete_account(request):
    user = request.user
    if user.check_password(request.data.get('password')):

        # remove profile image
        if user.image != 'default_profile.svg' and user.image:
            old_image = user.image.path
            if os.path.exists(old_image):
                os.remove(old_image)

        # remove all blog image
        blogs = Blog.objects.filter(Q(author__id=user.id))
        for blog in blogs:
            old_image = blog.image.path
            if os.path.exists(old_image) and blog.image != 'default_blog_image.png':
                os.remove(old_image)

        user.delete()
        return Response(success_response('delete success'))
    else:
        return Response(error_response('Wroung password'))