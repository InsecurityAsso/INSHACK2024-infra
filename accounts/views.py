from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


import traceback, base64, os

from inshack.settings import DEBUG, MEDIA_ROOT

from accounts.models import player as player_model, token as token_model, team as team_model
from accounts.forms import *

from contrib.mail import send_mail
from contrib.MarkdownRenderer import markdown_to_html
from contrib.token_generator import generate_token


# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.user.is_authenticated and DEBUG is False:
        return redirect('personal_space')
    
    if request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(username=email, password=password)

        # check if the user is verified
        if user is not None and user.is_verified is False:
            messages.error(request, "Votre compte n'a pas encore été vérifié par notre équipe. Vous recevrez un email lorsque votre compte sera vérifié. Si vous ne recevez pas d'email d'ici 72h, <a href='contact'>contactez-nous</a>.")
            return redirect('index')

        # if the user is authenticated, log him in
        elif user is not None and user.is_verified is True:
            # login the user
            login(request, user)
            print("authenticated")
            # if there is a next url, redirect to it
            next = request.POST.get('next')

            print([next])
            
            if next and next != 'None':
                # redirect to the next url with format http://localhost:8000{next}
                return redirect(next)
            else:
                return redirect('personal_space')

            
        else:
            messages.error(request, "L'email ou le mot de passe est incorrect.")
            return render(request, 'user_mgmt/login.html')
    else:
        # get the next url
        next = request.GET.get('next')
        return render(request, f'user_mgmt/login.html', {'next': next})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def register(request):
    # if user is already logged in, redirect him to his personal space
    if request.user.is_authenticated:
        return redirect('personal_space')
    # handle tokenized verified link
    if request.method == 'GET':
        token = request.GET.get('token')
        if token:
            return register_verified(request, token)
    elif request.method == 'POST':
        # get form data
        email = request.POST.get('email')
        
        # make sure email is not used yet
        if player_model.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée, merci d'en choisir une autre.")
            return redirect('register')
        
        # delete all tokens for this email that have the action 'register'
        token_model.objects.filter(player_email=email, action='register').delete()

        # generate token and store it in the database, then send it through an email
        token = generate_token()
        new_token = token_model.objects.create(token=token, player_email=email, action='register')
        new_token.save()

        link = f"http://localhost:8000/register?token={token}"

        send_mail(email, 'Email de confirmation', loader.render_to_string('mails/verify_email.html', {'title': 'Email de confirmation', 'link': link}))
        
        messages.success(request, "Email envoyé, il devrait arriver d'ici 10 minutes. Soyez patient et buvez un café !<br>Si vous ne le recevez pas après ce délais, vérifiez vos spams.<br>Si cela ne résout pas le problème, <a href='contact'>contactez-nous</a>.")
        return redirect('index')
    
    return render(request, 'user_mgmt/register.html')

