from django.contrib import admin

from ..models import Person, Person_Alias


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
    extra = 0


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


admin.site.register(Person, PersonAdmin)
