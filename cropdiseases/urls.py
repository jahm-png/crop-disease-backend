from django.urls import path
from .views import (
    DiseaseList,
    SymptomDiagnosis,
    ImageDiagnosisView,
    AddDisease,
    diagnose,
    get_weather,  # ✅ this is the correct import
)

urlpatterns = [
    path('diseases/', DiseaseList.as_view(), name='disease-list'),
    path('diagnose/', SymptomDiagnosis.as_view(), name='symptom-diagnosis'),
    path('diagnose-fb/', diagnose, name='diagnose-function-based'),
    path('image-diagnosis/', ImageDiagnosisView.as_view(), name='image-diagnosis'),
    path('add-disease/', AddDisease.as_view(), name='add-disease'),
    path('weather/', get_weather, name='get-weather'),  # ✅ use get_weather not WeatherView
]
