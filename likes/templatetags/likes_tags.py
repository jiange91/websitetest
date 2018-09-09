from django import template
from ..models import LikeCount, Activities, LikeRecord, ParCount, ParRecord


register = template.Library()

@register.simple_tag
def get_like_count(obj):
    act = Activities.objects.get(id=obj.id)
    like_count, created = LikeCount.objects.get_or_create(act=act)
    return like_count.liked_num


@register.simple_tag
def get_like_status(user, authenticated, obj):
    act = Activities.objects.get(id=obj.id)
    if not authenticated:
        return ''
    if LikeRecord.objects.filter(act=act, user=user):
        return 'active'
    else:
        return ''

@register.simple_tag
def get_par_count(obj):
    act = Activities.objects.get(id=obj.id)
    par_count, created = ParCount.objects.get_or_create(act=act)
    return par_count.par_num


@register.simple_tag
def get_par_status(obj, user, authenticated):
    act = Activities.objects.get(id=obj.id)
    if not authenticated:
        return ''
    else:
        if ParRecord.objects.filter(act=act, user=user):
            return 'active2'
        else:
            return ''
