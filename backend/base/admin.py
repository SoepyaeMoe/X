from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Heart)