from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from .models import Profile, User, Goal

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Goal.objects.create(created_by=instance, title='목표 1')
        Goal.objects.create(created_by=instance, title='목표 2')
        Goal.objects.create(created_by=instance, title='목표 3')
        if instance.email:
            Profile.objects.create(user=instance, username=instance.email)
        elif instance.kakao_id:
            Profile.objects.create(user=instance, username=f'kakao{instance.kakao_id}')
        else:
            Profile.objects.create(user=instance, username=f'guest{User.objects.count()}')