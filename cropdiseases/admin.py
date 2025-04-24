from django.contrib import admin
from .models import Disease

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'disease_name', 'symptoms', 'treatment')
    search_fields = ('crop_name', 'disease_name', 'symptoms')
