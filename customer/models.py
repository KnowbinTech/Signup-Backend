from django.db import models
from django.db.models import Sum
from django_fsm import transition
from django_fsm import FSMIntegerField

from setup.middleware.request import CurrentRequestMiddleware

from users.models.base_model import BaseModel
from users.models import User
from masterdata.models import ReturnReason


def generate_return_id():
    return_last = Return.objects.all().order_by('-id')
    if return_last.count() > 0:
        last_return = return_last[0].return_id
        number = int(last_return[6:]) + 1
    else:
        number = 1
    return_key = f"{number:06}"
    return_id = f"SC-RET{return_key}"

    if Return.objects.filter(return_id=return_id).exists():
        return generate_return_id()
    return return_id


class WishList(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_wishlist', verbose_name='User', null=True
    )
    product = models.ForeignKey(
        'product.Products', on_delete=models.CASCADE, related_name='product_wishlist', verbose_name='Product', null=True
    )

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Cart(BaseModel):
    session_key = models.CharField(max_length=70, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='user_cart',
        verbose_name='User', null=True, blank=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    currency = models.CharField(max_length=10, default='INR', null=True, blank=True, verbose_name='Currency')
    is_completed = models.BooleanField(default=False, verbose_name='Cart Completed')

    def __str__(self):
        return f"{self.user.get_full_name()}"

    def calculate_total(self):
        total_amount = CartItem.objects.filter(cart=self, deleted=False).aggregate(Sum('total_amount'))
        self.total_amount = total_amount['total_amount__sum'] if total_amount['total_amount__sum'] else 0.00
        self.save()

    def complete_cart(self):
        self.is_completed = True
        self.save()

    @classmethod
    def get_session_cart(cls):
        request = CurrentRequestMiddleware.get_request()
        session_key = request.session.session_key
        if not request.session.exists(session_key):
            request.session.create()
        session_key = request.session.session_key

        try:
            return cls.objects.get(session_key=session_key, is_completed=False)
        except cls.DoesNotExist:
            return cls.objects.create(session_key=session_key, total_price=0)

    @classmethod
    def get_user_cart(cls, set_total=True):
        user = CurrentRequestMiddleware.get_request().user

        cart, created = cls.objects.get_or_create(
            user_id=user.id, deleted=False,
            is_completed=False
        )
        if set_total:
            cart.total_amount = cart.cartitems.filter(
                product_variant__stock__gt=0, deleted=False
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            cart.save()
        return cart


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', verbose_name='Cart Details')
    product_variant = models.ForeignKey('product.Variant', on_delete=models.CASCADE, related_name='cart_product',
                                        verbose_name='Product Variant')
    quantity = models.IntegerField(default=1, verbose_name='Quantity')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Price')

    def save(self, *args, **kwargs):
        total_amount = self.price * self.quantity
        self.total_amount = total_amount
        super().save(*args, **kwargs)
        self.cart.calculate_total()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product_variant.restore_stock(self.quantity)


class Review(BaseModel):
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    product = models.ForeignKey(
        'product.Products', on_delete=models.SET_NULL,
        related_name='product_review', null=True,
        verbose_name="Product"
    )

    comment = models.TextField(null=True, verbose_name='Comment')

    rating = models.CharField(max_length=5, default='0', null=True, verbose_name='Rating', choices=RATING_CHOICES)


class ReviewImage(BaseModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review_image',
        verbose_name='Review', null=True
    )

    file = models.FileField(upload_to='review/image', verbose_name='Image', blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)


class Return(BaseModel):
    PENDING = 0
    SUBMITTED = 1
    IN_REVIEW = 2
    APPROVED = 3
    REJECTED = 4

    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (SUBMITTED, 'SUBMITTED'),
        (IN_REVIEW, 'IN REVIEW'),
        (APPROVED, 'APPROVED'),
        (REJECTED, 'REJECTED'),
    )

    REFUND_METHOD = (
        ('Exchange', 'Exchange'),
        ('Refund', 'Refund'),
    )

    REFUND_IN_REVIEW = 0
    REFUND_PENDING = 1

    EXCHANGE_IN_TRANSIT = 2
    EXCHANGE_DELIVERED = 3

    REFUND_INITIATED = 4
    REFUND_REIMBURSED = 5

    REFUND_CHOICES = (
        (REFUND_PENDING, 'PENDING'),
        (REFUND_IN_REVIEW, 'IN REVIEW'),
        (EXCHANGE_IN_TRANSIT, 'IN TRANSIT'),
        (EXCHANGE_DELIVERED, 'DELIVERED'),
        (REFUND_INITIATED, 'REFUND INITIATED'),
        (REFUND_REIMBURSED, 'REIMBURSED'),
    )

    return_id = models.CharField(max_length=100, verbose_name='Return Id', null=True, blank=True)

    reason = models.ForeignKey(
        ReturnReason, on_delete=models.SET_NULL, related_name='return_season',
        verbose_name='Reason', null=True
    )

    order = models.ForeignKey(
        'orders.Order',  # or just Order if you've imported it
        on_delete=models.SET_NULL,
        related_name='order_returns',
        null=True,
        verbose_name='Order'
    )

    product = models.ForeignKey(
        'product.Variant', on_delete=models.SET_NULL, related_name='return_product',
        verbose_name='Product', null=True
    )

    purchase_bill = models.FileField(upload_to='return/bill', null=True, blank=True, verbose_name='Purchase Bill')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    refund_method = models.CharField(
        choices=REFUND_METHOD, max_length=70, blank=True, null=True, verbose_name='Refund Method'
    )

    tracking_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Tracking ID')
    shipping_agent = models.CharField(max_length=256, blank=True, null=True, verbose_name='Shipping Agent')

    status = FSMIntegerField(default=PENDING, choices=STATUS_CHOICES, verbose_name='Status', protected=True)

    approved_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='approved_user',
        blank=True, null=True, verbose_name='Approved User'
    )
    approved_comment = models.TextField(blank=True, null=True, verbose_name='Approved Comment')
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name='Approved Date')

    rejected_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='rejected_user',
        blank=True, null=True, verbose_name='Approved User'
    )
    rejected_comment = models.TextField(blank=True, null=True, verbose_name='Rejected Comment')
    rejected_at = models.DateTimeField(blank=True, null=True, verbose_name='Rejected Date')

    # Refund
    refund_status = FSMIntegerField(default=REFUND_PENDING, choices=REFUND_CHOICES, verbose_name='Refund Status',
                                    protected=True)

    refund_tracking_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Refund Tracking ID')
    refund_shipping_agent = models.CharField(max_length=256, blank=True, null=True,
                                             verbose_name='Refund Shipping Agent')
    refund_transaction_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Refund Tracking ID')

    def save(self, *args, **kwargs):
        if not self.return_id:
            self.return_id = generate_return_id()
        super().save(*args, **kwargs)

    @transition(field=status, source=['Submitted'], target='In Review')
    def in_review(self):
        return f"{self.return_id} moved to In Review"

    @transition(field=status, source=['In Review'], target='Approved')
    def approve(self):
        return f"{self.return_id} moved Approved"

    @transition(field=status, source=['In Review'], target='Rejected')
    def reject(self):
        return f"{self.return_id} moved to Reject"

    @transition(field=refund_status, source=['Pending'], target='In Transit')
    def in_transit(self):
        return f"{self.return_id} moved to In Transit"

    @transition(field=refund_status, source=['In Transit'], target='Delivered')
    def delivered(self):
        return f"{self.return_id} moved Delivered"

    @transition(field=refund_status, source=['Pending'], target='Refund Initiated')
    def refund_initiated(self):
        return f"{self.return_id} moved to Refund Initiated"

    @transition(field=refund_status, source=['Refund Initiated'], target='Refunded')
    def refunded(self):
        return f"{self.return_id} moved to Refunded"
