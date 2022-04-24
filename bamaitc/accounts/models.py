import random
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
import pyotp
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField





class UserManager(BaseUserManager):
   
    def create_user(self, username, email, phone, password, **extra_fields):
        """
        Create and save a User with the given email, phone number and password.
        """
        if not email:
            raise ValueError('ایمیل باید وارد شود')
        if not phone:
            raise ValueError('شماره همراه باید وارد شود')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, username, email, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, phone number and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, phone, password, **extra_fields)
    
    
    
    
    
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + str(random.randint(0, 12000))
    return unique_slug






class Country(models.Model):
    name = models.CharField(_("name of country"), max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(_("name of city"), max_length=50)
    country = models.ForeignKey(Country, verbose_name=_("country of city"), on_delete=models.CASCADE)


    def __str__(self):
        return self.name




class CustomUser(AbstractUser):
    phone_regex = RegexValidator( regex = '^9\d{9}$', message ="شماره همراه باید به فرمت (9xxxxxxxxx) وارد شود.")
    phone = models.CharField(_('شماره همراه'),validators =[phone_regex], max_length=10, unique=True,null=True)
    email = models.EmailField(_('آدرس ایمیل'), unique=True)
    REQUIRED_FIELDS = ['email', 'phone']
    is_verified = models.BooleanField('تایید شد', default=False, help_text='Designates whether this user has verified phone')
    key = models.CharField(max_length=100, unique=True, blank=True)



    objects = UserManager()  


    def __str__(self):
        return f'{self.phone} / {self.username}' 
    
    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        #Here we are using Time Based OTP. The interval is 60 seconds.
        #otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.key, interval=300)
        return t.verify(provided_otp)
    
    
        

class Profile(models.Model):
    slug = models.SlugField(_("اسلاگ"), blank=True)
    Male= 'male'
    Female= 'fmle'
    STATUS= [
        (Male, 'مذکر'),
        (Female, 'مونث'),
    ]
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")
    first_name = models.CharField(_("نام"), max_length=50)
    last_name = models.CharField(_("نام خانوادگی"), max_length=50)
    invite_code = models.CharField(_("کد معرفی "), max_length=20, unique=True)
    description = models.TextField(_("بیوگرافی"), null=True, blank=True)
    address = models.CharField(_("آدرس"),max_length=30,blank=True)
    date_joined = models.DateTimeField(_("تاریخ پیوستن"),auto_now_add=True)
    age = models.PositiveIntegerField(_("سن"),null=True, blank=True)
    sexuality = models.CharField(_("جنسیت"), max_length=4, choices=STATUS, default=Male)
    updated_on = models.DateTimeField(_("تاریخ ویرایش"),auto_now=True)
    image = models.ImageField("عکس کاربر",upload_to='uploads/profile', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    city = models.ForeignKey(City, verbose_name=_("شهر"), on_delete=models.CASCADE, null=True, blank=True)
    use_invite_code = models.BooleanField(_("استفاده از کد معرف"), default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.first_name))
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return self.user.username
    

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="wallet")
    date_create = models.DateTimeField(_("تاریخ ایجاد"), auto_now=False, auto_now_add=True)
    cash = models.PositiveIntegerField(_("موجودی کیف پول"), default=0)

    def __str__(self):
        return f'{self.user.username} / {self.cash}'
    
    
    
class DesinedSite(models.Model):
    name = models.CharField(_("name"), max_length=50)
    url = models.URLField(_("url"), max_length=200)
    image = models.ImageField(_("image"), upload_to='uploads/desinedsite', height_field=None, width_field=None, max_length=None)
    desc = RichTextUploadingField(blank=True)
    
    
    
    def __str__(self):
        return f'{self.name}'
    
    
    
    
class ApplicationDesined(models.Model):
    name = models.CharField(_("name"), max_length=50)
    url = models.URLField(_("url"), max_length=200)
    image = models.ImageField(_("image"), upload_to='uploads/desinedsite', height_field=None, width_field=None, max_length=None)
    desc = RichTextUploadingField(blank=True)
    plat = models.CharField(_("platform"), max_length=50, default='android')
    
    
    
    def __str__(self):
        return f'{self.name}'
    
    