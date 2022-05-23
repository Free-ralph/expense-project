from django.contrib import admin
from .models import Income




class IncomeAdminModel(admin.ModelAdmin):
    raw_id_fields = [
        'owner'
    ]

admin.site.register(Income, IncomeAdminModel)