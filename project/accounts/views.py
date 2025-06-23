from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from search.models import School
from menu.models import Like, VisitLog, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('search:home')
        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})

    return render(request, 'accounts/login.html')


def logout(request):  # {% url 'accounts:logout' %}
    auth.logout(request)
    return redirect('accounts:start')

def start_view(request):
    return render(request, 'accounts/start.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']
        nickname = request.POST['nickname']
        school_name = request.POST['school']

        # username 중복 체크
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {
                'error': '이미 존재하는 아이디입니다.'
            })

        if password != confirm:
            return render(request, 'accounts/signup.html', {
                'error': '비밀번호가 일치하지 않습니다.'
            })

        try:
            school = School.objects.get(name=school_name)
        except School.DoesNotExist:
            return render(request, 'accounts/signup.html', {
                'error': '선택한 학교가 존재하지 않습니다.'
            })

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, nickname=nickname, school=school)
        auth.login(request, user)
        return redirect('search:home')

    # GET 요청
    schools = School.objects.all()
    return render(request, 'accounts/signup.html', {'schools': schools})

def mypage(request, id):
    user = get_object_or_404(User, pk=id)
    profile = user.profile

    # 최근 방문 중 아직 리뷰가 없는 메뉴 1개 가져오기
    latest_review = (
        VisitLog.objects
        .filter(user=profile, reviewed=False, menu__isnull=False)
        .select_related('menu', 'store')
        .order_by('-visited_at')
        .first()
    )

    context = {
        'user': user,
        'latest_review': latest_review  # ➕ context에 추가
    }
    return render(request, 'accounts/mypage.html', context)


def my_likes(request, id):
    user = get_object_or_404(User, pk=id)
    profile = user.profile
    likes = Like.objects.filter(user=profile).select_related('menu__store')  # 메뉴 + 음식점 정보
    context = {
        'likes': likes
    }
    return render(request, 'accounts/my_likes.html', context)

def my_visits(request, id):
    user = get_object_or_404(User, pk=id)
    profile = user.profile
    visits = VisitLog.objects.filter(user=profile).select_related('menu', 'store').order_by('-visited_at')
    context = {
        'visits': visits
    }
    return render(request, 'accounts/my_visits.html', context)

def my_reviews(request, id):
    user = get_object_or_404(User, pk=id)
    profile = user.profile
    reviews = Review.objects.filter(writer=profile).select_related('menu__store').order_by('-created_at')
    context = {
        'reviews': reviews
    }
    return render(request, 'accounts/my_reviews.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password and password != confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('accounts:edit_profile')

        if password:
            user.set_password(password)
            user.save()
            auth.login(request, user)  # 비번 바꾸면 재로그인 필요

        if nickname:
            profile.nickname = nickname
            profile.save()

        messages.success(request, '정보가 성공적으로 수정되었습니다.')
        return redirect('accounts:mypage', id=user.id)

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'accounts/edit_profile.html', context)