from django.shortcuts import render
from .models import User, Activities, LikeCount, LikeRecord, ParCount, ParRecord
from django.http import JsonResponse


def successresponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)


def successdianzan(par_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['par_num'] = par_num
    return JsonResponse(data)

def errorresponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like_change(request):
    act_id = request.GET.get('act_id')
    act = Activities.objects.get(id=act_id)
    if request.session.get('is_login'):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
    else:
        return errorresponse(400, '请先登录')

    if request.GET.get('is_like') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(user=user,act=act)
        if created:
            # 未点赞
            like_count, created = LikeCount.objects.get_or_create(act=act)
            like_count.liked_num += 1
            like_count.save()
            return successresponse(like_count.liked_num)
        else:
            return errorresponse(402, '已点赞')
    else:
        if LikeRecord.objects.filter(user=user,act=act):
            #已点赞，可取消
            like_record = LikeRecord.objects.get(user=user,act=act)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(act=act)
            if not created:
                #有数据
                like_count.liked_num -= 1
                like_count.save()
                return successresponse(like_count.liked_num)
            else:
                return errorresponse(404, '没有数据')
        else:
            #取消过了
            return errorresponse(403,'不能重复取消')

def par_change(request):
    act_id = request.GET.get('act_id')
    is_par = request.GET.get('is_par')
    act = Activities.objects.get(id=act_id)
    if request.session.get('is_login'):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
    else:
        return errorresponse(400, '请先登录')

    if is_par == 'true':
        par_record, created = ParRecord.objects.get_or_create(act=act, user=user)
        if created:
            par_count, created = ParCount.objects.get_or_create(act=act)
            par_count.par_num += 1
            par_count.save()
            return successdianzan(par_count.par_num)
        else:
            return errorresponse(402, '已订阅')
    else:
        if ParRecord.objects.filter(act=act,user=user):
            par_record = ParRecord.objects.get(act=act, user=user)
            par_record.delete()
            par_count, created = ParCount.objects.get_or_create(act=act)
            if not created:
                par_count.par_num -= 1
                par_count.save()
                return successdianzan(par_count.par_num)
            else:
                return errorresponse(404, 'data error')
        else:
            return errorresponse(403,'未订阅')

