from django.contrib import admin
from .models import Market,Bet,BetSlip

class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "result",
        "odds" ,
        "created_at",
        "updated_at",
    )
    list_display_links = ("code",)
    search_fields= ("id",)
    #list_editable = (
    #    "odds",
    #)
    list_filter = ("code","result", "created_at", "updated_at")


admin.site.register(Market, MarketAdmin)



class BetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "bet_slip",
        "amount",
        "active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("account",)
    search_fields= ("id",)
    #list_editable = (
    #    "odds",
    #)
    list_filter = ("account","active", "created_at", "updated_at")


admin.site.register(Bet, BetAdmin)

class BetSlipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields= ("id",)
    #list_editable = (
    #    "odds",
    #)
    list_filter = ("created_at", "updated_at")


admin.site.register(BetSlip, BetSlipAdmin)
