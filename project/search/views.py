from django.shortcuts import render, redirect , get_object_or_404
from django.db.models import Avg
from menu.models import Store, Menu, Review , Like
from accounts.models import Profile
from search.models import School
from math import radians, cos, sin, asin, sqrt
import random

def haversine(lat1, lon1, lat2, lon2):
    # 거리 계산 함수
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # 위도/경도 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # haversine 공식
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 지구 반지름 (단위: km)

    return c * r  # 두 지점 사이 거리 (단위: km)

def search(request):
    user = request.user
    school = user.profile.school
    radius = int(request.GET.get('radius', 500))  # 기본값 500m 설정
    menus_with_image = Menu.objects.exclude(image__isnull=True).exclude(image='')
  # 빈 문자열 제거
    advertised_menu = random.choice(list(menus_with_image)) if menus_with_image.exists() else None


    return render(request, 'home.html', {
        'school': school,
        'radius': radius,
        'advertised_menu': advertised_menu,
    })


def recommend_result(request):
    user = request.user
    try:
        profile = user.profile
        school = profile.school
    except Profile.DoesNotExist:
        return redirect('accounts:create_profile')

    # 🔒 안전한 변환
    try:
        price = int(request.GET.get('price', '5000'))
        radius = int(request.GET.get('radius', '500'))
    except ValueError:
        return redirect('search:home')  # 잘못된 요청이면 홈으로 보내기

    category_name = request.GET.get('category')

    all_stores = Store.objects.filter(school=school)
    if category_name:
        all_stores = all_stores.filter(category__name=category_name)

    nearby_ids = [
        s.id for s in all_stores
        if haversine(s.latitude, s.longitude, school.latitude, school.longitude) * 1000 <= radius
    ]

    menus = Menu.objects.filter(store__id__in=nearby_ids, price__lte=price).order_by('-price')

    liked_menu_ids = set(Like.objects.filter(user=profile).values_list('menu_id', flat=True))

    menu_data = []
    for menu in menus:
        store_reviews = Review.objects.filter(menu__store=menu.store)
        menu_data.append({
            'menu': menu,
            'liked': menu.id in liked_menu_ids,
            'review_count': store_reviews.count(),
            'average_rating': round(store_reviews.aggregate(avg=Avg('rating'))['avg'] or 0, 1),
        })

    return render(request, 'search/recommend_result.html', {
        'menus': menu_data,
        'price': price,
        'radius': radius,
        'selected_category': category_name,
        'categories': ["한식", "일식", "중식", "양식", "기타"],
    })

def like_menu(request, menu_id):
    if request.method == 'POST':
        profile = request.user.profile
        menu = get_object_or_404(Menu, id=menu_id)

        like = Like.objects.filter(user=profile, menu=menu).first()
        if like:
            like.delete()  # 찜 취소
        else:
            Like.objects.create(user=profile, menu=menu)  # 찜 등록

        return redirect(request.META.get('HTTP_REFERER', 'search:recommend_result'))


def random_wait(request):
    price = int(request.GET.get('price', 5000))
    radius = int(request.GET.get('radius', 500))
    category = request.GET.get('category')

    return render(request, 'search/random_wait.html', {
        'price': price,
        'radius': radius,
        'category': category,
    })


def random_result(request):
    user = request.user
    try:
        school = user.profile.school
    except:
        return redirect('accounts:create_profile')

    price = int(request.GET.get('price', 5000))
    radius = int(request.GET.get('radius', 500))
    category = request.GET.get('category')

    stores = Store.objects.filter(school=school)
    if category:
        stores = stores.filter(category__name=category)

    nearby_store_ids = [
        store.id for store in stores
        if haversine(store.latitude, store.longitude, school.latitude, school.longitude) * 1000 <= radius
    ]

    menus = Menu.objects.filter(store__id__in=nearby_store_ids, price__lte=price)

    if not menus.exists():
        return render(request, 'search/random_result.html', {
            'menu': None,
            'price': price,
            'radius': radius,
            'category': category,
        })

    selected_menu = random.choice(list(menus))

    return render(request, 'search/random_result.html', {
        'menu': selected_menu,
        'price': price,
        'radius': radius,
        'category': category,
    })
