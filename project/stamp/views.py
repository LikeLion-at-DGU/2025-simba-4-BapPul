from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from stamp.models import RiceMap, RiceGrain, Riceball

# @login_required
# def rice_map(request):
#     user_profile = request.user.profile
#     rice_map, _ = RiceMap.objects.get_or_create(owner=user_profile)

#     rice_grains = rice_map.rice_grains.order_by('created_at')
#     riceballs = rice_map.riceballs.order_by('-created_at')

#     context = {
#         'rice_grains': rice_grains,
#         'riceballs': riceballs,
#         'riceball_count': riceballs.count(),
#     }
#     return render(request, 'stamp/rice_map.html', context)

#테스트할 때 로그인 안되도 접근 가능하게 하기 위해서
def rice_map_main(request):
    if not request.user.is_authenticated:
        # 로그인 안 된 사용자에겐 빈 값 전달
        context = {
            'rice_grains': [],
            'riceballs': [],
            'riceball_count': 0,
        }
        return render(request, 'stamp/rice_map.html', context)

    user_profile = request.user.profile
    rice_map, _ = RiceMap.objects.get_or_create(owner=user_profile)

    rice_grains = rice_map.rice_grains.order_by('created_at')
    riceballs = rice_map.riceballs.order_by('-created_at')

    context = {
        'rice_grains': rice_grains,
        'riceballs': riceballs,
        'riceball_count': riceballs.count(),
    }
    return render(request, 'stamp/rice_map_main.html', context)

