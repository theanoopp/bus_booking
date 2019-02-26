from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    phonenum = models.CharField(max_length=11, blank=True, default='')
    city = models.CharField(max_length=40, blank=True, default='')
    gender = models.CharField(max_length=1, blank=True, default='')
    dob = models.CharField(max_length=20, blank=True, default='')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class TravellerDetails(models.Model):
    name = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    seatNumber = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=40)
    fare = models.IntegerField()
    etstNumber = models.CharField(max_length=40)
    seatStatus = models.CharField(max_length=40)


class TicketDetails(models.Model):
    etstnum = models.CharField(max_length=40)
    pnrnum = models.CharField(max_length=40)
    ticketStatus = models.CharField(max_length=40)
    ticketdump = models.CharField(max_length=40)



