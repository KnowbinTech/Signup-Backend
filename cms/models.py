from django.db import models
from users.models.base_model import BaseModel


class HeroSection(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Title')
    cta_text = models.CharField(max_length=256, verbose_name='CTA Button Text')
    short_description = models.CharField(max_length=256, verbose_name='Short Description')
    link = models.CharField(max_length=512, verbose_name='CTA Button Link')
    image = models.CharField(max_length=300, verbose_name='Image')

    def __str__(self):
        return f"{self.title}"

