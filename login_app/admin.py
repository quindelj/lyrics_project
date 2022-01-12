from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Snippit)
admin.site.register(Like)