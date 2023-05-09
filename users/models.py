from django.db import models #type: ignore
from django.db.models.signals import post_save
from typing import List
from django.dispatch import receiver
from django.utils import timezone #type: ignore
from django.contrib.auth.models import ( #type: ignore
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User)
from django.utils.translation import gettext_lazy as _ #type: ignore


class UserManager(BaseUserManager):
    """
    Manager for the CustomUser model. Use this to perform actions on a CustomUser object.
    """
    def _create_user(
            self,
            email: str,
            password: str,
            is_staff: bool,
            is_superuser: bool,
            **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user: User = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> User:
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email:str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email authentication
    """
    class UserCategory(models.TextChoices):
        STUDENT = 'ST', _('Student')
        LECTURER = 'LE', _('Lecturer')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(blank=False, max_length=255, unique=True, verbose_name='email address')
    username = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=2, choices=UserCategory.choices, default=UserCategory.STUDENT)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects: UserManager = UserManager()

    def get_absolute_url(self):
        return f"/users/{self.pk}"

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        return super(CustomUser, self).save(*args, **kwargs)


class Profile(models.Model):
    """
    Contains extra information about a user
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to='images/profile_pics', null=True, blank=True)
    about = models.TextField(max_length=500, null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.pk} - {self.user.email}"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return None #"https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_960_720.png"



@receiver(post_save, sender=CustomUser, dispatch_uid="create_user_profile")
def create_profile_on_user_create(sender, instance, created, **kwargs):
    if created == True:
        Profile.objects.create(user=instance)


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    can_create_post = models.BooleanField(default=False)
    can_alter_post = models.BooleanField(default=False)
    can_delete_post = models.BooleanField(default=False)
    can_create_user = models.BooleanField(default=False)
    can_alter_user = models.BooleanField(default=False)
    can_delete_user = models.BooleanField(default=False)
    can_create_podcast = models.BooleanField(default=False)
    can_alter_podcast = models.BooleanField(default=False)
    can_delete_podcast = models.BooleanField(default=False)
    can_create_opportunities = models.BooleanField(default=False)
    can_update_opportunities = models.BooleanField(default=False)
    can_delete_opportunities = models.BooleanField(default=False)

    @classmethod
    def create_super_staff(cls, user: User):
        super_staff: Staff = Staff.objects.create(user=user,
            can_create_post = True,
            can_alter_post = True,
            can_delete_post = True,
            can_create_user = True,
            can_alter_user = True,
            can_delete_user = True,
            can_create_podcast = True,
            can_alter_podcast = True,
            can_delete_podcast = True,
            can_create_opportunities = True,
            can_update_opportunities = True,
            can_delete_opportunities = True,
        )
        super_staff.save()
        return super_staff


    def __str__(self) -> str:
        return self.user.email
