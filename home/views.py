from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from setup.permissions import IsSuperUser
from django.db.models import Sum
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncMonth
from drf_spectacular.utils import extend_schema

from .serializers import DashboardSerializer

from users.models import User
from orders.models import Order, OrderItem
from .utils import calculate_retention_rate
from .utils import order_processing_time
from .utils import order_return_rate


@extend_schema(tags=["Home"])
class DashboardAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def post(self, request, *args, **kwargs):

        serializers = DashboardSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        from_date = serializers.data.get('from_date')
        to_date = serializers.data.get('to_date')

        all_orders = Order.objects.all()

        orders = all_orders.filter(
            status__in=[
                Order.ORDER_PLACED,
                Order.ORDER_PROCESSING,
                Order.PACKED,
                Order.READY_FOR_DISPATCH,
                Order.DELIVERED
            ]
        )

        last_period_from_date, last_period_to_date = serializers.find_previous_period()

        total_sales = orders.filter(
            created_at__date__gte=from_date,
            created_at__date__lte=to_date
        ).aggregate(Sum('total_amount'))['total_amount__sum']

        total_sales_previous_period = orders.filter(
            created_at__date__gte=last_period_from_date,
            created_at__date__lte=last_period_to_date
        ).aggregate(Sum('total_amount'))['total_amount__sum']

        total_sales = total_sales if total_sales else 0
        total_sales_previous_period = total_sales_previous_period if total_sales_previous_period else 0

        if total_sales_previous_period == 0:
            # Handle division by zero (in case previous sales are zero)
            percentage_change = float('inf') if total_sales > 0 else float('-inf')
        else:
            # Calculate percentage change
            percentage_change = ((total_sales - total_sales_previous_period) / total_sales_previous_period) * 100

        if percentage_change > 0:
            change_type = "increase"
        elif percentage_change < 0:
            change_type = "decrease"
        else:
            change_type = "no change"

        sales = {
            'total_sales': total_sales,
            'previous_total_sales': total_sales_previous_period,
            'percentage_change': f"Percentage {change_type}: {abs(percentage_change):.2f}%"
        }

        customers = User.objects.filter(is_customer=True).count()

        customers_queryset = User.objects.filter(is_customer=True)

        customers_details = {
            'customers': customers_queryset.count(),
            'new_customers': customers_queryset.filter(
                created_at__date__gte=from_date,
                created_at__date__lte=to_date
            ).count(),
            'retention_rate': calculate_retention_rate(from_date, to_date, customers_queryset)
        }

        # Aggregate total quantity sold for each product variant
        top_products = OrderItem.objects.values('product_variant__product__name').annotate(
            total_quantity_sold=Sum('quantity'),
            total_revenue=Sum('total_amount')
        ).order_by('-total_quantity_sold')[:10]  # Adjust to get top N products

        # Aggregate total quantity sold and revenue for each product variant
        products_performance = OrderItem.objects.values('product_variant__product__name').annotate(
            total_quantity_sold=Sum('quantity'),
            total_revenue=Sum('total_amount')
        )

        # Define a threshold for low sales (adjust as needed)
        low_sales_threshold = 10  # Example: Consider products with less than 10 units sold as low-performing

        # Filter products with low sales based on quantity sold or revenue
        low_performing_products = [
            {
                'product_name': item['product_variant__product__name'],
                'total_quantity_sold': item['total_quantity_sold'],
                'total_revenue': item['total_revenue']
            }
            for item in products_performance
            if item['total_quantity_sold'] < low_sales_threshold  # Adjust condition based on sales volume or revenue
        ]

        category_performance = OrderItem.objects.values('product_variant__product__categories__name').annotate(
            total_quantity_sold=Sum('quantity'),
            total_revenue=Sum('total_amount')
        ).exclude(  # Add this to exclude None/null category names
            product_variant__product__categories__name__isnull=True
        )

        return Response({
            'message': 'success',
            'data': {
                'sales': sales,
                'customers': customers_details,
                'products': {
                    'top_products': top_products,
                    'low_performing_products': low_performing_products,
                    'category_performance': category_performance,
                },

                'orders': {
                    'details': {
                        'PENDING': all_orders.filter(status=Order.PENDING).count(),
                        'PAYMENT_INITIATED': all_orders.filter(status=Order.PAYMENT_INITIATED).count(),
                        'ORDER_PLACED': all_orders.filter(status=Order.ORDER_PLACED).count(),
                        'ORDER_PROCESSING': all_orders.filter(status=Order.ORDER_PROCESSING).count(),
                        'PACKED': all_orders.filter(status=Order.PACKED).count(),
                        'READY_FOR_DISPATCH': all_orders.filter(status=Order.READY_FOR_DISPATCH).count(),
                        'SHIPPED': all_orders.filter(status=Order.SHIPPED).count(),
                        'DELIVERED': all_orders.filter(status=Order.DELIVERED).count(),
                        'CANCELLED': all_orders.filter(status=Order.CANCELLED).count()
                    },
                    'order_processing_time': order_processing_time(),
                    'order_return_rate': order_return_rate(),
                }
            }
        }, status=status.HTTP_200_OK)


