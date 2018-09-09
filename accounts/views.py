from django.shortcuts import render
from accounts.models import User, ConfirmString
from activities.models import Groups
from django.http import JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect
from accounts.forms import LoginForm, RegisterForm, UserForm, PswForm
import hashlib
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def hash_code(s, salt='confirm'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code, username):
    subject = 'From Miunottingham'
    text_content = 'If you see this message, it tells that your email server does not support HTML content'
    html_content = '''
                    <p>Hellow {}, Thanks for signing up with Miunottingham.<p/>
                    <p><a href="http://localhost:8000/accounts/confirm/{}" target=blank>
                    You must follow this link to activate your account</a></p>
                    <p>Have fun, and don't hesitate to contact us with your feedback</p>
                    <p>This link lasts for {} days</p>'''.format(username, code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject,  text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_psw_email(email, code, username):
    subject = 'From Miunottingham'
    text_content = 'If you see this message, it tells that your email server does not support HTML content'
    html_content = '''
                    <p>Hello {}, you are trying to modify the password for your account in Miunottingham. If it's not
                    your purpose, please contact our technical staff.</p>
                    <p><a href="http://localhost:8000/accounts/pswchange/{}" target=blank>
                     you can click this link to edit your password</a></p>
                    <p>Have fun, and don't hesitate to contact us with your feedback</p>
                    <p>This link lasts for {} days</p>'''.format(username, code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def index(request):
    pass
    return render(request, 'accounts/index.html')


def login_test(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']
            referer = request.META.get('HTTP_REFERER',reverse('miunottingham:main_page'))
            if message == 'Login successful':
                user = form.cleaned_data['user']
                request.session['is_login'] = True
                request.session['user_name'] = user.username
                request.session['user_id'] = user.id
                return redirect(request.GET.get('from', reverse('miunottingham:main_page')))
    else:
        form = LoginForm()
    return render(request, 'accounts/maotouying_test.html', locals())


def login_for_medal(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        message = form.cleaned_data['message']
        if message == 'Login successful':
            user = form.cleaned_data['user']
            request.session['is_login'] = True
            request.session['user_name'] = user.username
            request.session['user_id'] = user.id
            data = {}
            data['status'] = 'SUCCESS'
        else:
            data = {}
            data['status'] = 'ERROR'
        return JsonResponse(data)


def login(request):
        if request.session.get('is_login'):
            return HttpResponseRedirect(reverse('miunottingham:main_page'))
        if request.method == "POST":
                    email = request.POST.get('email', None)
                    password = request.POST.get('password', None)
                    if email and password:
                        email = email.strip()
                        try:
                            user = User.objects.get(email=email)
                            if not user.has_confirmed:
                                message = 'Your account is not activated yet, please check your email and find the link'
                                return render(request, 'accounts/login_test.html', locals())
                            if user.password == hash_code(password):
                                request.session['is_login'] = True
                                request.session['user_name'] = user.username
                                request.session['user_id'] = user.id
                                return redirect(request.GET.get('from', reverse('miunottingham:main_page')))
                            else:
                                message = "Wrong password"
                                return render(request, 'accounts/login_test.html', locals())
                        except ObjectDoesNotExist:
                            message = "Invalid account"
                            return render(request, 'accounts/login_test.html', locals())
        else:
            return render(request, 'accounts/login_test.html')


def logout(request):
    if not request.session.get('is_login'):
        return redirect(request.GET.get('from', reverse('miunottingham:main_page')))
    request.session['is_login'] = False
    request.session['user_name'] = None
    request.session['user_id'] = None
    return redirect(request.GET.get('from', reverse('miunottingham:main_page')))


def register(request):
    if request.session.get('is_login'):
        return HttpResponseRedirect(reverse('miunottingham:main_page'))
    if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                email = form.cleaned_data['email']
                if User.objects.filter(username=username):
                    message = 'username already exists'
                    return render(request, 'accounts/register.html', locals())
                else:
                    if User.objects.filter(email=email):
                        message = 'email address already exists'
                        return render(request, 'accounts/register.html', locals())
                    else:
                        if password1 != password2:
                            message = 'password does not match'
                            return render(request, 'accounts/register.html', locals())
                new_user = User()
                new_user.username = username
                # encrypt password
                new_user.password = hash_code(password2)
                new_user.email = email
                new_user.has_confirmed = True
                new_user.save()

                # code = make_confirm_string(new_user)
                # send_email(email, code, new_user.username)
                # message = 'Please activate your account through email confirmation'
                # return render(request, 'miunottingham/confirm.html', locals())
            return render(request, 'accounts/login_test.html')
    form = RegisterForm()
    return render(request, 'accounts/register.html', locals())


def confirm(request, code):
    message = None
    try:
        confirmation = ConfirmString.objects.get(code=code)
    except ObjectDoesNotExist:
        message = 'Invalid confirmation'
        return render(request, 'accounts/confirm.html', locals())

    c_time = confirmation.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirmation.delete()
        confirmation.user.delete()
        message = 'Your email link has expired, please sign up again'
        return render(request, 'accounts/confirm.html', locals())
    else:
        confirmation.user.has_confirmed = True
        confirmation.user.save()
        confirmation.delete()
        message = 'Thanks for joining us, Please login'
        return render(request, 'accounts/confirm.html', locals())


def userinfo(request):
    if not request.session.get('is_login'):
        return HttpResponseRedirect(reverse('accounts:login'))
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    # if user.groups_set.filter(user_id=userid):
    #     group = user.groups_set.get(user_id=userid)
    #     isgroup = group.has_confirmed
    #     group_name = group.group_name
    # else:
    #     isgroup = False
    if request.method != 'POST':
        form = UserForm(instance=user)
    else:
        form = UserForm(instance=user, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if (user.username != username) and (User.objects.filter(username=username)):
                message = 'username already exists'
                return render(request,'accounts/userinfo.html', locals())
            else:
                if (User.objects.filter(email=email)) and (user.email != email):
                    message = 'email address already exists'
                    return render(request, 'accounts/userinfo.html', locals())
            user.username = username
            user.email = email
            user.save()
            request.session['user_name'] = username
            notice = 'you have successfully edit your information'
    return render(request, 'accounts/userinfo.html',locals())


def pswchange_request(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    request.session['is_login'] = False
    request.session['user_name'] = None
    request.session['user_id'] = None
    email = user.email
    username = user.username
    code = make_confirm_string(user)
    send_psw_email(email, code, username)
    message = 'Please confirm the request via the link in your email'
    return render(request, 'accounts/confirm.html', locals())


def pswchange(request, code):
    message = None
    try:
        confirmation = ConfirmString.objects.get(code=code)
    except ObjectDoesNotExist:
        message = 'Invalid confirmation'
        return render(request, 'accounts/confirm.html', locals())

    c_time = confirmation.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirmation.delete()
        message = 'Your email link has expired, please try again'
        return render(request, 'accounts/confirm.html', locals())
    else:
        if request.method == "POST":
            form = PswForm(request.POST)
            if form.is_valid():
                user = confirmation.user
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if hash_code(password1) == user.password:
                    message = "The new password can't be the same with the old one"
                    return render(request, 'accounts/pswchange.html', locals())
                else:
                    if password1 != password2:
                        message = 'password does not match'
                        return render(request, 'accounts/pswchange.html', locals())
                # encrypt password
                user.password = hash_code(password2)
                user.save()
                message = 'You have successfully change your password, please sign in'
                confirmation.delete()
                return render(request, 'accounts/confirm.html', locals())
        form = PswForm()
        return render(request, 'accounts/pswchange.html', locals())


def pswforget(request):
    if request.method == "POST":
        info = request.POST.get('input')
        info = info.strip()
        if User.objects.filter(email=info):
            user = User.objects.get(email=info)
            username = user.username
            code = make_confirm_string(user)
            send_psw_email(info, code, username)
            message = 'Please confirm the request via the link in your email'
            return render(request, 'accounts/confirm.html', locals())  # public warning page
        else:
            message = "Unregistered account"
            return render(request, 'accounts/pswforget.html',locals())
    return render(request, 'accounts/pswforget.html')



