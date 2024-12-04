from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .forms import PostForm, CommentForm, UserForm, ProfileForm, CustomUserCreationForm
from .models import Post, Comment, Tag, Category


def landing_page(request):
    return render(request, 'blog/landing_page.html')

# Home Page
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

# Create Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)

        # Menetapkan tags ke post yang baru
        selected_tags = self.request.POST.getlist('tags')  # Mendapatkan tag yang dipilih
        post.save()  # Simpan post terlebih dahulu

        post.tags.set(selected_tags)  # Menetapkan tags
        post.save()  # Simpan ulang

        return super().form_valid(form)

# Edit Post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')


# Delete Post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')


# Register User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            # Menangani jika password tidak cocok atau kesalahan lainnya
            messages.error(request, "Passwords do not match!")
    else:
        form = UserCreationForm()

    return render(request, 'blog/register.html', {'form': form})

# User Dashboard
@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(post__author=request.user)

    context = {
        'total_posts': user_posts.count(),
        'total_comments': user_comments.count(),
        'posts': user_posts,
        'no_posts': user_posts.count() == 0,
        'no_comments': user_comments.count() == 0,
    }
    return render(request, 'blog/dashboard.html', context)


# User Profile
@login_required
def profile(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined,
    }
    return render(request, 'blog/profile.html', context)


# Edit User Profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'blog/edit_profile.html', context)


# Post Detail
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)


# Change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Menghindari logout setelah password diubah
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'blog/change_password.html', {'form': form})


# Custom Logout
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# Category Detail
class CategoryDetailView(ListView):
    model = Post
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        # Ambil kategori berdasarkan ID yang diberikan di URL
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        # Kembalikan postingan yang terkait dengan kategori tersebut
        return Post.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        # Menambahkan kategori ke dalam context untuk digunakan di template
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context

# Tag Detail
class TagDetailView(ListView):
    model = Post
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'

    def get_queryset(self):
        # Ambil tag berdasarkan ID yang diberikan di URL
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        # Kembalikan postingan yang memiliki tag tersebut
        return Post.objects.filter(tags=tag)

    def get_context_data(self, **kwargs):
        # Menambahkan tag ke dalam context untuk digunakan di template
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return context

def get_tags(request, category_id):
    # Mengambil tag yang sesuai dengan kategori yang dipilih
    tags = Tag.objects.filter(category_id=category_id)
    tag_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return JsonResponse({'tags': tag_list})



def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            # Ambil tags yang dipilih
            selected_tags = request.POST.getlist('tags')  # Mengambil semua ID tag yang dipilih
            post.tags.set(selected_tags)  # Menetapkan tags pada post

            post.save()

            # Redirect atau beri response
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})

def get_tags_by_category(request):
    category_id = request.GET.get('category_id')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            tags = Tag.objects.filter(category=category)
            tag_data = [{'id': tag.id, 'name': tag.name} for tag in tags]
            return JsonResponse({'tags': tag_data})
        except Category.DoesNotExist:
            return JsonResponse({'tags': []})
    return JsonResponse({'tags': []})
