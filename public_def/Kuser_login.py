from django.contrib.auth import authenticate
from django.contrib.auth import login

def user_login(request):
    isuserlogin = False
    error_message = ''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request,user)
        isuserlogin = True
    else:
        isuserlogin = False
        error_message = 'Wrong login information!'
    return isuserlogin, error_message
