from django.contrib import admin
from .models import LDAPUser, UserProfile
from django.utils.html import mark_safe


admin.site.register(LDAPUser)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        if not obj.profile_picture:
            return None
        return mark_safe('<img src="{}" width="100" height="80" />'.format(obj.profile_picture.url))

    image_tag.short_description = 'Profile Image'
    image_tag.allow_tags = True

    list_display = ('image_tag', 'user')
