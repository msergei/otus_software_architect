from django.contrib.auth.models import User
from django.db import models
import unicodedata

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, username):
        """
        Creates and saves a User with the given email and password.
        """

        user = self.model(
            username=username,
        )

        user.save(using=self._db)
        return user


class AbstractBaseUser(models.Model):
    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username


class UserProfile(AbstractBaseUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        primary_key=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )

    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)

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
