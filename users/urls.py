from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('user-address', views.AddressRegisterModelViewSet)
router.register('manager', views.ManagerViewSet)
router.register('customers', views.CustomerViewSet)

urlpatterns = [
    path('user/email/', views.TestMail.as_view(), name='user-mail'),
    path('user/subscribe/', views.SubscribeToSignup.as_view(), name='subscribe-to-signup'),

    path('user/sign-up/', views.Signup.as_view(), name='user-signup'),
    path('user/change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('user/me/', views.Me.as_view(), name='me'),
    path('user/prolile-update/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('user/user-signed-up/', views.LogtoUserCreateHooks.as_view(), name='user-signed-up'),

    path(
        'session/', include(([
            path('user/login/', views.Login.as_view(), name='user-login')
        ])), name="session-login"
    ),

    path(
        'token/', include(([
            path('user/login/', views.TokenLoginAPTView.as_view(), name='token-login'),
            path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
            path('user/status/', views.LoginStatus.as_view(), name='token-refresh-c'),
        ])), name="jwt-token-login"
    ),

    path('user/logout/', views.Logout.as_view(), name='user-logout'),

    path('social/', include('allauth.urls')),
]

urlpatterns += router.urls

