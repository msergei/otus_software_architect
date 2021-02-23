from django.contrib.auth.models import User, UserManager, AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class UserProfile(AbstractUser):
    username = models.CharField(
        max_length=150,
        primary_key=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )
    email = models.EmailField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [username]

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return False

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return False

    @property
    def is_active(self):
        "Is the user active?"
        return True


class Wallet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    currency = models.ForeignKey('Currency', on_delete=models.RESTRICT)
    wallet = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0)],
        help_text='User wallet',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.currency.title}: {self.wallet}'

    class Meta:
        unique_together = ('user', 'currency')


class Currency(models.Model):
    title = models.CharField(max_length=12, primary_key=True)
    wallets = models.ManyToManyField(UserProfile, through=Wallet)

    def __str__(self):
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    user = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    currency_from = models.ForeignKey(Currency, on_delete=models.RESTRICT, related_name='currency_from')
    currency_to = models.ForeignKey(Currency, on_delete=models.RESTRICT, related_name='currency_to')

    success = models.BooleanField(null=True, blank=True)
    reason = models.CharField(max_length=512, null=True, blank=True)
    unique_key = models.PositiveBigIntegerField(unique=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.currency_from}-{self.currency_to}: {self.amount}'

    class Meta:
        unique_together = ('user', 'unique_key', 'currency_from', 'currency_to', 'amount'),
