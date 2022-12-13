from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from accounts.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                if not User.objects.get(email=email).is_active:
                    messages.info(
                        request, 'This account has already been created but the email has not been verified. Another confirmation email has been sent. Please check your inbox.')
                    user = User.objects.get(email=email)
                else:
                    messages.info(
                        request, 'There is already an account with this email, please login.')
                    return redirect('login')
            else:
                user = User.objects.create_user(username=email, password=password,
                                                email=email, first_name=first_name, last_name=last_name, is_active=False)
                user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your RestReviews account.'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('login')

        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)

    else:
        return render(request, 'accounts/registration.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request, user=None):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']

        if not user:
            user = auth.authenticate(username=email, password=password)

        if user:
            auth.login(request, user)
            return redirect('home')

        # if not user.is_active:
        #     messages.info(request, 'Email has not be verified yet. Please check your email for verification instructions.')
        else:
            if not User.objects.get(email=email).is_active:
                messages.info(request, 
                    "This account has already been created but the email has not been verified. To send another verification email, please resubmit your registration.")
            else:
                messages.info(request, 'Invalid Email or Password. ')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'restreviews.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password/password_reset.html", context={"password_reset_form": password_reset_form})
