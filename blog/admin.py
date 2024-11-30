from django.contrib import admin
from .models import Post, Comment, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Menampilkan kolom judul, penulis, dan waktu dibuat
    search_fields = ('title', 'content')  # Memungkinkan pencarian berdasarkan judul dan konten
    list_filter = ('author', 'created_at')  # Menyediakan filter berdasarkan penulis dan tanggal dibuat
    ordering = ('-created_at',)  # Mengurutkan postingan berdasarkan tanggal pembuatan, terbaru di atas

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('author', 'created_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)

