"""supermarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from management.api.account import (
    ChangePasswordView, ForgotPassword, 
    ForgotPasswordVerify, MyTokenRefreshView, 
    TokenLoginView, GetInfoView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django_twilio.views import sms
from management.api.product import ProductGroupIdView, ProductGroupView
from management.api.supplier import SupplierIdView, SupplierView

from management.api.user import (
    UserIdView, UserView,
)

from management.api.customer_group import (
    CustomerGroupIdView, CustomerGroupView
)

schema_view = get_schema_view(
   openapi.Info(
      title="Quản lý siêu thị mini API",
      default_version='v3',
      description="Quản lý siêu thị mini API",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/', include([
        path('account/', include([
            path('login/', TokenLoginView.as_view(), name='login'),
            # path('login/', TokenObtainPairView.as_view(), name='login'),
            path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
            path('forgot_password/', ForgotPassword.as_view(), name="forgot_password"),
            path('forgot_password/verify/', ForgotPasswordVerify.as_view(), name="forgot_password_verify"),
            path('change_password/', ChangePasswordView.as_view(), name='change_password'),
            path('get_info/', GetInfoView.as_view(), name='get_info'),
        ])),
        path('customer/', include([
            path('', UserView.as_view(), name='customer'),
            path('<int:id>/', UserIdView.as_view(), name='customer_id'),
        ])),
        path('customer-group/', include([
            path('', CustomerGroupView.as_view(), name='customer_group'),
            path('<int:id>/', CustomerGroupIdView.as_view(), name='customer_group_id'),
        ])),
        path('staff/', include([
            path('', UserView.as_view(), name='staff'),
            path('<int:id>/', UserIdView.as_view(), name='staff_id'),
        ])),
        path('supplier/', include([
            path('', SupplierView.as_view(), name='supplier'),
            path('<int:id>/', SupplierIdView.as_view(), name='staff_id'),
        ])),
        path('product-group/', include([
            path('', ProductGroupView.as_view(), name='product_group'),
            path('<int:id>/', ProductGroupIdView.as_view(), name='staff_id'),
        ]))
    ])),

]
