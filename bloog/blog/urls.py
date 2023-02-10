from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [


    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('contact/', contact, name='contact'),

    path('logout/', user_logout, name='logout'),
    #path('', index, name='home'),
    path('', cache_page(60) (HomeBlog.as_view()), name='home'),
    #Ниже передаем путь по пареметру
    #path('category/<int:category_id>/',get_category, name='category'),
    path('category/<int:category_id>/',BlogByCategory.as_view(), name='category'),
    #path('blog/<int:blog_id>/',view_blog, name='view_blog'),
    path('blog/<int:pk>/',ViewBlog.as_view(), name='view_blog'),
    #path('blog/add-blog/',add_blog, name='add_blog'),
    path('blog/add-blog/',CreateBlog.as_view(), name='add_blog'),
]