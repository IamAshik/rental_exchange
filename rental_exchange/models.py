import datetime

from django.conf import settings
from django.urls import reverse
from djrichtextfield.models import RichTextField

from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class Car(models.Model):
    TRANSMISSIONS = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic')
    ]
    FUELS = [
        ('Gasoline', 'Gasoline'),
        ('Diesel', 'Diesel'),
        ('Liquefied Petroleum', 'Liquefied Petroleum'),
        ('Compressed Natural Gas', 'Compressed Natural Gas'),
        ('Ethanol', 'Ethanol'),
        ('Bio-diesel', 'Bio-diesel')
    ]
    PRICE_VARIATIONS = [
        ('Month', 'Month')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, blank=False, null=True)
    model_no = models.CharField(max_length=50, blank=False, null=False)
    model_year = models.IntegerField(
        validators=[MinValueValidator(1984), MaxValueValidator(datetime.date.today().year)], blank=False)
    license_no = models.CharField(max_length=100, null=True, blank=True)
    mileage = models.IntegerField(default=0, blank=False, null=False)
    transmission = models.CharField(max_length=20, choices=TRANSMISSIONS, blank=False, null=False)
    seats = models.IntegerField(default=0, blank=False, null=False)
    luggage = models.IntegerField(default=0, blank=False, null=False)
    fuels = models.ManyToManyField('Fuel', blank=True)
    description = models.TextField(blank=True, null=True)
    rental_price = MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD', blank=False,
                              null=False)
    price_variable = models.CharField(max_length=20, choices=PRICE_VARIATIONS, default='Month', blank=False, null=False)
    features = models.ManyToManyField('Feature', blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='rental_exchange/car_images', null=True, blank=True)
    fitness_test = models.CharField(max_length=20, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], null=True, blank=True)
    agreement_paper = models.FileField(upload_to='rental_exchange/agreement_papers/', null=True, blank=True)
    tags = models.CharField(max_length=512, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "cars"
        verbose_name_plural = "Cars".upper()
        ordering = ("created_at",)
        unique_together = ('name', 'model_no', 'model_year')

    def get_absolute_url(self):
        # return f"car/{self.id}/"
        return reverse('car-detail', args=[self.id])


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='rental_exchange/brand_images', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "brands"
        verbose_name_plural = "Brands".upper()
        ordering = ("name",)


class Feature(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "features"
        verbose_name_plural = "Features".upper()
        ordering = ("title",)


class Fuel(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "fuels"
        verbose_name_plural = "Fuels".upper()
        ordering = ("title",)


# class Owner(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, blank=False, null=False)
#     country = CountryField(blank=False, null=False)
#     city = models.CharField(max_length=100, blank=False, null=False)
#     address = models.CharField(max_length=255, blank=False, null=False)
#     image = models.ImageField(upload_to='rental_exchange/owner_images', null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
#
#     def __str__(self):
#         return self.user
#
#     class Meta:
#         db_table = "owners"
#         verbose_name_plural = "Owners".upper()
#         ordering = ("id",)


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, blank=False, null=False)
#     country = CountryField(blank=False, null=False)
#     city = models.CharField(max_length=100, blank=False, null=False)
#     address = models.CharField(max_length=255, blank=False, null=False)
#     image = models.ImageField(upload_to='rental_exchange/customer_images', null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
#
#     def __str__(self):
#         return self.user
#
#     class Meta:
#         db_table = "customers"
#         verbose_name_plural = "Customers".upper()


class Blog(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    short_description = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="+")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blogs"
        verbose_name_plural = "Blogs".upper()
        ordering = ("-created_at",)


class Comment(models.Model):
    comment = models.TextField(blank=False, null=False)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="+")

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "comments"
        verbose_name_plural = "Comments".upper()
        ordering = ("created_at",)


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    is_seen = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "contacts"
        verbose_name_plural = "Contacts".upper()
        ordering = ("created_at",)


class System(models.Model):
    site_title = models.CharField(max_length=255, default='Rental Exchange', blank=False, null=False)
    site_logo = models.ImageField(upload_to='rental_exchange/system', blank=False, null=False)
    contact_email = models.EmailField(max_length=255, blank=False, null=False)
    contact_phone = models.CharField(max_length=20, blank=False, null=False)
    contact_address = models.CharField(max_length=255, blank=False, null=False)
    email_from = models.EmailField(max_length=255, blank=False, null=False)
    email_from_password = models.CharField(max_length=255, blank=False, null=False)
    email_to = models.EmailField(max_length=255, blank=False, null=False)
    map_url = models.URLField(blank=False, null=False, verbose_name='Map')
    facebook_url = models.URLField(blank=False, null=False, verbose_name='Facebook')
    twitter_url = models.URLField(blank=False, null=False, verbose_name='Twitter')
    instagram_url = models.URLField(blank=False, null=False, verbose_name='Instagram')
    copyright_owner = models.CharField(max_length=100, blank=False, null=False)
    copyright_year = models.IntegerField(
        validators=[MinValueValidator(1984), MaxValueValidator(datetime.date.today().year)], blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="+")

    class Meta:
        db_table = "systems"
        verbose_name_plural = "Systems".upper()


class CarRegistrationRequest(models.Model):
    client_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Your Name')
    client_email = models.EmailField(max_length=100, null=False, blank=False, verbose_name='Email')
    client_phone = models.CharField(max_length=20, blank=False, null=False, verbose_name='Phone')
    client_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address')
    car_title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Car Title')
    car_model = models.CharField(max_length=50, null=False, blank=False, verbose_name='Car Model')
    model_year = models.IntegerField(validators=[MinValueValidator(1984), MaxValueValidator(datetime.date.today().year)], blank=False)
    message = models.TextField(null=True, blank=True)
    is_contacted = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s (%s)' %(self.client_name, self.client_email)

    class Meta:
        db_table = "car_registration_requests"
        verbose_name_plural = "Car Registration Requests".upper()
        ordering = ("-created_at",)


class CarBooking(models.Model):
    REQUEST_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]
    RENT_STATUS = [
        ('On Going', 'On Going'),
        ('Closed', 'Closed')
    ]
    PAYMENT_STATUS = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    ]
    RENT_FOR = [
        ('3', '3 Months'),
        ('4', '4 Months'),
        ('5', '5 Months'),
        ('6', '6 Months'),
        ('7', '7 Months'),
        ('8', '8 Months'),
        ('9', '9 Months'),
        ('10', '10 Months'),
        ('11', '11 Months'),
        ('12', '12 Months')
    ]
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=False, blank=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="+")
    start_date = models.DateField(blank=False, null=False)
    rent_for = models.CharField(max_length=50, choices=RENT_FOR, blank=False, null=False)
    rental_cost = MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD', blank=True, null=True)
    is_seen = models.BooleanField(default=False, blank=True)
    request_status = models.CharField(max_length=50, choices=REQUEST_STATUS, default='Pending', blank=True)
    rent_status = models.CharField(max_length=50, choices=RENT_STATUS, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='Unpaid', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="+")

    def __str__(self):
        return '%s' %(self.car)

    class Meta:
        db_table = "car_booking"
        verbose_name_plural = "Car Bookings".upper()
        ordering = ("-created_at",)


class PaymentHistory(models.Model):
    PAYMENT_METHODS = [
        ('Hand Cash', 'Hand Cash'),
        ('PayPal', 'PayPal')
    ]
    booking = models.OneToOneField('CarBooking', on_delete=models.CASCADE, null=False, blank=False)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='Hand Cash')
    amount = MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD', blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking

    class Meta:
        db_table = "payment_history"
        verbose_name_plural = "Payment History".upper()
        ordering = ("-payment_date",)


class TransactionHistory(models.Model):
    booking = models.ForeignKey('CarBooking', on_delete=models.CASCADE, blank=False, null=False)
    added_amount = MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.booking.car.owner

    class Meta:
        db_table = "transaction_history"
        verbose_name_plural = "Transaction History".upper()
        ordering = ("-created_at",)


class VehicleOwnerAccount(models.Model):
    account_holder = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    total_income = MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD', blank=True, null=True)
    last_added_amount = MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_holder

    class Meta:
        db_table = "vehicle_owner_account"
        verbose_name_plural = "Vehicle Owner Accounts".upper()
        ordering = ("account_holder",)