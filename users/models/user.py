from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


def generate_customer_id():
    user_last = User.objects.filter(is_customer=True).order_by('-id')
    if user_last.count() > 0:
        last_customer_id = user_last[0].customer_id
        number = int(last_customer_id[6:]) + 1
    else:
        number = 1
    customer_key = f"{number:06}"
    customer_id = f"SC-USR{customer_key}"

    if User.objects.filter(is_customer=True, customer_id=customer_id).exists():
        return generate_customer_id()
    return customer_id


class User(AbstractUser):
    GENDER = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Prefer Not to say', 'Prefer Not to say'),
    )
    # Override default fields to make them optional
    first_name = None
    last_name = None

    # Replace first_name and last_name with a single name field
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name='Email')

    sub = models.CharField(max_length=125)
    is_customer = models.BooleanField(default=False)
    customer_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Customer ID')
    mobile_number = models.CharField(null=True, max_length=15, verbose_name='Mobile Number')

    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date Of Birth')
    gender = models.CharField(choices=GENDER, max_length=25, blank=True, null=True, verbose_name='Gender')

    profile_picture = models.FileField(upload_to='profile/', blank=True, null=True, verbose_name='Profile Picture')
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)

    is_suspended = models.BooleanField(default=False)

    store_manager = models.BooleanField(default=False)
    other_information = models.JSONField(default={}, blank=True, null=True, verbose_name='Other Information')

    ########################################
    # BaseModel
    ########################################
    created_by = models.ForeignKey('User', related_name='%(class)s_created_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Created By')
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Created At')

    updated_by = models.ForeignKey('User', related_name='%(class)s_updated_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Updated By')
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Updated At')

    deleted = models.BooleanField(default=False, verbose_name='Deleted')
    deleted_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Deleted At')
    deleted_by = models.ForeignKey('User', related_name='%(class)s_deleted_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Deleted By')

    ########################################

    class Meta(AbstractUser.Meta):
        pass

    def get_full_name(self):
        return self.name if self.name else self.username

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.is_customer and not self.customer_id:
            self.customer_id = generate_customer_id()
        super().save(*args, **kwargs)

