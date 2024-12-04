from django.db import models
from users.models.base_model import BaseModel


class HeroSection(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Title')
    cta_text = models.CharField(max_length=256, verbose_name='CTA Button Text')
    short_description = models.CharField(max_length=256, verbose_name='Short Description')
    link = models.CharField(max_length=512, verbose_name='CTA Button Link')
    image = models.FileField(upload_to='hero_section/', blank=True, null=True, verbose_name='Image')
    is_in_shop_page = models.BooleanField(default=False, verbose_name='Is in Shop Page')

    def save(self, *args, **kwargs):
        if self.is_in_shop_page:
            # Delete the existing row with `is_in_shop_page=True`
            HeroSection.objects.filter(is_in_shop_page=True).exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

