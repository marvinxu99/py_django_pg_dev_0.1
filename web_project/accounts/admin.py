from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User as CustomUser
from .models import Person, Prsnl, Person_Alias, Prsnl_Alias
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Define an inline admin descriptor for Person model
# which acts a bit like a singleton
# class PersonInline(admin.TabularInline):   
class PersonAliasInline(admin.StackedInline):   
    model = Person_Alias
    can_delete = False
    verbose_name_plural = 'person alias'
    fieldsets = (
        (None, {
            'fields': ['alias', 'alias_pool_cd', 'alias_expiry_dt_tm'],
        }),
        (None, {
            'fields': ['is_active', 'active_status_cd'],
        }),
    )
    extra = 1

class PrsnlAliasInline(admin.StackedInline):   
    model = Prsnl_Alias
    can_delete = False
    verbose_name_plural = 'prsnl alias'
    fieldsets = (
        (None, {
            'fields': ['alias', 'alias_expiry_dt_tm', 'alias_pool_cd'],
        }),
        (None, {
            'fields': ['is_active', 'active_status_cd'],
        }),
    )
    extra = 0


class PersonInline(admin.StackedInline):   
    model = Person
    can_delete = False
    verbose_name_plural = 'persons'
    fieldsets = (
        (None, {
            'fields': ['name_first', 'name_middle', 'name_last', 'name_full_formatted'],
        }),
        (None, {
            'fields': ['is_active', 'active_status_cd'],
        }),
    )
    extra = 0


class PrsnlInline(admin.StackedInline):   
    model = Prsnl
    can_delete = False
    verbose_name_plural = 'personnel'
    # fieldsets = (
    #     ('Names', {
    #         'fields': ['name_first', 'name_middle', 'name_last', 'name_full_formatted'],
    #         'classes': ['wide', 'extrapretty'],   # can be 'collapse', 'wide', 'extrapretty' 
    #         'description': 'this is needed'
    #     }),
    #     ('Advanced opitons', {
    #         'fields': ['is_active', 'active_status_cd'],
    #         'classes': ['wide', 'extrapretty']
    #     }),
    # )
    fieldsets = (
        (None, {
            'fields': ['name_first', 'name_middle', 'name_last', 'name_full_formatted'],
            'description': '***This section is ONNLY needed for staff members.***'
        }),
        (None, {
            'fields': ['is_active', 'active_status_cd'],
        }),
    )
    extra = 0

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    inlines = [ PersonInline, PrsnlInline]
 

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name_first', 'name_last', 'name_full_formatted', 'is_active')
    list_filter = ('name_last', 'name_first')
    fieldsets = (
        (None, {'fields': ('name_first', 'name_middle', 'name_last', 'name_full_formatted')}),
        (None, {'fields': ('is_active', 'active_status_cd')}),
    )
    add_fieldsets = (
        (None, {'fields': ('name_first', 'name_middle', 'name_last', 'name_full_formatted')}),
        (None, {'fields': ('is_active', 'active_status_cd')}),
    )
    search_fields = ['name_last', 'name_first']
    ordering = ['name_last',]
    inlines = [ PersonAliasInline, ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Person, PersonAdmin)
