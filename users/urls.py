from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('user-address', views.AddressRegisterModelViewSet)
router.register('manager', views.ManagerViewSet)
router.register('customers', views.CustomerViewSet)

urlpatterns = [
    path('user/change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('user/me/', views.Me.as_view(), name='me'),
    path('user/prolile-update/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('user/user-signed-up/', views.LogtoUserCreateHooks.as_view(), name='user-signed-up'),
    path('user/subscribe/', views.SubscribeToSignup.as_view(), name='subscribe-to-signup'),
]

urlpatterns += router.urls

