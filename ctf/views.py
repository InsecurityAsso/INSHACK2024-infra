from django.shortcuts import render

import base64

from contrib.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'user_mgmt/login.html')

def register(request):
    if request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        print(email)
        send_mail(email, 'Email de confirmation')
    return render(request, 'user_mgmt/register.html')

def register_verified(request, token):
    # decode token with base64 to retrerive email
    email = base64.b64decode(token).decode('utf-8')
