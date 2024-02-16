from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    
    fieldsets=UserAdmin.fieldsets+(
        (None,{'fields':('phone_number','gender', "profile_picture")}),
    )
    add_fieldsets=UserAdmin.add_fieldsets+(
        (None,{'fields':('phone_number','gender', "profile_picture")}),
    )
    
    list_display=['username','is_staff','phone_number','gender']
    list_display_links=['username','is_staff','phone_number','gender']
        
admin.site.register(CustomUser,CustomUserAdmin)