def register_verified(request, token):
    try:
        if DEBUG and token == 'test':
            email = 'matheo.d91@gmail.com'
        else:
            # verify the token 
            used_token = token_model.objects.filter(token=token, action='register').first()

            # token invalid
            if used_token is None:
                messages.error(request, "Le lien de confirmation est invalide ou a expiré, merci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
                return redirect('index')
            
        # token valid
        email = used_token.player_email
        token = used_token.token
        print(f"email: {email}\ntoken: {token}")
        # allow the user to create his account
        form = playerRegistrationForm(initial={'email': email, 'username': email, 'token': token})
        return render(request, 'user_mgmt/register_verified.html', {'form': form, 'email': email, 'token': token})
    
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

                # get the token
                token = request.POST.get('token')

                # hash the password
                form.instance.set_password(form.cleaned_data.get('password'))

                # verify the token again and save create the account
                used_token = token_model.objects.filter(player_email=request.POST.get('email'), action='register', token=token).first()

                # token invalid
                if used_token is None:
                    messages.error(request, "Le lien de confirmation est invalide ou a expiré, merci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
                    return redirect('index')
                
                # token valid
                else:
                    # save the form
                    form.save()

                    # delete all tokens for this email that have the action 'register'
                    token_model.objects.filter(player_email=request.POST.get('email'), action='register').delete()

                    print("account created")

                    # send message and redirect to index
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
@login_required(login_url='login')
def user_checkup(request):
    if request.method == 'POST':
        # get form data
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        message = request.POST.get('message')

        print(user_id, status, message)

        # if the player is accepted, set is_verified to True
        if status == 'accepted':

            player_model.objects.filter(id=user_id).update(is_verified=True)
        
            
            # send email to the player
            user = player_model.objects.get(id=user_id)
            send_mail(user.email, 'Votre participation a été acceptée.', loader.render_to_string('mails/player_accepted.html', {'title': 'Votre compte a été accepté', 'player': user}))        


        # if the player is rejected, ssend him an email with the reason and delete his account
        elif status == 'rejected':
            # send email to the player
            user = player_model.objects.get(id=user_id)
            send_mail(user.email, 'Votre participation a été refusée.', loader.render_to_string('mails/player_refused.html', {'title': 'Votre compte a été refusé', 'player': user, 'reason': message}))
            
            # delete the player
            player_model.objects.filter(id=user_id).delete()

    
    # get all players that are not verified yet
    players = player_model.objects.filter(is_verified=False, is_staff=False, is_superuser=False)

    # return the template with the players
    return render(request, 'user_mgmt/manual_verify.html', {'users': players})


@login_required(login_url='login')
def myspace(request):
    if request.method == 'POST':
        form = updateProfile(request.POST, request.FILES, instance=player.objects.get(id=request.user.id))
        if form.is_valid():
            new_picture = form.cleaned_data.get('profile_picture')

            # change the profile picture name to the username encrypted in base64 (no '=')
            if new_picture is not None:
                new_picture.name = base64.b64encode(request.user.username.encode()).decode().replace('=', '') + '.' + new_picture.name.split('.')[-1]
                form.instance.profile_picture = new_picture

            # Do not update the profile picture if the user did not change it
            if new_picture is None and form.cleaned_data.get('clear_pp') is False:
                form.instance.profile_picture = player.objects.get(id=request.user.id).profile_picture
                form.save()
                messages.success(request, "Votre profil a bien été mis à jour. Si vous ne constatez pas de changement, cliquez <a href=http://localhost:8000/myspace>ici</a> pour rafraîchir la page. Si le problème persiste, videz votre cache (ctrl + F5) ou <a href='contact'>contactez-nous</a>")
                return redirect('personal_space')
            
            # If the user wants to delete the profile picture, delete it
            elif form.cleaned_data.get('clear_pp'):
                old_picture = player.objects.get(id=request.user.id).profile_picture
                if old_picture:
                    try:
                        with open(old_picture.path, 'rb'):
                            pass  # Dummy read to ensure the file is closed
                        os.remove(old_picture.path)
                    except FileNotFoundError:
                        pass  # Ignore if the file is not found

                # Set player profile_picture to EMPTY
                form.instance.profile_picture = None
                player.objects.filter(id=request.user.id).update(profile_picture=None)

            # Update the bio and the profile picture
            form.save()
            
            messages.success(request, "Votre profil a bien été mis à jour. Si vous ne constatez pas de changement, cliquez <a href=http://localhost:8000/myspace>ici</a> pour rafraîchir la page. Si le problème persiste, videz votre cache (ctrl + F5) ou <a href='contact'>contactez-nous</a>")
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de votre profil. Merci de réessayer. Si le problème persiste, <a href='contact'>contactez-nous</a>.")

    bio = request.user.biography
    formatted_bio = markdown_to_html(bio) if bio is not None else "[...]"
    form = updateProfile(initial={'biography': request.user.biography})
    return render(request, 'user_space/personnal_space.html', {'user': request.user, 'bio': formatted_bio, 'form': form})

def teapot(request):
    return render(request, 'errors/418.html')
    

def check_user(user, current_user):
    if user is not None:
        if user.id == current_user.id:
            return True
    return False

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if token:
        # confirm with password the account deletion
            return render(request, 'user_space/delete_account.html', {'token': token, 'email': request.user.email})

        else :
            return render(request, 'user_space/prompt_email.html', {'context': 'supprimer votre compte'})

    else:
        # get form data
        token = request.POST.get('token')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # if there is a token, verify the token/email/password combination and if valid, delete the account
        if token and email and password:
            
            # check if password is valid
            user = authenticate(username=request.user.email, password=password)

            if check_user(user, request.user):
                # check if token is valid
                used_token = token_model.objects.filter(token=token, player_email=email, action='delete').first()

                # token invalid
                if used_token is None:
                    messages.error(request, "Le lien de confirmation est invalide ou a expiré, merci de réessayer.<br>Si le problème persiste, <a href='contact'>contactez-nous</a>.")
                    return redirect('index')
                
                # token valid
                else:
                    # delete the player
                    player_model.objects.filter(id=request.user.id).delete()

                    # delete all tokens for this email that have the action 'delete'
                    token_model.objects.filter(player_email=email, action='delete').delete()

                    # send email to the player
                    send_mail(email, 'Votre compte a été supprimé.', loader.render_to_string('mails/account_deleted.html', {'title': 'Votre compte a été supprimé'}))

                    # send message and redirect to index
                    messages.success(request, "Votre compte a bien été supprimé.")
                    return redirect('index')
                
            # password invalid
            else:
                messages.error(request, "Le mot de passe est incorrect.")
                return render(request, 'user_space/delete_account.html', {'token': token, 'email': email})

        # if there is no token, check if the form contains an email
        # if there is an email, make sure it matches the user's email and send a token
        elif email:
            # if email matches the user's email, send a token
            if email == request.user.email:
                # delete all tokens for this email that have the action 'delete'
                token_model.objects.filter(player_email=email, action='delete').delete()

                # generate token and store it in the database, then send it through an email
                token = generate_token()
                new_token = token_model.objects.create(token=token, player_email=email, action='delete')
                new_token.save()

                link = f"http://localhost:8000/dangerzone/delete?token={token}"

                send_mail(email, 'Confirmation de suppression de compte', loader.render_to_string('mails/delete_account.html', {'title': 'Confirmation de suppression de compte', 'link': link}))
                
                messages.success(request, "Email envoyé, il devrait arriver d'ici 10 minutes. Soyez patient et buvez un café !<br>Si vous ne le recevez pas après ce délais, vérifiez vos spams.<br>Si cela ne résout pas le problème, <a href='contact'>contactez-nous</a>.")
                return redirect('personal_space')
                
            # if email does not match the user's email, send an error message and redirect to myspace
            else:
                messages.error(request, "L'email renseigné ne correspond pas à votre adresse email.")
                return render(request, 'user_space/prompt_email.html', {'context': 'supprimer votre compte'})
            
        # if there is no email, send an error message and redirect to myspace
        else:
            messages.error(request, "Une erreur est survenue. Merci de réessayer. Si le problème persiste, <a href='contact'>contactez-nous</a>.")
            return redirect('teapot')
            



@login_required(login_url='login')
def change_password(request):
    if request.method == 'GET':
        # show reset page
        pass
    else:
        # replace user password
        # then return index with success message
        pass
