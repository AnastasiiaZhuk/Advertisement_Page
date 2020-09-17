from django.db import models
from django.core.validators import MinValueValidator

from user.models import AdvUser
from user.utilities import get_timestamp_path


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Name')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Order')
    super_rubric = models.ForeignKey(
        'SuperRubric', on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Super Rubric'
    )


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Super Rubric'
        verbose_name_plural = 'Super Rubrics'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = (
            'super_rubric__order', 'super_rubric__name',
            'order', 'name'
        )
        verbose_name = 'Sub Rubric'
        verbose_name_plural = 'Sub Rubrics'


class Advertisement(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published at')
    contacts = models.TextField(verbose_name='Contacts')
    image = models.ImageField(upload_to=get_timestamp_path, blank=True, verbose_name='Images')
    is_active = models.BooleanField(db_index=True, default=True, verbose_name='Print in list?')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Author')
    rubric = models.ForeignKey(
        SubRubric,
        on_delete=models.PROTECT,
        related_name='heading'
    )

    def delete(self, *args, **kwargs):
        for ai in self.additional_image_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Advertisements'
        ordering = ['-published']


class AdditionalImage(models.Model):
    adv = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name='Advertisement'
    )
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name_plural = "Additional Images"
