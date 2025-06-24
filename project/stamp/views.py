from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stamp.models import RiceMap, RiceGrain, Riceball


def rice_map_main(request):
    return render(request, 'stamp/rice_map_main.html')


@login_required(login_url='/accounts/login/')
def rice_map(request):
    user_profile = request.user.profile
    current_rice_map = RiceMap.objects.filter(owner=user_profile).order_by('-created_at').first()

    if current_rice_map:
        rice_grains = current_rice_map.rice_grains.order_by('created_at')
        riceballs = current_rice_map.riceballs.order_by('-created_at')
        riceball_count = Riceball.objects.filter(rice_map__owner=user_profile).count()
        past_rice_maps = RiceMap.objects.filter(owner=user_profile).exclude(id=current_rice_map.id).order_by('-created_at')
        past_riceballs = Riceball.objects.filter(rice_map__owner=user_profile,rice_map__finished_at__isnull=False).order_by('-created_at')
    else:
        rice_grains = []
        riceballs = []
        riceball_count = 0
        past_rice_maps = []
        past_riceballs = []

    total_point = Riceball.objects.filter(rice_map__owner=user_profile).count() * 50

    context = {
        'rice_grains': rice_grains,
        'current_rice_map': current_rice_map,
        'riceballs': riceballs,
        'riceball_count': riceball_count,
        'total_point': total_point,
        'past_rice_maps': past_rice_maps,
        'past_riceballs': past_riceballs, 
    }

    return render(request, 'stamp/rice_map.html', context)
