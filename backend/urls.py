from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/cropdiseases/', include('cropdiseases.urls')),  # ✅ Already has weather and image diagnosis
    path('api/', include('cropdiseases.urls')),  # ✅ Add this line to fix /api/send-sms/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
