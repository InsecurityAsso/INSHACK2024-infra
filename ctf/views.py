from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


import base64, uuid, traceback

from inshack.settings import DEBUG
from contrib.mail import send_mail
from contrib.MarkdownRenderer import markdown_to_html

from ctf.models import player
from ctf.forms import *

TOKENS = {}

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(username=email, password=password)

        # check if the user is verified
        if user is not None and user.is_verified is False:
            messages.error(request, "Votre compte n'a pas encore été vérifié par notre équipe. Vous recevrez un email lorsque votre compte sera vérifié. Si vous ne recevez pas d'email d'ici 72h, <a href='contact'>contactez-nous</a>.")
            return render(request, 'user_mgmt/login.html')

        # if the user is authenticated, log him in
        elif user is not None and user.is_verified is True:
            # login the user
            login(request, user)
            print("authenticated")
            return redirect('personal_space')

            
        else:
            messages.error(request, "L'email ou le mot de passe est incorrect.")
            return render(request, 'user_mgmt/login.html')
    else:
        # get the next url
        next = request.GET.get('next')
        return render(request, f'user_mgmt/login.html{"?next="+next if next is not None else ""}')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        
        # make sure email is not used yet
        if player.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée, merci d'en choisir une autre.")
            return redirect('index')

        token = str(uuid.uuid4().hex)
        # store token in TOKENS dict
        TOKENS[email] = token

        link = f"http://localhost:8000/register/verified/{base64.b64encode(email.encode('utf-8')).decode('utf-8')}/{token}"

        send_mail(email, 'Email de confirmation', loader.render_to_string('mails/verify_email.html', {'title': 'Email de confirmation', 'link': link}))
        
        messages.success(request, "Email envoyé, il devrait arriver d'ici 5 à 10 minutes. Soyez patient et buvez un café !<br>Si vous ne le recevez pas après 10 minutes, vérifiez vos spams.<br>Si cela ne résout pas le problème, <a href='contact'>contactez-nous</a>.")
        return redirect('index')
    
    return render(request, 'user_mgmt/register.html')

def register_verified(request, email, token):
    try:
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
            messages.error(request, "Le lien de confirmation est invalide ou a expiré, merci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
            return redirect('index')
        form = playerRegistrationForm(initial={'email': email, 'username': email})
        return render(request, 'user_mgmt/register_verified.html', {'form': form, 'email': email})
    except Exception as e:
        print(e, traceback.print_exc())
        # send message and be a teapot
        messages.error(request, "Le lien de confirmation est invalide ou a expiré, erci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
        return redirect('teapot')


def create_account(request):
    try:
        if request.method == 'POST':
            form = playerRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                # get the mail
                form.instance.username = form.instance.email = request.POST.get('email')

                # hash the password
                form.instance.set_password(form.cleaned_data.get('password'))

                # save the form
                form.save()
                messages.success(request, "Votre compte est en cours de vérification par notre équipe. Vous recevrez un email lorsque votre compte sera vérifié. Si vous ne recevez pas d'email d'ici 72h, <a href='contact'>contactez-nous</a>.")
                return redirect('index')
            else:
                messages.error(request, "Une erreur est survenue lors de la création de votre compte. Merci de réessayer. Si le problème persiste, <a href='contact'>contactez-nous</a>.")
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors de la création de votre compte : {e}. Merci de réessayer. Si le problème persiste, <a href='contact'>contactez-nous</a>.")
        print(e)
        traceback.print_exc()
    return redirect('index')

@user_passes_test(lambda u: u.is_staff, login_url='login')
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
            send_mail(user.email, 'Votre participation a été refusée.', loader.render_to_string('mails/player_refused.html', {'title': 'Votre compte a été refusé', 'player': user, 'reason': message}))
            
            # delete the player
            player.objects.filter(id=user_id).delete()

    
    # get all players that are not verified yet
    players = player.objects.filter(is_verified=False, is_staff=False, is_superuser=False)

    # return the template with the players
    return render(request, 'user_mgmt/manual_verify.html', {'users': players})


@login_required(login_url='login')
def myspace(request):
    if request.method == 'POST':
        # récupérer les données du formulaire
        form = updateProfile(request.POST, request.FILES, instance=player.objects.get(id=request.user.id))
        if form.is_valid():
            # mise à jour de la biographie de l'utilisateur
            pic = list(request.FILES.keys())  # Convertir les clés en une liste
            print(pic)
            new_bio = form.cleaned_data.get('biography')
            new_picture = form.cleaned_data.get('profile_picture')
            print(new_bio, new_picture)
            # imprimer la requête au format texte
            form.save()
            messages.success(request, "Votre profil a bien été mis à jour.")
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de votre profil. Merci de réessayer. Si le problème persiste, <a href='contact'>contactez-nous</a>.")

    bio = request.user.biography
    formatted_bio = markdown_to_html(bio) if bio is not None else "[...]"
    form = updateProfile(initial={'biography': request.user.biography})
    return render(request, 'user_space/personnal_space.html', {'user': request.user, 'bio': formatted_bio, 'form': form})


def teapot(request):
    return render(request, 'errors/418.html')