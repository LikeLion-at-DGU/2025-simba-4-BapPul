from django.shortcuts import render, redirect
from menu.models import Store, Menu
from accounts.models import Profile
from search.models import School
from math import radians, cos, sin, asin, sqrt

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

    return render(request, 'search/main.html', {
        'school': school,
        'radius': radius,
    })


def recommend_result(request):
    user = request.user
    try:
        school = user.profile.school
    except Profile.DoesNotExist:
        return redirect('accounts:create_profile')

    price = int(request.GET.get('price', 5000))
    radius = int(request.GET.get('radius', 500))
    category_name = request.GET.get('category')  # 문자열 e.g. "한식"

    all_stores = Store.objects.filter(school=school)
    if category_name:  # ✅ 선택된 카테고리 있을 때만 필터
        all_stores = all_stores.filter(category__name=category_name)

    nearby_ids = [
        s.id for s in all_stores
        if haversine(s.latitude, s.longitude, school.latitude, school.longitude) * 1000 <= radius
    ]

    menus = Menu.objects.filter(store__id__in=nearby_ids, price__lte=price)

    return render(request, 'search/recommend_result.html', {
        'menus': menus,
        'price': price,
        'radius': radius,
        'selected_category': category_name,
        'categories': ["한식", "일식", "중식", "양식", "분식", "기타"],  # 이건 Category 테이블에서 불러오게도 가능
    })
