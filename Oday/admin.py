from django.contrib import admin
from Oday import models
from .models import FooterSetting, FooterLink

admin.site.register(models.AddToCardModel)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.LoginHistory)


@admin.register(FooterSetting)
class FooterSettingAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "phone", "email")


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order", "is_active")
    list_editable = ("order", "is_active")
