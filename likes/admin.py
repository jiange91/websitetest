from django.contrib import admin
from .models import LikeRecord, LikeCount, ParRecord, ParCount

admin.site.register(LikeCount)
admin.site.register(LikeRecord)
admin.site.register(ParCount)
admin.site.register(ParRecord)