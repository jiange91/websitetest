from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from activities.models import Groups, Activities, GroupConfirmString
from accounts.models import User
from django.urls import reverse
from activities.forms import ActivitiesForm, GroupsForm
from django.core.exceptions import ObjectDoesNotExist
import hashlib
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from accounts.forms import LoginForm


def success(likecount):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = likecount
    return JsonResponse(data)


def error(message):
 data = {}
 data['status'] = 'ERROR'
 data['message'] = message
 return JsonResponse(data)


def hash_code(s, salt='confirm'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(group):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(group.group_name, now)
    GroupConfirmString.objects.create(code=code, group=group)
    return code


def send_group_email(email, code, username, user_id, group_name):
    subject = 'From Miunottingham'
    text_content = 'If you see this message, it tells that your email server does not support HTML content'
    html_content = '''
                    <p>Hello {}, you are trying to register a group: {}</p>
                    <p><a href="http://localhost:8000/miunottingham/groupconfirm/{}/{}" target=blank>
                     you must to click this link to confirm your group</a></p>
                    <p>Have fun, and don't hesitate to contact us with your feedback</p>
                    <p>This link lasts for {} days</p>'''.format(username, group_name, code, user_id, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def main_page(request):
    activities = Activities.objects.order_by("-pub_date", "-begin")
    return render(request, 'miunottingham/test_main_page.html', locals())


def groups(request):
    group_list = Groups.objects.all()
    context = {'group_list': group_list}
    return render(request, 'miunottingham/groups.html', context)


def group_acts(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    activities = group.activities_set.all()
    group_name = group.group_name
    if request.session.get('is_login'):
        id = request.session.get('user_id')
        user = User.objects.get(id=id)
        if user.groups_set.filter(user_id=id):
            if user.groups_set.get(user_id=id).id == group_id and user.groups_set.get(user_id=id).has_confirmed:
                notice = "your_group"
    return render(request, 'miunottingham/test_group_acts.html', locals())


def details(request, act_id):
    activity = Activities.objects.get(id=act_id)
    group = activity.group_name
    authenticated = request.session.get('is_login')
    form = LoginForm()
    if authenticated:
        id = request.session.get('user_id')
        user = User.objects.get(id=id)
        if user.groups_set.filter(user_id=id):
            if user.groups_set.get(user_id=id).id == group.id and user.groups_set.get(user_id=id).has_confirmed:
                notice = "your_group"
    return render(request, 'miunottingham/maotou_details_login.html', locals())


def new_activity(request, group_id):
    group_name = Groups.objects.get(id=group_id).group_name
    if request.method != 'POST':
        form = ActivitiesForm()
    else:
        form = ActivitiesForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.group_name = Groups.objects.get(id=group_id)
            activity.save()
            return HttpResponseRedirect(reverse('miunottingham:group_acts',args=[group_id]))
    return render(request, 'miunottingham/new_activity.html', locals())


def edit_activity(request, act_id):
    activity = Activities.objects.get(id=act_id)
    group = activity.group_name
    if request.method != 'POST':
        form = ActivitiesForm(instance=activity)
    else:
        form = ActivitiesForm(instance=activity, data=request.POST)
        if form.is_valid():
            form.save()
            if request.FILES.get('img'):
                activity.img = request.FILES.get('img')
                activity.save()
            return HttpResponseRedirect(reverse('miunottingham:details',args=[act_id]))
    return render(request, 'miunottingham/edit_activity.html', locals())


def new_group(request, userid):
    if request.method == "POST":
            group_name = request.POST.get('group_name', None)
            img = request.FILES.get('avatar', None)
            if Groups.objects.filter(group_name=group_name):
                message = 'Group already exists'
                return render(request, 'miunottingham/test_register.html', locals())
            group = Groups()
            group.group_name = group_name
            group.img = img
            user = User.objects.get(id=userid)
            username = user.username
            group.user = user
            group.has_confirmed = True
            group.save()

            message = 'you have successfully registered a group' + ': ' + group_name
            return render(request,'miunottingham/confirm.html',locals())
    form = GroupsForm()
    return render(request, 'miunottingham/test_register.html', locals())


def groupconfirm(request, code, user_id):
    user = User.objects.get(id=user_id)
    message = None
    try:
        confirmation = GroupConfirmString.objects.get(code=code)
    except ObjectDoesNotExist:
        message = 'Invalid confirmation'
        return render(request, 'miunottingham/confirm.html', locals())

    c_time = confirmation.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirmation.delete()
        confirmation.group.delete()
        message = 'Your email link has expired, please try to register again'
        return render(request, 'miunottingham/confirm.html', locals())
    else:
        confirmation.group.has_confirmed = True
        confirmation.group.save()
        confirmation.delete()
        message = 'You have successfully register a group.'
        return render(request, 'miunottingham/confirm.html', locals())


def delete_act(request, act_id):
    activity = Activities.objects.get(id=act_id)
    group = activity.group_name
    activity.delete()
    return HttpResponseRedirect(reverse('miunottingham:group_acts',args=[group.id]))




