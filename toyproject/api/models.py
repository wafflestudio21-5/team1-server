from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from datetime import date

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    email = models.EmailField(null=True, unique=True)
    kakao_id = models.BigIntegerField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def __str__(self):
        return str(self.id)
    
    @property
    def created_at_iso(self):
        return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        related_name='profile',
        on_delete=models.CASCADE, 
        primary_key=True
    )
    intro = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        if not self.username:
            return 'null'
        else:
            return self.username

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

    color = models.CharField(max_length=25, default='blue')

    created_by = models.ForeignKey(User, related_name='goals', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.created_by}'
    
    @property
    def created_at_iso(self):
        return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='likes', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey('content_type', 'object_id')

    emoji = models.CharField(max_length=64)

    def __str__(self):
        return f"like by {self.user} on {self.liked_object}"

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='comments', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    commented_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation(Like)

    def __str__(self):
        return f"comment by {self.user} on {self.commented_object}"
    
    @property
    def created_at_iso(self):
        return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

class Todo(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=None, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    goal = models.ForeignKey(Goal, related_name='todos', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='todos', on_delete=models.CASCADE)
    likes = GenericRelation(Like)
    image = models.ImageField(upload_to='todo_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def created_at_iso(self):
        return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    @property
    def reminder_iso(self):
        if self.reminder is None:
            return None
        else:
            return self.reminder.strftime('%p') + ' ' + self.reminder.strftime('%I:%M')
    
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
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        null=True,
        blank=True
    )
    image = models.ImageField(null=True, blank=True)
    emoji = models.CharField(max_length=64)
    color = models.CharField(max_length=25, default='blue')
    created_by = models.ForeignKey(User, related_name='diarys', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.date} diary by {self.created_by}"


