from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # נוודא שהמשתמש הוא מנהל
            login(request, user)
            return render(request, 'management/admin_dashboard.html')
        else:
            return render(request, 'management/login_guide.html', {
                'error': 'שם משתמש או סיסמה שגויים'
            })
    return render(request, 'management/login_guide.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')
