from django.contrib import admin
from .models import (
    Stake,
    SpinxSetting,
)

class SpinxSettingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "refer_per",
        "per_to_keep",
        "min_bet",
        "virtual_acc",
        "created_at",
        "updated_at",
        "active"
    )
    list_display_links = ("id",)
    list_editable = (
        "refer_per",
        "per_to_keep",
        "min_bet",
        "virtual_acc",
        "active"
    )


admin.site.register(SpinxSetting, SpinxSettingAdmin)



class StakeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "account_type",
        "amount",
        "placed",
        "win_multiplier",
        "pointer",
        "closed",
        "expected_win_amount",
        "real_account",
        "spinned",
        "bet_status",
        "active_spinsx",
        #"this_user_has_cash_to_bet",
        "created_at",
        "updated_at",
    )

    list_display_links = ("account",)
    search_fields = ("account",)
    list_filter = ("account","real_account","spinned", "created_at")


admin.site.register(Stake, StakeAdmin)



