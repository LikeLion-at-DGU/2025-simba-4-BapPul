import requests
from search.models import School
from .models import Store, Category

# ❌ 제외할 카테고리 키워드
BLOCKED_CATEGORY_KEYWORDS = ["카페", "커피", "술집", "호프", "주점", "포장마차", "바", "와인"]

# ✅ 원하는 대분류 카테고리 (없으면 '기타' 처리)
WANTED_MAIN_CATEGORIES = ["한식", "중식", "일식", "양식", "분식", "패스트푸드"]

def is_excluded_category(category_name: str) -> bool:
    
    return any(keyword in category_name for keyword in BLOCKED_CATEGORY_KEYWORDS)

def extract_main_category(category_full: str) -> str:
    
    for main_cat in WANTED_MAIN_CATEGORIES:
        if main_cat in category_full:
            return main_cat
    return "기타"

def get_restaurants_nearby_school(school):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": "KakaoAK c667f7edb965566d20e472b3b30b4c4d"  # ← 너의 REST API 키
    }

    restaurants = []

    for page in range(1, 4):  # ✅ 최대 3페이지까지 요청
        params = {
            "query": "음식점",
            "x": school.longitude,
            "y": school.latitude,
            "radius": 1000,
            "size": 15,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        if 'documents' not in result:
            print("❌ 'documents' 키가 없습니다!")
            continue

        for place in result['documents']:
            category_full = place.get("category_name", "")

            if is_excluded_category(category_full):
                continue  # ❌ 카페/술집 등 제외

            # ✅ 대분류만 추출
            category_clean = extract_main_category(category_full)

            restaurants.append({
                "name": place['place_name'],
                "address": place.get('road_address_name') or place.get('address_name'),
                "lat": float(place['y']),
                "lng": float(place['x']),
                "category": category_clean
            })

    return restaurants

def fetch_and_save_restaurants_for_school(school):
    data = get_restaurants_nearby_school(school)

    for item in data:
        category_obj, _ = Category.objects.get_or_create(name=item['category'])

        if not Store.objects.filter(name=item['name'], address=item['address'], school=school).exists():
            Store.objects.create(
                name=item['name'],
                address=item['address'],
                latitude=item['lat'],
                longitude=item['lng'],
                school=school,
                category=category_obj
            )
