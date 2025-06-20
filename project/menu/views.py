from django.shortcuts import render, get_object_or_404
from .models import Store, Menu , Review ,VisitLog

def store_detail(request, store_id, menu_id):
    store = get_object_or_404(Store, id=store_id)
    menus = Menu.objects.filter(store=store)
    selected_menu = get_object_or_404(Menu, id=menu_id, store=store)

    return render(request, 'menu/store_detail.html', {
        'store': store,
        'menus': menus,
        'selected_menu': selected_menu,  # 강조 표시용
    })

def store_review_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    # 이 음식점의 모든 리뷰 (연결된 메뉴들에 달린 리뷰들 포함)
    reviews = Review.objects.filter(menu__store=store).select_related('menu', 'writer')

    return render(request, 'menu/store_review_list.html', {
        'store': store,
        'reviews': reviews,
    })
    
def store_location(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    user = request.user.profile

    menu_id = request.GET.get('menu_id')
    menu = get_object_or_404(Menu, id=menu_id) if menu_id else None

    VisitLog.objects.create(user=user, store=store, menu=menu)

    context = {
        'store': store,
        'menu': menu,
    }
    return render(request, 'menu/store_location.html', context)


def store_review(request, store_id, menu_id):
    store = get_object_or_404(Store, id = store_id)
    menu = get_object_or_404(Menu, id = menu_id)