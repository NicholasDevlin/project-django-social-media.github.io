from django.contrib import admin

from .models import User, References, Posting

# Register your models here.
admin.site.register(User)
admin.site.register(References)
admin.site.register(Posting)