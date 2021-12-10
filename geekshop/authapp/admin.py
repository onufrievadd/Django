from django.contrib import admin

# Register your models here.
from authapp.models import User
from baskets.admin import BasketAdmin
from baskets.models import Basket

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)