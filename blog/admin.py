from django.contrib import admin
from .models import Post, Comment, Profile , Category, Tag, Like
from django.contrib.auth.models import Group

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at', 'category', 'tags')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        #Batasi queryset untuk Staff
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Staff").exists():
            return qs.filter(author=request.user)
        return qs

    def has_delete_permission(self, request, obj=None):
        #Batasi delete permission untuk Staff
        if request.user.groups.filter(name="Staff").exists():
            return False
        return True

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('author', 'created_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Like)

def create_default_groups():
    superuser_group, _ = Group.objects.get_or_create(name="Superusers")
    staff_group, _ = Group.objects.get_or_create(name="Staff")

create_default_groups()