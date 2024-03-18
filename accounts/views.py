from django.contrib.auth.models import User
from .models import Profile  # Import Profile model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from pathlib import Path
from django.contrib import messages
from dotenv import load_dotenv
load_dotenv()


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/activate_account_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')  # Retrieve email address from the form
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Create the profile if it doesn't exist and the account is verified
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user, verified=True)
        else:
            user.profile.verified = True
            user.profile.save()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Authenticate the user
        messages.success(request, "Account Activation success!")
        return redirect('home')  # Replace 'home' with your desired URL after activation
    else:
        messages.error(request, "Account Activation failed!")
        return render(request, 'accounts/account_activation_invalid.html')
def login(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to a different page
        
        return redirect('home')  # Replace 'home' with your desired URL for authenticated users
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Logged in Successfully!")
            return redirect('home')  # Replace 'home' with your desired URL after login
    else:
        
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, "logged out successfully!")
    return redirect('home')  # Replace 'home' with your desired URL after logout


def custom_google_login(request):
    # Construct the Google authentication URL with required parameters
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=794428946338-7pi1dd6v68nuo7v9nbijl1apj3cl1tmb.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F&scope=profile%20email&response_type=code&state=auNOK6lOi3sPqSlz&access_type=online&service=lso&o2v=2&theme=glif&ddm=0&flowName=GeneralOAuthFlow"
    
    return redirect(google_auth_url)