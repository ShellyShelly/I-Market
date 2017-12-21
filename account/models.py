from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, surname=None, address=None,
                    is_active=True, is_staff=False, is_admin=False, is_confirmed=False):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.is_confirmed = is_confirmed
        user.name = name
        user.surname = surname
        user.address = address
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name        = models.CharField(max_length=255, blank=True, null=True)
    surname     = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(verbose_name='Postal code', max_length=20, default='76000', blank=True, null=True)
    email       = models.EmailField(
                verbose_name='email',
                max_length=255,
                unique=True,
                )
    mobile = models.CharField(max_length=12, blank=True, null=True)
    active      = models.BooleanField(default=True) # can login
    staff       = models.BooleanField(default=False)  # is an admin user; non super-user
    admin       = models.BooleanField(default=False)  # is a superuser
    is_confirmed   = models.BooleanField(default=False)  # is account confirmed
    confirmation_date = models.DateTimeField()  # date and time of email(account at general) confirmation
    last_login     = models.DateTimeField(auto_now_add=True)  # date and time of last login
    # "Password field" built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def get_absolute_url(self):
        pass

    def get_full_name(self):
        # The user is identified by their email address
        full_name = '%s %s'.format(self.name, self.surname)
        return full_name.strip()

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    """
    def email_user(self):
        # Sends an email to this user
        send_mail(subject, message, from_email, [self.email])
    """

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        # "Is the user an admin member?"
        return self.admin

    @property
    def is_active(self):
        # "Is the user active?"
        return self.active
