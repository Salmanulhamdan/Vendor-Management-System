from rest_framework import viewsets,status
from vendors.models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import generics
from rest_framework.response import Response
from .serializers import AcknowledgePurchaseOrderSerializer
from rest_framework.views import APIView

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer



class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_code' 

    def retrieve(self, request, *args, **kwargs):
        vendor_code = self.kwargs.get('vendor_code')
        vendor = self.get_object()
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)



class AcknowledgePurchaseOrder(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AcknowledgePurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            acknowledgment_date = serializer.validated_data['acknowledgment_date']
            purchase_order.acknowledgment_date = acknowledgment_date
            purchase_order.save()

            # Update average_response_time for the vendor
            vendor = purchase_order.vendor
            response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).values_list('acknowledgment_date', 'order_date')
            total_response_time = sum((ack_date - order_date).total_seconds() for ack_date, order_date in response_times)
            total_orders = len(response_times)
            average_response_time = total_response_time / total_orders if total_orders > 0 else 0
            vendor.average_response_time = average_response_time
            vendor.save()

            return Response({'message': 'Purchase Order acknowledged successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)