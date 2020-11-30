from django.contrib import admin

# Register your models here.
from users.forms import UserChangeForm, UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name')}),
    #     ('Permissions', {'fields': ('is_staff',)}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
    #     }),
    # )

    # def get_fields(self, request, obj=None):
    #     if obj:
    #         fields = ()
    #     else:
    #         fields = ('cname', 'mname')
    #     return fields

    # def get_fieldsets(self, request, obj=None):
    #     if obj:
    #         fieldsets = (
    #             (None, {'fields': ('email', 'password')}),
    #             ('Personal info', {'fields': ('first_name', 'last_name')}),
    #             ('Permissions', {'fields': ('is_staff',)}),
    #         )
    #     else:
    #         fieldsets = (
    #             (None, {
    #                 'classes': ('wide',),
    #                 'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
    #             }),
    #         )
    #     return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(UserAdmin, self).get_form(request, obj, **kwargs)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    # fieldsets = (
    #     (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    # )
    # add_fieldsets = (
    #     (None,
    #      {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')
    #     }
    #     ),
    # )
    # search_fields = ('email',)
    # ordering = ('email',)
