from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from datetime import date

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        related_name='profile',
        on_delete=models.CASCADE, 
        primary_key=True
    )
    intro = models.TextField(null=True, blank=True)
    display_name = models.CharField(max_length=15, null=True, blank=True, default=None)
    profile_pic = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # If display_name is not provided, set it to the username of the associated User.
        if not self.display_name:
            self.display_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username + "'s Profile"

class Goal(models.Model):
    title = models.CharField(max_length=64)
    
    PUBLIC = 'PB'
    PRIVATE = 'PR'
    FOLLOWERS = 'FL'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (FOLLOWERS, 'Followers'),
    ]
    visibility = models.CharField(
        max_length=2, 
        choices=VISIBILITY_CHOICES,
        default=FOLLOWERS
    )

    color = models.CharField(max_length=25, default='white')

    created_by = models.ForeignKey(User, related_name='goals', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.created_by}'

class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='likes', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"like by {self.user} on {self.liked_object}"

class Todo(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    reminder = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=date.today)
    is_completed = models.BooleanField(default=False)
    goal = models.ForeignKey(Goal, related_name='todos', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='todos', on_delete=models.CASCADE)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title
    
class Diary(models.Model):
    description = models.TextField()
    PUBLIC = 'PB'
    PRIVATE = 'PR'
    FOLLOWERS = 'FL'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (FOLLOWERS, 'Followers'),
    ]
    visibility = models.CharField(
        max_length=2, 
        choices=VISIBILITY_CHOICES, 
        default=FOLLOWERS
    )
    mood = models.IntegerField(
        default=50,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    image = models.ImageField(null=True, blank=True)
    emoji = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    color = models.CharField(max_length=25, default='white')
    created_by = models.ForeignKey(User, related_name='diarys', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    likes = GenericRelation(Like)

    def __str__(self):
        return f"{self.date} diary by {self.created_by}"


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, related_name='comments', on_delete=models.CASCADE)
    likes = GenericRelation(Like)

    def __str__(self):
        return f"comment by {self.user} on {self.diary}"