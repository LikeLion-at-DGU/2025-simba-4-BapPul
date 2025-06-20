from django.shortcuts import render, get_object_or_404
from .models import Store, Menu

def store_detail(request, store_id, menu_id):
    store = get_object_or_404(Store, id=store_id)
    menus = Menu.objects.filter(store=store)
    selected_menu = get_object_or_404(Menu, id=menu_id, store=store)

    return render(request, 'menu/store_detail.html', {
        'store': store,
        'menus': menus,
        'selected_menu': selected_menu,  # 강조 표시용
    })
