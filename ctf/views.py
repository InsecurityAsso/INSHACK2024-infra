from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

import base64, uuid

from contrib.mail import send_mail
from inshack.settings import DEBUG

from ctf.models import player
from django.contrib.admin.views.decorators import staff_member_required

TOKENS = {}

# Create your views here.
def index(request, banner=None):
    if banner:
        return render(request, 'index.html', {'banner': banner})
    return render(request, 'index.html')

def login(request):
    print(request.user, request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'user_mgmt/login.html')

def register(request):
    if request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        print(email)
        token = str(uuid.uuid4().hex)
        # store token in TOKENS dict
        TOKENS[email] = token

        link = f"http://localhost:8000/register/verified/{base64.b64encode(email.encode('utf-8')).decode('utf-8')}/{token}"

        send_mail(email, 'Email de confirmation', loader.render_to_string('mails/verify_email.html', {'title': 'Email de confirmation', 'link': link}))
        
        messages.success(request, "Email envoyé, il devrait arriver d'ici 5 à 10 minutes. Soyez patient et buvez un café !<br>Si vous ne le recevez pas après 10 minutes, vérifiez vos spams.<br>Si cela ne résout pas le problème, <a href='contact'>contactez-nous</a>.")
        return redirect('index')
    
    return render(request, 'user_mgmt/register.html')

def register_verified(request, email, token):
    # decode token with base64 to retrerive email
    if email != 'test':
        email = base64.b64decode(email).decode('utf-8')
    # check if token is valid
    if DEBUG is True and email == 'test' and token == 'test':
        email = 'matheo.d91@gmail.com'
    elif TOKENS.get(email) == token:
        # remove token from TOKENS dict
        del TOKENS[email]
    else:
        messages.error(request, "Le lien de confirmation est invalide ou a expiré, erci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
        return redirect('index')
    return render(request, 'user_mgmt/register_verified.html', {'email': email})

def create_account(request):
    if request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        school = request.POST.get('school_name')
        id_doc = request.POST.get('student_id') # file type input

        # create the player
        try :
            new_player = player.objects.create_user(username=email,email=email, password=password, first_name=first_name, last_name=last_name, school=school, id_card=id_doc)
            new_player.save()
            messages.success(request, "Votre compte a bien été créé, vous pouvez maintenant vous connecter.")
        except Exception as e:
            messages.error(request, "Une erreur est survenue lors de la création de votre compte, merci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
            print(e)
        return redirect('index')


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def user_checkup(request):
    if request.method == 'POST':
        # get form data
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        message = request.POST.get('message')

        print(user_id, status, message)

        # if the player is accepted, set is_verified to True
        if status == 'accepted':

            player.objects.filter(id=user_id).update(is_verified=True)
        
            
            # send email to the player
            user = player.objects.get(id=user_id)
            send_mail(user.email, 'Votre participation a été acceptée.', loader.render_to_string('mails/player_accepted.html', {'title': 'Votre compte a été accepté', 'player': user}))        


        # if the player is rejected, ssend him an email with the reason and delete his account
        elif status == 'rejected':
            # send email to the player
            user = player.objects.get(id=user_id)
            send_mail(user.email, 'Votre participation a été refusée.', loader.render_to_string('mails/player_accepted.html', {'title': 'Votre compte a été refusé', 'player': user, 'message': message}))
            
            # delete the player
            player.objects.filter(id=user_id).delete()

    
    # get all players that are not verified yet
    players = player.objects.filter(is_verified=False)

    # return the template with the players
    return render(request, 'user_mgmt/manual_verify.html', {'users': players})

def user_checkup_done(request):
    return redirect('user_checkup')
