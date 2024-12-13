from django.core.exceptions import PermissionDenied

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Batasi akses untuk Staff
        if request.user.is_authenticated and request.user.groups.filter(name="Staff").exists():
            restricted_paths = ['/admin/blog/post/delete/', '/admin/blog/post/change/']
            if any(path in request.path for path in restricted_paths):
                raise PermissionDenied("Staff are not allowed to perform this action.")
        return self.get_response(request)
