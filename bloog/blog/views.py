from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from .forms import BlogForm, UserRegisterForm, UserLoginForm, ContactForm
from .models import Blog, Category
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {"form": form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'vitalii.podgornii@ukr.net',
                             ['vitalii.podgornii@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка Валидации')
    else:
        form = ContactForm()
    return render(request, 'blog/test.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def text(request):
    objects = []


class HomeBlog(MyMixin, ListView):
    model = Blog
    template_name = 'blog/home_blog_list.html'
    context_object_name = 'blog'
    mixin_prop = 'hello world'
    paginate_by = 2

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('category')


class BlogByCategory(MyMixin, ListView):
    model = Blog
    template_name = 'blog/home_blog_list.html'
    context_object_name = 'blog'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Blog.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewBlog(DetailView):
    model = Blog
    context_object_name = 'blog_item'
    # template_name = 'blog/blog_detail.html'
    # pk_url_kwarg = 'blog_id'


class CreateBlog(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = 'blog/add_blog.html'
    # success_url = reverse_lazy('home')
    raise_exception = True


# def index(request):
#     blog = Blog.objects.order_by('-created_at')
#     context = {
#         'blog': blog,
#         'title': 'Список новостей',
#     }
#     return render(request, 'blog/index.html', context)


# Для того что бы можно было переходить по категориям на сайте, используем функию(def get_category)
def get_category(request, category_id):
    blog = Blog.objects.filter(category_id=category_id)

    category = Category.objects.get(pk=category_id)
    return render(request, 'blog/category.html', {'blog': blog, 'category': category})

# def view_blog(request, blog_id):
#     #    blog_item = Blog.objects.get(pk=blog_id)
#     blog_item = get_object_or_404(Blog, pk=blog_id)
#     return render(request, 'blog/view_blog.html', {'blog_item': blog_item})


# def add_blog(request):
#     if request.method == 'POST':
#         form = BlogForm(request.POST)
#         if form.is_valid():
#             # blog = Blog.objects.create(**form.cleaned_data)
#             blog = form.save()
#             return redirect(blog)
#     else:
#         form = BlogForm()
#     return render(request, 'blog/add_blog.html', {'form': form})
