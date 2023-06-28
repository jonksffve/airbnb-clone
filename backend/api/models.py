from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(_("Category"), max_length=50)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(_("Title"), max_length=50,
                             blank=False, null=False)
    description = models.TextField(_("Description"), blank=False, null=False)
    image = models.ImageField(
        _("Cover image"), upload_to='listings/', default='placeholder.jpeg', blank=False, null=False)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(1)])
    guestCount = models.SmallIntegerField(
        _("Guests"), blank=False, null=False, validators=[MinValueValidator(1)])
    roomCount = models.SmallIntegerField(
        _("Guests"), blank=False, null=False, validators=[MinValueValidator(1)])
    bathroomCount = models.SmallIntegerField(
        _("Guests"), blank=False, null=False, validators=[MinValueValidator(1)])
    category = models.ForeignKey("Category", verbose_name=_(
        "Category"), on_delete=models.CASCADE, blank=False, null=False)
    location = models.CharField(
        _("Location"), max_length=50, blank=False, null=False)

    def __str__(self):
        return self.title
