from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(_("Category"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

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
    location = models.CharField(
        _("Location"), max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(_("Date"), auto_now_add=True, blank=True)
    creator = models.ForeignKey(
        "accounts.User", verbose_name=_("Creator"), on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey("Category", verbose_name=_(
        "Category"), on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

    def __str__(self):
        return self.title


class FavoriteListing(models.Model):
    listing = models.ForeignKey(Listing, verbose_name=_(
        ""), related_name='favorites', on_delete=models.CASCADE)
    user = models.ForeignKey(
        "accounts.User", verbose_name=_(""), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'user'], name='unique_listing_user')
        ]

    def __str__(self):
        return f'{self.user.get_full_name()} favorites {self.listing.id}'
