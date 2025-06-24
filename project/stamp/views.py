from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stamp.models import RiceMap, RiceGrain, Riceball


def rice_map_main(request):
    return render(request, 'stamp/rice_map_main.html')

# ===== 기존 코드 (보존용, 주석 처리) =====
# 테스트할 때 로그인 안되도 접근 가능하게 하기 위해서 일단!
# def rice_map(request):
#     if not request.user.is_authenticated:
#         return render(request, 'stamp/rice_map.html', {
#             'rice_grains': [],
#             'current_rice_map': None,
#             'riceball_count': 0,
#             'total_point': 0,
#             'past_rice_maps': [],
#         })

#     user_profile = request.user.profile
#     current_rice_map = RiceMap.objects.filter(owner=user_profile).order_by('-created_at').first()

#     rice_grains = current_rice_map.rice_grains.order_by('created_at')
#     riceballs = current_rice_map.riceballs.order_by('-created_at')

#     past_rice_maps = RiceMap.objects.filter(owner=user_profile).exclude(id=current_rice_map.id).order_by('-created_at')

#     context = {
#         'rice_grains': rice_grains,
#         'current_rice_map': current_rice_map,
#         'riceballs': riceballs,
#         'riceball_count': riceballs.count(),
#         'total_point': Riceball.objects.filter(rice_map__owner=user_profile).count() * 2000,
#         'past_rice_maps': past_rice_maps,
#     }
#     return render(request, 'stamp/rice_map.html', context)


# ===== 최종 반영 코드 (login_required + 예외 처리 포함) =====

@login_required(login_url='/accounts/login/')
def rice_map(request):
    user_profile = request.user.profile
    current_rice_map = RiceMap.objects.filter(owner=user_profile).order_by('-created_at').first()

    if current_rice_map:
        rice_grains = current_rice_map.rice_grains.order_by('created_at')
        riceballs = current_rice_map.riceballs.order_by('-created_at')
        riceball_count = riceballs.count()
        past_rice_maps = RiceMap.objects.filter(owner=user_profile).exclude(id=current_rice_map.id).order_by('-created_at')
    else:
        rice_grains = []
        riceballs = []
        riceball_count = 0
        past_rice_maps = []

    total_point = Riceball.objects.filter(rice_map__owner=user_profile).count() * 2000

    context = {
        'rice_grains': rice_grains,
        'current_rice_map': current_rice_map,
        'riceballs': riceballs,
        'riceball_count': riceball_count,
        'total_point': total_point,
        'past_rice_maps': past_rice_maps,
    }

    return render(request, 'stamp/rice_map.html', context)
