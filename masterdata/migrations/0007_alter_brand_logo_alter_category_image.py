# Generated by Django 4.2.4 on 2024-11-23 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0006_remove_brand_tags_remove_category_tags_brand_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='image'),
        ),
    ]