from django.contrib import admin
from django.contrib import admin
from .models import ContactUs,UserStat,FaqTopic,FaqQa,ContactSubject,Info

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "subject",
        "message",
    )

    list_display_links = ("id",)


admin.site.register(ContactUs, ContactAdmin)

class UserStatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "homepage_hits_login",
        "homepage_hits_anonymous",
        "spinx_hits",
        "spinx_hits_anonymous",
        "created_at",
        "updated_at"

    )
    list_display_links = ("id",)
    list_filter = ("created_at",)

admin.site.register(UserStat, UserStatAdmin)


admin.site.register(FaqTopic)
admin.site.register(FaqQa)
admin.site.register(ContactSubject)
admin.site.register(Info)
