from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from customer.models import CartItem
from product.models import Variant


class Command(BaseCommand):
    help = 'To restore the product, that are in the inactive cart'

    def handle(self, *args, **options):
        time_ago = datetime.now() - timedelta(seconds=20) 
        for cart_item in CartItem.objects.filter(deleted=False, created_at__lt=time_ago):
            variant = Variant.objects.get(pk=cart_item.product_variant_id)
            print("variant.stock",variant.stock)
            print("cartItem.quantity",cart_item.quantity)
            variant.stock += cart_item.quantity
            variant.save()
            





