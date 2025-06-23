from django.shortcuts import render, get_object_or_404, redirect
from .models import Store, Menu , Review ,VisitLog
from django.db.models import Avg, Count

def store_detail(request, store_id, menu_id):
    store = get_object_or_404(Store, id=store_id)
    menus = Menu.objects.filter(store=store)
    selected_menu = get_object_or_404(Menu, id=menu_id, store=store)

    # 리뷰 3개 (이미지 있는 것만)
    recent_reviews = Review.objects.filter(
        menu__store=store,
        image__isnull=False
    ).exclude(image='').order_by('-created_at')[:3]

    # 평균 별점, 리뷰 개수 계산
    stats = Review.objects.filter(menu__store=store).aggregate(
        avg_rating=Avg('rating'),
        review_count=Count('id')
    )

    return render(request, 'menu/store_detail.html', {
        'store': store,
        'menus': menus,
        'selected_menu': selected_menu,
        'recent_reviews': recent_reviews,
        'avg_rating': round(stats['avg_rating'], 1) if stats['avg_rating'] else 3.0,
        'review_count': stats['review_count'],
    })

def store_review_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    # 이 음식점의 모든 리뷰 (연결된 메뉴들에 달린 리뷰들 포함)
    reviews = Review.objects.filter(menu__store=store).select_related('menu', 'writer')

    return render(request, 'menu/store_review_list.html', {
        'store': store,
        'reviews': reviews,
    })
    
def store_location(request, store_id, menu_id):
    store = get_object_or_404(Store, id=store_id)
    user = request.user.profile

    menu = get_object_or_404(Menu, id=menu_id)

    VisitLog.objects.create(user=user, store=store, menu=menu)

    context = {
        'store': store,
        'menu': menu,
    }
    return render(request, 'menu/store_location.html', context)


def store_review(request, store_id, menu_id):
    store = get_object_or_404(Store, id=store_id)
    menu = get_object_or_404(Menu, id=menu_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        image = request.FILES.get('photo')
        review = Review.objects.create(
            writer=request.user.profile,
            menu=menu,
            rating=rating,
            image= image,
        )
        return render(request, 'menu/review_confirm.html', {
            'store': store,
            'menu': menu,
            'rating': rating,
            'nickname': request.user.profile.nickname,
            'review': review,
        })

    return render(request, 'menu/store_review.html', {
        'store': store,
        'menu': menu,
    })