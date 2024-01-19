from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User, Goal, Diary, Like, Todo, Comment, Profile

class LikeInline(GenericTabularInline):
    model = Like

class CommentInline(GenericTabularInline):
    model = Comment
    ct_field = 'content_type'
    id_field = 'object_id'
    extra = 1


class TodoInline(admin.StackedInline):
    model = Todo

class TodoAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
    ]

class DiaryAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        CommentInline,
    ]

class CommentAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
    ]

class GoalAdmin(admin.ModelAdmin):
    inlines = [
        TodoInline,
    ]

# Register your models here.
admin.site.register(User)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Diary, DiaryAdmin)
admin.site.register(Like)
admin.site.register(Todo, TodoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)