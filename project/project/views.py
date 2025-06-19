# project/views.py

from django.shortcuts import redirect

def root_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('search:home')  # 로그인한 경우
    else:
        return redirect('accounts:login')  # 로그인 안 한 경우
