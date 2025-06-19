import requests
from search.models import School
from .models import Store

def get_restaurants_nearby_school(school):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": "KakaoAK c667f7edb965566d20e472b3b30b4c4d"
    }
    params = {
        "query": "음식점",
        "x": school.longitude,
        "y": school.latitude,
        "radius": 1000,
        "size": 15
    }

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    print("📦 카카오 응답 JSON 전체:", result)

    if 'documents' not in result:
        print("❌ 'documents' 키가 없습니다!")
        return []

    restaurants = []
    for place in result['documents']:
        restaurants.append({
            "name": place['place_name'],
            "address": place.get('road_address_name') or place.get('address_name'),
            "lat": float(place['y']),
            "lng": float(place['x']),
        })

    return restaurants


def fetch_and_save_restaurants_for_school(school):
    data = get_restaurants_nearby_school(school)
    for item in data:
        if not Store.objects.filter(name=item['name'], address=item['address'], school=school).exists():
            Store.objects.create(
                name=item['name'],
                address=item['address'],
                latitude=item['lat'],
                longitude=item['lng'],
                school=school
            )

