from django.contrib import admin

from ..models import Prsnl, Person_Alias, Prsnl_Alias


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


class PrsnlAdmin(admin.ModelAdmin):
    list_display = ('name_first', 'name_last', 'name_full_formatted', 'position', 'is_active')
    list_filter = ('name_last', 'position', 'is_active')
    fieldsets = (
        (None, {'fields': ('name_first', 'name_middle', 'name_last', 'name_full_formatted')}),
        (None, {'fields': ('position', 'is_active', 'active_status_cd')}),
    )
    add_fieldsets = (
        (None, {'fields': ('name_first', 'name_middle', 'name_last', 'name_full_formatted')}),
        (None, {'fields': ('postion', 'is_active', 'active_status_cd')}),
    )
    search_fields = ['name_last', 'name_first']
    ordering = ['name_last',]
    verbose_name_plural = 'personnel'
    inlines = [ PrsnlAliasInline, ]

admin.site.register(Prsnl, PrsnlAdmin)
