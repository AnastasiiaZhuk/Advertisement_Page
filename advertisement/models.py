from django.db import models
from django.core.validators import MinValueValidator


class Heading(models.Model):
    name = models.CharField(max_length=32, db_index=True)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    advertisements = models.ForeignKey(
        Heading,
        on_delete=models.PROTECT,
        related_name='rubric',
    )

    class Meta:
        verbose_name_plural = 'Advertisements'
        ordering = ['-published']
