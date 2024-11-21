from django.db import models
from users.models.base_model import BaseModel
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Tag(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)

    def __str__(self):
        return self.name


class Attribute(BaseModel):
    name = models.CharField(max_length=80, null=True, verbose_name='Name')
    value = ArrayField(models.CharField(max_length=100), blank=True, null=True, default=list, verbose_name='Values')
    # value = models.JSONField(default=list, null=True, verbose_name='Values')

    def __str__(self):
        return self.name


class Dimension(BaseModel):
    DIMENSION_UNIT = (
        ('mm', 'mm'),
        ('cm', 'cm'),
        ('inch', 'inch'),
        ('M', 'M'),
    )

    WEIGHT_UNIT = (
        ('gm', 'gm'),
        ('Kg', 'Kg'),
    )

    length = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Length')
    breadth = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Breadth')
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Height')

    dimension_unit = models.CharField(max_length=20, choices=DIMENSION_UNIT, verbose_name='Dimension Unit', null=True,
                                      blank=True)

    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Weight')
    weight_unit = models.CharField(max_length=20, choices=WEIGHT_UNIT, verbose_name='Weight Unit', null=True,
                                   blank=True)

    def __str__(self):
        return f"{self.length}-{self.breadth}-{self.height}-{self.dimension_unit} {self.weight}{self.weight_unit}"


class Brand(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)
    logo = models.CharField(max_length=300, blank=True, null=True, verbose_name='Logo')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    tags = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True, default=list, verbose_name='Tags')

    def __str__(self):
        return self.name

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()


class AttributeGroup(BaseModel):
    name = models.CharField(max_length=75, null=True, verbose_name='Name')
    attributes = models.ManyToManyField(Attribute, related_name='attributeitems', null=True, verbose_name='Attributes')

    def __str__(self):
        return self.name if self.name else 'AttributeGroupObject({})'.format(self.id)


class Category(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    handle = models.CharField(max_length=75, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')

    parent_category = models.ForeignKey(
        'Category', related_name='subcategory', verbose_name='Parent Category',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    attribute_group = models.ForeignKey(
        AttributeGroup, related_name='attributegroup', verbose_name='Attribute Groups',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    image = models.FileField(upload_to='category/images', blank=True, null=True, verbose_name='Image')

    is_main_menu = models.BooleanField(default=False, verbose_name='Main Menu')
    is_top_category = models.BooleanField(default=False, verbose_name='Top Category')

    tags = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True, default=list, verbose_name='Tags')

    def __str__(self):
        return self.name

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()


class ReturnReason(BaseModel):
    title = models.CharField(max_length=512, null=True, verbose_name='Reason')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return self.title