@extend_schema(tags=["Home"])
class CustomerGrowthAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def get(self, request):
        # Get current month's start date and last month's start date
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (current_month_start - timezone.timedelta(days=1)).replace(day=1)

        # Count customers registered this month and last month
        current_month_customers = User.objects.filter(
            is_customer=True,
            created_at__gte=current_month_start
        ).count()
        last_month_customers = User.objects.filter(
            is_customer=True,
            created_at__gte=last_month_start,
            created_at__lt=current_month_start
        ).count()

        # Calculate growth and percentage growth
        growth = current_month_customers - last_month_customers
        percentage_growth = (growth / last_month_customers) * 100 if last_month_customers != 0 else 0

        # Prepare response data
        data = {
            'current_month_customers': current_month_customers,
            'last_month_customers': last_month_customers,
            'growth': growth,
            'percentage_growth': round(percentage_growth, 2)  # Round percentage to 2 decimal places
        }

        return Response({
            'message': 'success',
            'data': data
        }, status=status.HTTP_200_OK)


@extend_schema(tags=["Home"])
class CustomerOrderAnalysisAPIView(APIView):
    def get(self, request):
        # Get current month's start date and last month's start date
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (current_month_start - timezone.timedelta(days=1)).replace(day=1)

        # Count customers who placed orders this month and last month
        current_month_orders = Order.objects.filter(order_date__gte=current_month_start).values_list('customer_id', flat=True).distinct()
        last_month_orders = Order.objects.filter(order_date__gte=last_month_start, order_date__lt=current_month_start).values_list('customer_id', flat=True).distinct()

        current_month_customers = len(set(current_month_orders))
        last_month_customers = len(set(last_month_orders))

        # Calculate growth and percentage growth
        growth = current_month_customers - last_month_customers
        percentage_growth = (growth / last_month_customers) * 100 if last_month_customers != 0 else 0

        # Prepare response data
        data = {
            'current_month_customers_with_orders': current_month_customers,
            'last_month_customers_with_orders': last_month_customers,
            'growth': growth,
            'percentage_growth': round(percentage_growth, 2)  # Round percentage to 2 decimal places
        }

        return Response(data)


@extend_schema(tags=["Home"])
class CustomerRetentionAPIView(APIView):
    def get(self, request):
        # Get current month's start date and last month's start date
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (current_month_start - timezone.timedelta(days=1)).replace(day=1)

        # Get active customer IDs from last month
        active_customers_last_month = User.objects.filter(
            is_customer=True,
            created_at__lt=current_month_start,
            is_active=True
        ).values_list('id', flat=True)

        # Count active customers from last month who are still active this month
        retained_customers_count = User.objects.filter(
            is_customer=True,
            id__in=active_customers_last_month,
            is_active=True
        ).count()

        # Count total active customers last month
        total_active_customers_last_month = User.objects.filter(
            is_customer=True,
            created_at__lt=current_month_start,
            is_active=True
        ).count()

        # Calculate retention rate and percentage retention rate
        retention_rate = (retained_customers_count / total_active_customers_last_month) * 100 if total_active_customers_last_month != 0 else 0

        # Prepare response data
        data = {
            'retained_customers_count': retained_customers_count,
            'total_active_customers_last_month': total_active_customers_last_month,
            'retention_rate': round(retention_rate, 2)  # Round retention rate to 2 decimal places
        }

        return Response(data)


@extend_schema(tags=["Home"])
class MonthlyCustomerCountAPIView(APIView):
    def get(self, request):
        # Get current year
        current_year = timezone.now().year

        # Filter customers created within the current year
        customers = User.objects.filter(is_customer=True, created_at__year=current_year)

        # Annotate customers count by month
        monthly_counts = customers.annotate(
            month=TruncMonth('created_at')  # Truncate datetime to month
        ).values(
            'month'
        ).annotate(
            count=Count('id')
        ).order_by(
            'month'
        )

        # Prepare response data
        data = {
            'monthly_customer_counts': list(monthly_counts)
        }

        return Response(data)

