from django.contrib import admin

# Register your models here.
from django.db import models
from django.forms import CheckboxSelectMultiple

from rental_exchange.forms import CarForm, SystemForm
from rental_exchange.models import Car, Brand, Feature, Blog, System, Contact
from users.admin import UserAdmin


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Car._meta.fields]
    list_display_links = ['name']
    list_per_page = 10
    exclude = ('created_by', 'updated_by')
    autocomplete_fields = ['brand']
    form = CarForm
    # formfield_overrides = {
    #     'features': {'widget': CheckboxSelectMultiple},
    # }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brand._meta.fields]
    list_display_links = ['name']
    list_per_page = 10
    search_fields = ['name']
    exclude = ('created_by', 'updated_by')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Feature._meta.fields]
    list_display_links = ['title']
    list_per_page = 10
    exclude = ('created_by', 'updated_by')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Blog._meta.fields]
    list_display_links = ['title']
    list_per_page = 10
    exclude = ('created_by', 'updated_by')
    search_fields = ['title']


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in System._meta.fields]
    form = SystemForm
    fieldsets = (
        ('Site', {'fields': ('site_title', 'site_logo')}),
        ('Contacts', {'fields': ('contact_email', 'contact_phone', 'contact_address')}),
        ('Mail Setup', {'fields': ('email_from', 'email_from_password', 'email_to')}),
        ('Map Setup', {'fields': ('map_url',)}),
        ('Social Links', {'fields': ('facebook_url', 'twitter_url', 'instagram_url')}),
        ('Copyright', {'fields': ('copyright_owner', 'copyright_year')}),
    )

    def has_add_permission(self, *args, **kwargs):
        return not System.objects.exists()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]


# @admin.register(Customer)
# class CustomerAdmin(UserAdmin):
#     list_display = ['first_name', 'last_name', 'phone', 'is_active', 'last_login']
#     fields = ['phone', 'address']
#     # fieldsets = (
#     #     ('Personal Information', {
#     #         'classes': ('wide',),
#     #         'fields': ('first_name', 'last_name', 'phone', 'address')}
#     #      ),
#     #     ('Authentication', {
#     #         'classes': ('wide',),
#     #         'fields': ('email', 'password')}
#     #      ),
#     #     ('Permissions And Roles', {
#     #         'classes': ('wide',),
#     #         'fields': ('groups', 'user_permissions')}
#     #      ),
#     #     ('Status', {
#     #         'classes': ('wide',),
#     #         'fields': ('is_active',)}
#     #      ),
#     # )
#     # add_fieldsets = (
#     #     (None, {
#     #         'classes': ('wide',),
#     #         'fields': ('first_name', 'last_name', 'phone', 'address', 'email', 'password1', 'password2'),
#     #     }),
#     # )