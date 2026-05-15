from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class AdminProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.PositiveBigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='placeholder.jpg', upload_to='admin', null=True, blank=True)


class SellerProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.PositiveBigIntegerField(null=True, blank=True)
    shop_name = models.CharField(max_length=200, null=True)
    shop_address = models.CharField(max_length=500, null=True, blank=True)
    gst_number = models.CharField(max_length=20, null=True)
    verified = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    image = models.ImageField(default='placeholder.jpg', upload_to='seller', null=True, blank=True)


class CustomerProfile(models.Model):
    gender_choice = (('Male','Male'), ('Female', 'Female'), ('Other','Other'))
    user = OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=30, choices=gender_choice, null=True, blank=True)
    contact_number = models.PositiveBigIntegerField(null=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(default='placeholder.jpg', upload_to='customer')


class Category(models.Model):
    category = models.CharField(max_length=500)

    def __str__(self):
        return self.category


class Subcategory(models.Model):
    subcategory = models.CharField(max_length=500)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, default='Select Subcategory')

    def __str__(self):
        return self.subcategory



class Feedback(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)


class Inquiry(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)






@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            user = AdminProfile.objects.create(user=instance)
            gr, cr = Group.objects.get_or_create(name="admin")
            instance.groups.add(gr)
            user.save()

    



