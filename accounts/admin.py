from django.contrib import admin

from .models import (
    Account,
    CentralBank,
    AccountSetting,
    Currency,
    CashDeposit,
    CashWithrawal,
    Transaction,
)

class CentralBankAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "give_away",
        "to_keep",
        "give_away_marketer",
        "to_keep_marketer",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id","name")
    list_filter = ("id","name","created_at","updated_at")

admin.site.register(CentralBank, CentralBankAdmin)


class AccountSettingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "min_redeem_refer_credit",
        "auto_approve",
        "auto_approve_cash_trasfer",
        "withraw_factor",
        "paypill",
        "created_at"
    )
    list_display_links = ("id",)
    search_fields = ("id",)
    list_editable = (
        "min_redeem_refer_credit",
        "auto_approve",
        "auto_approve_cash_trasfer",
        "withraw_factor",
        "paypill"
    )


admin.site.register(AccountSetting, AccountSettingAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "cbank",
        "user",
        "tokens",
        "balance",
        "actual_balance",
        "withraw_power",
        "withrawable_balance",
        "withrawable_balance_USD",
        "withrawable_balance_KES",
        "refer_balance",
        "ref1",
        "ref30",
        "trial_balance",
        "cum_deposit",
        "cum_withraw",
        "c_loss",
        "active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("user_id","user")
    search_fields = ("id",)
    list_editable = (
        "balance",
        "tokens",
        "actual_balance",
        "withraw_power",
        "refer_balance",
        "trial_balance",
        "cum_deposit",
        "cum_withraw",
      #  "created_at",
    )
    list_filter = ("user","cbank", "created_at", "updated_at")


admin.site.register(Account, AccountAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account", 
        "trans_type",
        "value",
        "running_balance",
        "currency",
        "created_at",
        "updated_at",
    )
    # list_display_links = ('',)
    search_fields = ("name",)
    #list_editable = ("name", "rate")
    # readonly_fields =()
    list_filter = ("account","trans_type", "created_at", "updated_at")
    
admin.site.register(Transaction, TransactionAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "rate",
        "created_at",
        "updated_at",
    )
    # list_display_links = ('',)
    search_fields = ("name",)
    list_editable = ("name", "rate")
    # readonly_fields =()


admin.site.register(Currency, CurrencyAdmin)

class CashDepositAdmin(admin.ModelAdmin):
    list_display = (
        #"user",
        "account",
        "deposited",
        "status",
        "deposit_type",
        "has_record",
        "amount",
        "tokens",
        "currency",
        #"current_bal",
        "created_at",
        "updated_at",
    )
    list_display_links = ("account",)
    search_fields = ("amount",)
    list_filter = (
       # "user",
        "currency",
        "deposit_type",
        "deposited",)
    readonly_fields = (
        "deposited",
        "has_record",
       # "current_bal",
        "created_at",
        "updated_at",
    )
    list_editable = (
        "deposit_type",
        "tokens",

    )
   # readonly_fields =("tokens",)

admin.site.register(CashDeposit, CashDepositAdmin)

class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "active",
        "cancelled",
        "approved",
        "withrawned",
        "withraw_status",
        "withr_type",
        "confirmed",
        "has_record",
        "amount",
        "tokens",
        "currency",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id","amount",)
    search_fields = ("account",)
    list_filter = ("account", "approved", "cancelled","confirmed","withr_type","currency", "active","created_at","updated_at",)
    readonly_fields = (
        "withrawned",
        "has_record",
        "active",
        "created_at",
        "updated_at",
    )
    list_editable = ("approved", "cancelled","confirmed","tokens")


admin.site.register(CashWithrawal, CashWithrawalAdmin)



