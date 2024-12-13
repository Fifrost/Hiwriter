from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post


def create_default_groups_and_permissions():
    # Buat atau dapatkan grup Superusers
    superuser_group, created = Group.objects.get_or_create(name="Superusers")
    if created:
        print("Superusers group created.")

    # Buat atau dapatkan grup Staff
    staff_group, created = Group.objects.get_or_create(name="Staff")
    if created:
        print("Staff group created.")

    # Dapatkan content type untuk model Post
    post_content_type = ContentType.objects.get_for_model(Post)

    # Tambahkan semua permissions untuk Superusers
    superuser_permissions = Permission.objects.filter(content_type=post_content_type)
    superuser_group.permissions.set(superuser_permissions)
    print("All permissions assigned to Superusers group.")

    # Tambahkan permission terbatas untuk Staff (view dan add saja)
    staff_permissions = Permission.objects.filter(
        content_type=post_content_type,
        codename__in=["view_post", "add_post"]
    )
    staff_group.permissions.set(staff_permissions)
    print("Limited permissions assigned to Staff group.")

    print("Groups and permissions setup complete!")


if __name__ == "__main__":
    print("This script should be run with Django's shell.")
