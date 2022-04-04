from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, email, date_of_birthday, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            first_name=first_name,
            email=self.normalize_email(email),
            date_of_birthday=date_of_birthday,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, email, date_of_birthday, password):
        user = self.create_user(first_name, email, password=password, date_of_birthday=date_of_birthday)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ManagerModel(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=13, null=True)
    email = models.EmailField(verbose_name='email address', null=True, max_length=25)
    date_of_birthday = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'first_name'
    REQUIRED_FIELDS = ['date_of_birthday', 'email']

    objects = MyUserManager()

    def get_full_name(self):
        return self.first_name

    # def has_perm(self, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     return True

    def __str__(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class OrderModel(models.Model):
    Product_Status = (
        ('шт', 'шт'),
        ('усл', 'усл'),
    )

    manager = models.ForeignKey(ManagerModel, on_delete=models.CASCADE, related_name='manager')
    customer = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    created = models.DateField(null=True)
    limit = models.DateField(null=True)
    product = models.CharField(max_length=400)
    number = models.IntegerField()
    price = models.IntegerField()
    percent = models.IntegerField()
    status_order = models.CharField(max_length=20, choices=Product_Status, default='шт', null=True, blank=True)
    product1 = models.CharField(max_length=400, null=True, blank=True)
    number1 = models.IntegerField(null=True, blank=True)
    price1 = models.PositiveIntegerField(null=True, blank=True)
    percent1 = models.IntegerField(null=True, blank=True)
    status_order1 = models.CharField(max_length=100, choices=Product_Status, default='шт', null=True, blank=True)
    product2 = models.CharField(max_length=400, null=True, blank=True)
    number2 = models.IntegerField(null=True, blank=True)
    price2 = models.PositiveIntegerField(null=True, blank=True)
    percent2 = models.IntegerField(null=True, blank=True)
    status_order2 = models.CharField(max_length=100, choices=Product_Status, default='шт', null=True, blank=True)
    product3 = models.CharField(max_length=400, null=True, blank=True)
    number3 = models.IntegerField(null=True, blank=True)
    price3 = models.PositiveIntegerField(null=True, blank=True)
    percent3 = models.IntegerField(null=True, blank=True)
    status_order3 = models.CharField(max_length=100, choices=Product_Status, default='шт', null=True, blank=True)
    product4 = models.CharField(max_length=400, null=True, blank=True)
    number4 = models.IntegerField(null=True, blank=True)
    price4 = models.PositiveIntegerField(null=True, blank=True)
    percent4 = models.IntegerField(null=True, blank=True)
    status_order4 = models.CharField(max_length=100, choices=Product_Status, default='шт', null=True, blank=True)

    def __str__(self):
        return str(self.manager)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    @property
    def all_price(self):
        total = self.price * self.number
        return total
