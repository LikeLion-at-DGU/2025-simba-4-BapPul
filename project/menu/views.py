from django.shortcuts import render, get_object_or_404, redirect
from .models import Store, Menu , Review ,VisitLog , Like
from django.db.models import Avg, Count
from django.urls import reverse

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
        'avg_rating': round(stats['avg_rating'], 1) if stats['avg_rating'] else 0.0,
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
        Review.objects.create(
            writer=request.user.profile,
            menu=menu,
            rating=rating,
            image=image,
        )

        # ✅ 리뷰 작성 끝났으면 리뷰 확인 화면으로 redirect
        return redirect('menu:review_confirm', store_id=store.id, menu_id=menu.id)

    return render(request, 'menu/store_review.html', {
        'store': store,
        'menu': menu,
    })
    

def review_confirm(request, store_id, menu_id):
    store = get_object_or_404(Store, id=store_id)
    menu = get_object_or_404(Menu, id=menu_id)

    review = Review.objects.filter(menu=menu, writer=request.user.profile).order_by('-created_at').first()

    stats = Review.objects.filter(menu__store=store).aggregate(
        avg_rating=Avg('rating'),
        review_count=Count('id')
    )

    is_liked = menu.likes.filter(user=request.user.profile).exists()

    return render(request, 'menu/review_confirm.html', {
        'store': store,
        'menu': menu,
        'review': review,
        'rating': review.rating,
        'nickname': request.user.profile.nickname,
        'avg_rating': round(stats['avg_rating'], 1) if stats['avg_rating'] else 0.0,
        'review_counting': stats['review_count'],
        'is_liked': is_liked,
    })


def like_menu_in_menu_app(request, menu_id):
    if request.method == 'POST':
        profile = request.user.profile
        menu = get_object_or_404(Menu, id=menu_id)

        like = Like.objects.filter(user=profile, menu=menu).first()
        if like:
            like.delete()
        else:
            Like.objects.create(user=profile, menu=menu)

        from_page = request.GET.get('from')
        if from_page == 'review_confirm':
            return redirect('menu:review_confirm', store_id=menu.store.id, menu_id=menu.id)

        return redirect(request.META.get('HTTP_REFERER', '/'))