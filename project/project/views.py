# project/views.py

from django.shortcuts import redirect, render

def root_redirect_view(request):
    return redirect('accounts:start')
    #if request.user.is_authenticated:
        #return redirect('search:home')  # 로그인한 경우
    #else:
        #return redirect('accounts:start')  # 로그인 안 한 경우
