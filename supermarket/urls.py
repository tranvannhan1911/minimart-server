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
from management.api.address import AddressPathIdView, AddressView, WardView
from management.api.customer.account import CustomerForgotPassword, CustomerLoginView
from management.api.general import CounterIndexView
from management.api.inventory import InventoryRCIdView, InventoryRCView, InventoryRecordIdView, InventoryRecordView, WarehouseTransactionIdView, WarehouseTransactionView
from management.api.product import CalculationUnitIdView, CategoryIdView, CategoryToParentView, CategoryToSelectView, CategoryView, PriceListIdView, PriceListView, ProductGroupIdView, ProductGroupView, CalculationUnitView, ProductIdView, ProductView
from management.api.promotion import PromotionByOrderView, PromotionByTypeView, PromotionHistoryIdView, PromotionHistoryView, PromotionIdView, PromotionLineIdView, PromotionLineView, PromotionProductIdView, PromotionView
from management.api.sell import OrderIdView, OrderRefundIdView, OrderRefundView, OrderView
from management.api.statistic import StatisticSalesCustomerView, StatisticSellView
from management.api.supplier import SupplierIdView, SupplierView

from management.api.user import (
    CustomerIdView, CustomerView, ResetPasswordView, StaffIdView, StaffView, 
)

from management.api.customer_group import (
    CustomerGroupIdView, CustomerGroupView
)

schema_view = get_schema_view(
   openapi.Info(
      title="Quản lý siêu thị mini API",
      default_version='v1',
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

            # customer
            
            path('login-customer/', CustomerLoginView.as_view()),
            path('forgot-password-customer/', CustomerForgotPassword.as_view()),
        ])),
        path('customer/', include([
            path('', CustomerView.as_view(), name='customer'),
            path('<int:id>/', CustomerIdView.as_view(), name='customer_id'),
        ])),
        path('customer-group/', include([
            path('', CustomerGroupView.as_view(), name='customer_group'),
            path('<int:id>/', CustomerGroupIdView.as_view(), name='customer_group_id'),
        ])),
        path('staff/', include([
            path('', StaffView.as_view(), name='staff'),
            path('<int:id>/', StaffIdView.as_view(), name='staff_id'),
            path('reset_password/<int:id>/', ResetPasswordView.as_view()),
        ])),
        path('supplier/', include([
            path('', SupplierView.as_view(), name='supplier'),
            path('<int:id>/', SupplierIdView.as_view(), name='supplier_id'),
        ])),
        path('product-group/', include([
            path('', ProductGroupView.as_view(), name='product_group'),
            path('<int:id>/', ProductGroupIdView.as_view(), name='product_group_id'),
        ])),
        path('calculation-unit/', include([
            path('', CalculationUnitView.as_view(), name='calculation_unit'),
            path('<int:id>/', CalculationUnitIdView.as_view(), name='calculation_unit_id'),
        ])),
        path('product/', include([
            path('', ProductView.as_view(), name='product'),
            path('<int:id>/', ProductIdView.as_view(), name='product_id'),
        ])),
        path('price-list/', include([
            path('', PriceListView.as_view(), name='price_list'),
            path('<int:id>/', PriceListIdView.as_view(), name='price_list_id'),
        ])),
        path('inventory-receiving/', include([
            path('', InventoryRCView.as_view(), name='inventory_receiving'),
            path('<int:id>/', InventoryRCIdView.as_view(), name='inventory_receiving_id'),
        ])),
        path('inventory-record/', include([
            path('', InventoryRecordView.as_view(), name='inventory_record'),
            path('<int:id>/', InventoryRecordIdView.as_view(), name='inventory_record_id'),
        ])),
        path('warehouse-transaction/', include([
            path('', WarehouseTransactionView.as_view(), name='warehouse_transaction'),
            path('<int:id>/', WarehouseTransactionIdView.as_view(), name='warehouse_transaction_id'),
        ])),
        path('category/', include([
            path('', CategoryView.as_view(), name='category'),
            path('<int:id>/', CategoryIdView.as_view(), name='category_id'),
            path('to_select/', CategoryToSelectView.as_view(), name='category'),
            path('get_parent/<int:id>/', CategoryToParentView.as_view(), name='category_id'),
        ])),
        path('promotion/', include([
            path('', PromotionView.as_view(), name='promotion'),
            path('<int:id>/', PromotionIdView.as_view(), name='promotion_id'),
        ])),
        path('promotion-line/', include([
            path('', PromotionLineView.as_view(), name='promotion_line'),
            path('<int:id>/', PromotionLineIdView.as_view(), name='promotion_line_id'),
            path('by_product/', PromotionProductIdView.as_view(), name='promotion_product_id'),
            path('by_order/', PromotionByOrderView.as_view()),
            path('by_type/', PromotionByTypeView.as_view()),
        ])),
        path('promotion-history/', include([
            path('', PromotionHistoryView.as_view()),
            path('<int:id>/', PromotionHistoryIdView.as_view()),
        ])),
        path('order/', include([
            path('', OrderView.as_view(), name='order'),
            path('<int:id>/', OrderIdView.as_view(), name='order_id'),
        ])),
        path('refund/', include([
            path('', OrderRefundView.as_view(), name='order_refund'),
            path('<int:id>/', OrderRefundIdView.as_view(), name='order_refund_id'),
        ])),
        path('address/', include('vi_address.urls')),
        path('address/tree/', AddressView.as_view()),
        path('address/path/<int:id>/', AddressPathIdView.as_view()),
        path('address/ward/<int:id>/', WardView.as_view()),
        path('counter-indext/<str:table>/', CounterIndexView.as_view()),

        path('statistic/', include([
            path('sales-staff/', StatisticSellView.as_view()),
            path('sales-customer/', StatisticSalesCustomerView.as_view()),
        ])),
    ])),

]
