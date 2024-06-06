from django.db.models import Avg, F, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HistoricalPerformance, PurchaseOrder
from django.db import models
from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    vendor = instance.vendor

    print("signaling")

    # Update On-Time Delivery Rate if PO is completed
    if instance.status == 'completed':
        total_completed_pos = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed'
        ).count()

        if total_completed_pos == 0:
            vendor.on_time_delivery_rate = 0.0
        else:
            on_time_completed_pos = PurchaseOrder.objects.filter(
                vendor=vendor, status='completed',
                delivery_date__lte=F('delivery_date')
            ).count()
            on_time_delivery_rate=(on_time_completed_pos / total_completed_pos) * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate

        # Update Quality Rating Average
        completed_pos_with_ratings = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', quality_rating__isnull=False
        )
        total_ratings_count = completed_pos_with_ratings.count()

        if total_ratings_count == 0:
            vendor.quality_rating_avg = 0.0
        else:
            average_quality_rating = completed_pos_with_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg']
            vendor.quality_rating_avg = average_quality_rating


        # Calculate Fulfillment Rate
        try:
            fulfillment_rate = PurchaseOrder.objects.filter(
                vendor=vendor
            ).filter(
                status='completed'
            ).count() / total_completed_pos
        except ZeroDivisionError:
            fulfillment_rate = 0.0
        vendor.fulfillment_rate = fulfillment_rate

    # Update Average Response Time if acknowledgment_date is set
    if instance.acknowledgment_date is not None:
        total_responded_pos = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        ).count()

        if total_responded_pos == 0:
            vendor.average_response_time = 0.0
        else:
            total_response_time = PurchaseOrder.objects.filter(
                vendor=vendor, acknowledgment_date__isnull=False
            ).aggregate(
                total_response_time=Sum(
                    F('acknowledgment_date') - F('issue_date'),
                    output_field=models.DurationField()
                )
            )['total_response_time']
            
            average_response_time = total_response_time / total_responded_pos
            vendor.average_response_time = average_response_time.total_seconds() / 3600  # Convert to hours

    vendor.save()

    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )







   