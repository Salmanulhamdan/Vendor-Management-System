from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet
from .views import VendorPerformanceView,AcknowledgePurchaseOrder

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<str:vendor_code>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge', AcknowledgePurchaseOrder.as_view()),
    
]